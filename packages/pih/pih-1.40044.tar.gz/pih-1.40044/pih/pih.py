import calendar
from collections import defaultdict
from datetime import datetime, timedelta
from getpass import getpass
import importlib.util
import locale
import os
import platform
import json
import requests
import re
import subprocess
import sys
from typing import Any, Callable, List, Tuple
import colorama
from colorama import Back, Style, ansi, Fore
from prettytable import PrettyTable
try:
    from packaging.version import parse
except ImportError:
    from pip._vendor.packaging.version import parse

pih_is_exsits = importlib.util.find_spec("pih") is not None
if not pih_is_exsits:
    sys.path.append("//pih/facade")
from pih.collection import ActionValue, FieldItem, FieldItemList, FullName, InventoryReportItem, LogCommand, LoginPasswordPair, Mark, MarkDivision, MarkGroup, MarkGroupStatistics, ParamItem, PasswordSettings, Patient, PrinterADInformation, PrinterReport, Result, ServiceRoleItem, TimeTrackingEntity, TimeTrackingResultByDate, TimeTrackingResultByDivision, TimeTrackingResultByPerson, User, UserContainer
from pih.const import CONST, FIELD_NAME_COLLECTION, FIELD_COLLECTION, PASSWORD, PATHS, USER_PROPERTY, LogChannels, LogCommands, LogLevels, ServiceCommandNames, ServiceRoles
from pih.rpc import RPC, Error
from pih.rpc_commnads import RPC_COMMANDS
from pih.tools import DataTools, PathTools, ResultTools, FullNameTool, PasswordTools


class NotImplemented(BaseException):
    pass


class NotFound(BaseException):
    pass


class IncorectInputFile(BaseException):
    pass


class NamePolicy:

    @staticmethod
    def get_first_letter(name: str) -> str:
        from transliterate import translit
        return translit(name[0], "ru", reversed=True).lower()

    @staticmethod
    def convert_to_login(full_name: FullName) -> FullName:
        return FullName(
            NamePolicy.get_first_letter(
                full_name.last_name),
            NamePolicy.get_first_letter(
                full_name.first_name),
            NamePolicy.get_first_letter(full_name.middle_name))

    @staticmethod
    def convert_to_alternative_login(login_list: FullName) -> FullName:
        return FullName(login_list.first_name, login_list.middle_name, login_list.last_name)

    @staticmethod
    def convert_to_reverse_login(login_list: FullName) -> FullName:
        return FullName(login_list.middle_name, login_list.first_name, login_list.last_name)


class PIH:

    def rpc_error_handler(details: str, code: Tuple, command: ServiceCommandNames) -> None:
        #add to new thread
        if not isinstance(command, ServiceCommandNames) or (isinstance(command, ServiceCommandNames) and RPC.get_service_role_by_command_name(command) != ServiceRoles.LOG):
            PIH.MESSAGE.to_system_group_from_debug_bot(
            f"\nPIH version: {PIH.VERSION.local()}\nPiPy version: {PIH.VERSION.remote()}\nUser: {PIH.OS.get_login()}\nComputer: {PIH.OS.get_host()}\n" + details, LogLevels.ERROR)
        raise Error(details, code) from None

    RPC.init(lambda details, code, command: 
        PIH.rpc_error_handler(details, code, command),
        lambda role:
            PIH.SERVICE.get_host(role)
        ,
        lambda role:
            PIH.SERVICE.get_port(role)
    )

    class VERSION:

        @staticmethod
        def local() -> str:
            return "1.40044"

        @staticmethod
        def remote() -> str:
            req = requests.get("https://pypi.python.org/pypi/pih/json")
            version = parse('0')
            if req.status_code == requests.codes.ok:
                data = json.loads(req.text.encode(req.encoding))
                releases = data.get('releases', [])
                for release in releases:
                    ver = parse(release)
                    if not ver.is_prerelease:
                        version = max(version, ver)
            return str(version)
            
    class SERVICE:

        @staticmethod
        def get_host(service_role: ServiceRoles) -> str:
            role_item: ServiceRoleItem = service_role.value
            host: str = role_item.host
            if host is None:
                host = PIH.OS.get_host()
            return host

        @staticmethod
        def get_port(service_role: ServiceRoles) -> str:
            role_item: ServiceRoleItem = service_role.value
            return role_item.port

    class PATH(PATHS):

        @staticmethod
        def resolve(value: str) -> str:
            return PathTools.resolve(value, PIH.OS.get_host())

    class SESSION:

        login:str = None

        @staticmethod
        def get_login() -> str:
            if PIH.SESSION.login is None:
                PIH.SESSION.start(PIH.OS.get_login())
            return PIH.SESSION.login

        @staticmethod
        def start(login:str) -> None:
            PIH.SESSION.login = login

    class OS:

        USE_AUTHENTIFICATION: bool = True

        @staticmethod
        def get_login() -> str:
            return os.getlogin()

        @staticmethod
        def get_host() -> str:
            return platform.node()

    class EVENT:

        @staticmethod
        def call(host: str, port: str, type: int) -> None:
            RPC_COMMANDS.event(host, port, type)

        @staticmethod
        def subscribe(host: str, port: str, type: int) -> bool:
            return RPC_COMMANDS.SCHEDULE.subscribe(host, port, type)

    class FORMAT:
    
        @staticmethod
        def telephone(value: str) -> str:
            value = value.replace("(", "").replace(")", "").replace(" ", "").replace("-", "")
            if len(value) > 0 and (value[0] == "8" or value[0] == "7"):
                value = CONST.PHONE_PREFIX + value[1:]
            return value

        @staticmethod
        def name(value: str) -> str:
            return value[0].upper() + value[1:].lower()

    class FILTER:
    
        @staticmethod
        def users_by_dn(data: List[User], dn: str) -> List:
            return list(filter(lambda x: x.distinguishedName.find(dn) != -1, data))

    class RESULT:

        class INVENTORY:
    
            @staticmethod
            def report(report_file_path: str) -> Result[List[InventoryReportItem]]:
                return DataTools.to_result(
                    RPC_COMMANDS.DOCS.get_inventory_report(report_file_path), InventoryReportItem)

        class TIME_TRACKING:
        
            @staticmethod
            def today(tab_number: str = None) -> Result[List[TimeTrackingResultByPerson]]:
                return PIH.RESULT.TIME_TRACKING.create(tab_number=tab_number)

            @staticmethod
            def in_period(day_start: int = 1, day_end: int = None, month: int = None, tab_number: str = None) -> Result[List[TimeTrackingResultByPerson]]:
                now: datetime = datetime.now()
                if month is not None:
                    now = now.replace(month = month)
                start_date: datetime = now.replace(hour=0, minute=0, second=0)
                end_date: datetime = now.replace(hour=23, minute=59, second=59)
                if day_start < 0:
                    start_date -= timedelta(days=abs(day_start))
                else:
                    start_date = start_date.replace(day=day_start)
                if day_end is not None:
                    if day_end < 0:
                        day_end -= timedelta(days=abs(day_start))
                    else:
                        day_end = start_date.replace(day=day_start)
                return PIH.RESULT.TIME_TRACKING.create(start_date, end_date, tab_number)

            @staticmethod
            def create(start_date: datetime = None, end_date: datetime = None, tab_number: str = None) -> Result[List[TimeTrackingResultByPerson]]:
                now: datetime = datetime.now() if start_date is None or end_date is None else None
                start_date = start_date or now.replace(hour=0, minute=0, second=0)
                end_date = end_date or now.replace(hour=23, minute=59, second=59)
                def get_date_or_time(entity: TimeTrackingEntity, date: bool) -> str:
                    return DataTools.if_not_none(entity, lambda: entity.TimeVal.split("T")[not date])
                result_data: dict = {}
                full_name_by_tab_number_map: dict = {}
                result_data = defaultdict(
                    lambda: defaultdict(lambda: defaultdict(list)))
                for time_tracking_entity in DataTools.to_result(
                    RPC_COMMANDS.MARK.get_time_tracking(start_date, end_date, tab_number), TimeTrackingEntity).data:
                    tab_number: str = time_tracking_entity.TabNumber
                    full_name_by_tab_number_map[tab_number] = time_tracking_entity.FullName
                    result_data[time_tracking_entity.DivisionName][tab_number][get_date_or_time(time_tracking_entity, True)].append(
                        time_tracking_entity)
                result: List[TimeTrackingResultByDivision] = []
                for division_name in result_data:
                    result_division_item: TimeTrackingResultByDivision = TimeTrackingResultByDivision(division_name)
                    result.append(result_division_item)
                    for tab_number in result_data[division_name]:
                        result_person_item: TimeTrackingResultByPerson = TimeTrackingResultByPerson(tab_number, full_name_by_tab_number_map[tab_number])
                        result_division_item.list.append(result_person_item)
                        for date in result_data[division_name][tab_number]:
                            time_tracking_entity_list: List[TimeTrackingEntity] = result_data[division_name][tab_number][date]
                            time_tracking_entity: TimeTrackingEntity = time_tracking_entity_list[0]
                            time_tracking_entity2: TimeTrackingEntity = None
                            if len(time_tracking_entity_list) > 1:
                                time_tracking_entity2 = time_tracking_entity_list[len(time_tracking_entity_list) - 1]
                            time_tracking_start_entity: TimeTrackingEntity = None
                            time_tracking_end_entity: TimeTrackingEntity = None
                            if time_tracking_entity.Mode == 1:
                                time_tracking_start_entity = time_tracking_entity
                            if time_tracking_entity.Mode == 2:
                                time_tracking_end_entity = time_tracking_entity
                            if time_tracking_entity2 is not None:
                                if time_tracking_entity2.Mode == 1:
                                    time_tracking_start_entity = time_tracking_entity2
                                if time_tracking_entity2.Mode == 2:
                                    time_tracking_end_entity = time_tracking_entity2
                            duration: str = "0"
                            if time_tracking_start_entity is not None:
                                if time_tracking_end_entity is not None: 
                                    duration_int: int = (datetime.fromisoformat(
                                        time_tracking_end_entity.TimeVal) - datetime.fromisoformat(time_tracking_start_entity.TimeVal)).seconds//3600
                                    duration = str(duration_int)
                                    result_person_item.duration += duration_int
                            result_person_item.list.append(
                                TimeTrackingResultByDate(date, get_date_or_time(time_tracking_start_entity, False), 
                                                         get_date_or_time(time_tracking_end_entity, False), duration))
                return Result(FIELD_COLLECTION.ORION.TIME_TRACKING_RESULT, result)

        class EXTRACT:

            @staticmethod
            def parameter(object: dict, name: str) -> str:
                return object[name] if name in object else ""

            @staticmethod
            def tab_number(mark_object: dict) -> str:
                return PIH.RESULT.EXTRACT.parameter(mark_object, FIELD_NAME_COLLECTION.TAB_NUMBER)

            @staticmethod
            def telephone(user_object: dict) -> str:
                return PIH.RESULT.EXTRACT.parameter(user_object, FIELD_NAME_COLLECTION.TELEPHONE)

            @staticmethod
            def login(user_object: dict) -> str:
                return PIH.RESULT.EXTRACT.parameter(user_object, FIELD_NAME_COLLECTION.LOGIN)

            @staticmethod
            def name(mark_object: dict) -> str:
                return PIH.RESULT.EXTRACT.parameter(mark_object, FIELD_NAME_COLLECTION.NAME)

            @staticmethod
            def dn(user_object: dict) -> str:
                return PIH.RESULT.EXTRACT.parameter(user_object, FIELD_NAME_COLLECTION.DN)

            @staticmethod
            def group_name(mark_object: dict) -> str:
                return PIH.RESULT.EXTRACT.parameter(mark_object, FIELD_NAME_COLLECTION.GROUP_NAME)

            @staticmethod
            def as_full_name(mark_object: dict) -> FullName:
                return FullNameTool.from_string(PIH.RESULT.EXTRACT.full_name(mark_object))

            @staticmethod
            def full_name(mark_object: dict) -> str:
                return PIH.RESULT.EXTRACT.parameter(mark_object, FIELD_NAME_COLLECTION.FULL_NAME)

            @staticmethod
            def person_id(mark_object: dict) -> str:
                return PIH.RESULT.EXTRACT.parameter(mark_object, FIELD_NAME_COLLECTION.PERSON_ID)

            @staticmethod
            def mark_id(mark_object: dict) -> str:
                return PIH.RESULT.EXTRACT.parameter(mark_object, FIELD_NAME_COLLECTION.MARK_ID)

            @staticmethod
            def description(object: dict) -> str:
                result = PIH.RESULT.EXTRACT.parameter(
                    object, FIELD_NAME_COLLECTION.DESCRIPTION)
                if isinstance(result, Tuple) or isinstance(result, List):
                    return result[0]

            @staticmethod
            def container_dn(user_object: dict) -> str:
                return PIH.RESULT.EXTRACT.container_dn_from_dn(PIH.RESULT.EXTRACT.dn(user_object))

            @staticmethod
            def container_dn_from_dn(dn: str) -> str:
                return ",".join(dn.split(",")[1:])

        class PRINTER:

            @staticmethod
            def list() -> Result[List[PrinterADInformation]]:
                def filter_by_server_name(printer_list: List[PrinterADInformation]) -> List[PrinterADInformation]:
                    return list(filter(lambda item: item.serverName == CONST.HOST.PRINTER_SERVER.NAME(), printer_list))
                result: Result[List[PrinterADInformation]] = DataTools.to_result(
                    RPC_COMMANDS.AD.printer_list(), PrinterADInformation)
                return Result(result.fields, filter_by_server_name(result.data))
    
            @staticmethod
            def report(redirect_to_log: bool = True) -> Result[List[PrinterReport]]:
                return DataTools.to_result(RPC_COMMANDS.PRINTER.report(redirect_to_log), PrinterReport)

            @staticmethod
            def status(redirect_to_log: bool = True) -> Result[List[PrinterReport]]:
                return DataTools.to_result(RPC_COMMANDS.PRINTER.status(redirect_to_log), PrinterReport)

        class MARK:

            @staticmethod
            def by_tab_number(value: str) -> Result[Mark]:
                return DataTools.to_result(RPC_COMMANDS.MARK.get_by_tab_number(value), Mark, True)

            @staticmethod
            def person_divisions() -> Result[List[Mark]]:
                return DataTools.to_result(RPC_COMMANDS.MARK.get_person_divisions(), MarkDivision)

            @staticmethod
            def by_name(value: str, first_item: bool = False) -> Result[List[Mark]]:
                return DataTools.to_result(RPC_COMMANDS.MARK.get_by_person_name(value), Mark, first_item)

            @staticmethod
            def by_any(value: str) -> Result[List[Mark]]:
                if PIH.CHECK.tab_number(value):
                    return PIH.RESULT.MARK.by_tab_number(value)
                elif PIH.CHECK.name(value, True):
                    return PIH.RESULT.MARK.by_name(value)
                return Result(None, None)

            @staticmethod
            def free_list() -> Result[Mark]:
                return DataTools.to_result(RPC_COMMANDS.MARK.get_free_marks(), Mark)

            @staticmethod
            def free_marks_by_group_id(value: int) -> Result[Mark]:
                return DataTools.to_result(RPC_COMMANDS.MARK.get_free_marks_by_group_id(value), Mark)

            @staticmethod
            def free_marks_group_statistics() -> Result[MarkGroupStatistics]:
                return DataTools.to_result(RPC_COMMANDS.MARK.get_free_marks_group_statistics(), MarkGroupStatistics)

            @staticmethod
            def all() -> Result[List[Mark]]:
                return DataTools.to_result(RPC_COMMANDS.MARK.get_all(), Mark)

        class POLIBASE:

            @staticmethod
            def patient_by_pin(value: int) -> Result[Patient]:
                return DataTools.to_result(RPC_COMMANDS.POLIBASE.get_patient_by_pin(value), Patient)

        class USER:

            @staticmethod
            def by_login(value: str, first_item: bool = False) -> Result[List[User]]:
                return DataTools.to_result(
                    RPC_COMMANDS.USER.get_user_by_login(value), User, first_item)

            @staticmethod
            def by_any(value: Any) -> Result[List[User]]:
                if isinstance(value, FullName):
                    return PIH.RESULT.USER.by_full_name(value)
                else:
                    if PIH.CHECK.login(value):
                        return PIH.RESULT.USER.by_login(value)
                    elif PIH.CHECK.name(value):
                        return PIH.RESULT.USER.by_name(value)
                
            @staticmethod
            def by_job_position(job_position: CONST.AD.JobPositions) -> Result[List[User]]:
                return DataTools.to_result(RPC_COMMANDS.USER.get_users_by_job_position(job_position), User)

            @staticmethod
            def by_group(group: CONST.AD.Groups) -> Result[List[User]]:
                return DataTools.to_result(RPC_COMMANDS.USER.get_users_in_group(group), User)

            @staticmethod
            def template_list() -> Result[List[User]]:
                return DataTools.to_result(RPC_COMMANDS.USER.get_template_list(), User)

            @staticmethod
            def containers() -> Result[List[UserContainer]]:
                return DataTools.to_result(RPC_COMMANDS.USER.get_containers(), UserContainer)

            @staticmethod
            def by_full_name(value: FullName) -> Result[List[User]]:
                return DataTools.to_result(RPC_COMMANDS.USER.get_user_by_full_name(value), User)

            @staticmethod
            def by_name(value: str) -> Result[List[User]]:
                return DataTools.to_result(RPC_COMMANDS.USER.get_users_by_name(value), User)

            @staticmethod
            def active_by_name(value: str) -> Result[List[User]]:
                return DataTools.to_result(RPC_COMMANDS.USER.get_active_users_by_name(value), User)

            @staticmethod
            def in_group(value: CONST.AD.Groups) -> Result[List[User]]:
                return DataTools.to_result(RPC_COMMANDS.USER.get_users_in_group(value), User)

            @staticmethod
            def all() -> Result[List[User]]:
                return PIH.RESULT.USER.by_name(CONST.AD.SEARCH_ALL_PATTERN)

            @staticmethod
            def all_active() -> Result[List[User]]:
                return PIH.RESULT.USER.active_by_name(CONST.AD.SEARCH_ALL_PATTERN)

            @staticmethod
            def by_tab_number(value: str) -> Result[User]:
                mark: Mark = PIH.RESULT.MARK.by_tab_number(value).data
                return Result(FIELD_COLLECTION.AD.USER, DataTools.if_check(mark, lambda: DataTools.get_first(PIH.RESULT.USER.by_full_name(FullNameTool.from_string(mark.FullName)).data)))

    class INPUT:

        @staticmethod
        def input(caption: str = None) -> str:
            try:
                return input() if caption is None else input(caption)
            except KeyboardInterrupt:
                raise KeyboardInterrupt()

        @staticmethod
        def telephone(format: bool = True, telephone_prefix: str = CONST.PHONE_PREFIX) -> str:
            while True:
                PR.input("Номер телефона")
                use_telephone_prefix: bool = telephone_prefix is not None
                telephone = PIH.INPUT.input(telephone_prefix if use_telephone_prefix else "")
                if use_telephone_prefix:
                    telephone = telephone_prefix + telephone
                check: bool = None
                if format:
                    telehone_fixed = PIH.FORMAT.telephone(telephone)
                    check = PIH.CHECK.telephone(telehone_fixed)
                    if check and telehone_fixed != telephone:
                        telephone = telehone_fixed
                        PR.value("Телефон отформатирован:", telephone)
                if check or PIH.CHECK.telephone(telephone):
                    return telephone
                else:
                    PR.red("Неверный формат номера телефона!")

        @staticmethod
        def email() -> str:
            while True:
                PR.input("Электронная почта")
                email = PIH.INPUT.input()
                if PIH.CHECK.email(email):
                    return email
                else:
                    PR.red("Неверный формат электронной почты!")

        @staticmethod
        def message() -> str:
            PR.input("Сообщение")
            return PIH.INPUT.input()       

        @staticmethod
        def description() -> str:
            PR.input("Введите описание")
            return PIH.INPUT.input()

        @staticmethod
        def login(check_on_exsits: bool = False):
            while True:
                PR.input("Введите логин")
                login = PIH.INPUT.input()
                if PIH.CHECK.login(login):
                    if check_on_exsits and PIH.CHECK.USER.is_exists_by_login(login):
                        PR.red("Логин занят!")
                    else:
                        return login
                else:
                    PR.red("Неверный формат логина!")

        @staticmethod
        def indexed_list(caption: str, name_list: List[Any], caption_list: List[str], by_index: bool = False) -> str:
            return PIH.INPUT.item_by_index(caption, name_list, lambda item, index: caption_list[index if by_index else item])

        @staticmethod
        def indexed_field_list(caption: str, list: FieldItemList) -> str:
            name_list = list.get_name_list()
            return PIH.INPUT.item_by_index(caption, name_list, lambda item, _: list.get_item_by_name(item).caption)

        @staticmethod
        def index(caption: str, data: dict, item_label: Callable = None) -> int:
            selected_index = -1
            length = len(data)
            while True:
                if item_label:
                    for index, item in enumerate(data):
                        PR.index(index + 1, item_label(item, index))
                if length == 1:
                    return 0
                selected_index = PIH.INPUT.input(PR.input_str(caption + f" (от 1 до {length})", "", ":"))
                if selected_index == "":
                    selected_index = 1
                try:
                    selected_index = int(selected_index) - 1
                    if selected_index >= 0 and selected_index < length:
                        return selected_index
                except ValueError:
                    continue

        @staticmethod
        def item_by_index(caption: str, data: List[Any], item_label: Callable = None) -> dict:
            return data[PIH.INPUT.index(caption, data, item_label)]

        @staticmethod
        def tab_number(check: bool = True) -> str:
            tab_number: str = None
            while True:
                PR.input("Введите табельный номер:")
                tab_number = PIH.INPUT.input()
                if check:
                    if PIH.CHECK.tab_number(tab_number):
                        return tab_number
                    else:
                        PR.red("Wrong tab number")
                        return tab_number
                else:
                    return tab_number

        @staticmethod
        def password(secret: bool = True, check: bool = False, settings: PasswordSettings = None) -> str:
            PR.input("Введите новый пароль:")
            while True:
                value = getpass(" ") if secret else PIH.INPUT.input()
                if not check or PIH.CHECK.password(value, settings):
                    return value
                else:
                    PR.red("Пароль не соответствует требованием безопасности")

        @staticmethod
        def same_if_empty(caption: str, src_value: str) -> str:
            value = PIH.INPUT.input(caption)
            if value == "":
                value = src_value
            return value


        @staticmethod
        def name() -> str:
            return PIH.INPUT.input(PR.input("Введите часть имени:"))

        @staticmethod
        def full_name() -> FullName:
            def full_name_part(caption: str) -> str:
                while(True):
                    value: str = PIH.INPUT.input(PR.input(caption))
                    value = value.strip()
                    if PIH.CHECK.name(value):
                        return PIH.FORMAT.name(value)
                    else:
                        pass
            full_name: FullName = FullName()
            full_name.last_name = full_name_part("Введите фамилию")
            full_name.first_name = full_name_part("Введите имя")
            full_name.middle_name = full_name_part("Введите отчество")
            return full_name

        @staticmethod
        def yes_no(text: str = " ", enter_for_yes: bool = False) -> bool:
            answer = PIH.INPUT.input(f"{PR.blue_str(text)} \n{PR.green_str('Да (1 или Ввод)')} {PR.red_str('Нет (Остальное)')}:" if enter_for_yes else
                                     f"{PR.blue_str(text)} \n{PR.red_str('Да (1)')} {PR.green_str('Нет (Остальное или Ввод)')}:")
            answer = answer.lower()
            return answer == "y" or answer == "yes" or answer == "1" or (answer == "" and enter_for_yes)

        class USER:

            @staticmethod
            def container() -> UserContainer:
                result: Result = PIH.RESULT.USER.containers()
                data = result.data
                PIH.VISUAL.containers_for_result(result, True)
                return PIH.INPUT.item_by_index("Выберите контейнер пользователя, введя индекс", data)

            @staticmethod
            def template() -> dict:
                result = PIH.RESULT.USER.template_list()
                data = result.data
                PIH.VISUAL.template_users_for_result(result, True)
                return PIH.INPUT.item_by_index("Выберите шаблон пользователя, введя индекс", data)

            @staticmethod
            def search_attribute() -> str:
                return PIH.INPUT.indexed_field_list("Выберите по какому критерию искать, введя индекс",
                    FIELD_COLLECTION.AD.SEARCH_ATTRIBUTE)

            @staticmethod
            def search_value(search_attribute: str) -> str:
                field_item = FIELD_COLLECTION.AD.SEARCH_ATTRIBUTE.get_item_by_name(
                    search_attribute)
                return PIH.INPUT.input(PR.input(f"Введите {field_item.caption.lower()}:"))
            
        class MARK:

            @staticmethod
            def free(group: MarkGroup = None) -> Mark:
                while True:
                    if group is None:
                        if PIH.INPUT.yes_no("Выбрать группы доступа для карты доступа, введя имени пользователя из этой группы?"):
                            result = PIH.RESULT.MARK.by_name(
                                PIH.INPUT.name())
                            mark_list: List[Mark] = result.data
                            length = len(mark_list)
                            if length > 0:
                                if length > 1:
                                    PIH.VISUAL.table_with_caption_first_title_is_centered(
                                        result, "Найденные пользователи:", True)
                                group = PIH.INPUT.item_by_index(
                                    "Выберите группу доступа", mark_list)
                            else:
                                PR.red("Пользователь с введенным именем не найден")
                        else:
                            result = PIH.RESULT.MARK.free_marks_group_statistics()
                            data = result.data
                            length = len(data)
                            if length > 0:
                                if length > 1:
                                    PIH.VISUAL.free_marks_group_statistics_for_result(
                                        result, True)
                                group = PIH.INPUT.item_by_index(
                                    "Выберите группу доступа введя индекс", data)
                            else:
                                PR.red("Свободный карт доступа нет!")
                                return None
                    if group is not None:
                        result = PIH.RESULT.MARK.free_marks_by_group_id(group.GroupID)
                        data = result.data
                        length = len(data)
                        if length > 0:
                            if length > 1:
                                PIH.VISUAL.free_marks_by_group_for_result(
                                    group, result, True)
                            return PIH.INPUT.item_by_index(
                                "Выберите карту доступа введя индекс", data)
                        else:
                            PR.red(
                                f"Нет свободных карт для группы доступа '{group.GroupName}'!")
                            return None
                    else:
                        pass
            
            @staticmethod
            def person_division() -> MarkDivision:
                division_list: List[MarkDivision] = PIH.RESULT.MARK.person_divisions(
                ).data
                return PIH.INPUT.item_by_index("Выберите подразделение для персоны, которой принадлежит карта доступа", division_list, lambda item, _: item.name)


            @staticmethod
            def by_name() -> Mark:
                PR.head2("Введите имя персоны:")
                result = PIH.RESULT.MARK.by_name(PIH.INPUT.name())
                PIH.VISUAL.marks_for_result(result, "Карты доступа", True)
                return PIH.INPUT.item_by_index("Выберите карточку, введя индекс", result.data)


        @staticmethod
        def message_for_user_by_login(login: str) -> str:
            user = ResultTools.get_first(
                PIH.RESULT.USER.by_login(login))
            if user is not None:
                head_string = f"Здравствуйте, {PIH.RESULT.EXTRACT.name(user)}, "
                PR.green(head_string)
                message = PIH.INPUT.input(PR.blue_str("Enter message: "))
                return head_string + message
            else:
                pass

        @staticmethod
        def container_dn_or_template_user_container_dn() -> str:
            container_type = PIH.INPUT.indexed_field_list(
                "Choose type of container:", FIELD_COLLECTION.AD.CONTAINER_TYPE)
            if container_type == FIELD_NAME_COLLECTION.TEMPLATE_USER_CONTAINER:
                return PIH.RESULT.EXTRACT.container_dn(PIH.INPUT.template_user())
            else:
                return PIH.RESULT.EXTRACT.dn(PIH.INPUT.container())

    class CHECK:

        class RIGTH:
    
            @staticmethod
            def by_group(group: CONST.AD.Groups) -> bool:
                user_list: List[User] = PIH.RESULT.USER.in_group(group).data
                if user_list is not None:
                    for user in user_list:
                        if user.samAccountName == PIH.SESSION.get_login():
                            return True
                return False

        class USER:

            @staticmethod
            def is_exists_by_login(value: str) -> bool:
                return RPC_COMMANDS.USER.user_is_exsits_by_login(value)

            @staticmethod
            def is_user(user: User) -> bool:
                 return PIH.CHECK.full_name(user.name)

            @staticmethod
            def is_acive(user: User) -> bool:
                 return user.distinguishedName.find(CONST.AD.ACTIVE_USERS_CONTAINER_DN) != -1

            @staticmethod
            def is_exists_by_full_name(full_name: FullName) -> bool:
                return ResultTools.data_is_empty(PIH.RESULT.USER.by_full_name(full_name))

            @staticmethod
            def search_attribute(value: str) -> bool:
                return value in CONST.AD.SEARCH_ATTRIBUTES

            @staticmethod
            def property(value: str) -> str:
                if value == "":
                    return USER_PROPERTY.USER_STATUS
                return value

        class MARK:

            @staticmethod
            def is_free(tab_number: str) -> bool:
                return RPC_COMMANDS.MARK.is_mark_free(tab_number)

            @staticmethod
            def is_exists_by_full_name(full_name: FullName) -> bool:
                result: Result[List[Mark]] = PIH.RESULT.MARK.by_name(
                    FullNameTool.to_string(full_name))
                return ResultTools.data_is_empty(result)

        class TIME_TRACKING:

            @staticmethod
            def available() -> bool:
                return PIH.CHECK.RIGTH.by_group(CONST.AD.Groups.TimeTrackingReport)

        class INVENTORY:

            @staticmethod
            def file_is_report(file_path: str) -> bool:
                return DataTools.rpc_unrepresent(RPC_COMMANDS.DOCS.is_inventory_report(file_path))

            @staticmethod
            def available() -> bool:
                return PIH.CHECK.RIGTH.by_group(CONST.AD.Groups.Inventory)

        @staticmethod
        def tab_number(value: str) -> bool:
            return re.fullmatch(r"[0-9]+", value) is not None

        @staticmethod
        def login(value: str) -> bool:
            pattern = r"([a-z]{" + \
                str(CONST.NAME_POLICY.PART_ITEM_MIN_LENGTH) + ",}[0-9]*)"
            return re.fullmatch(pattern, value) is not None

        @staticmethod
        def telephone(value: str) -> bool:
            return value is not None and re.fullmatch(r"^\+[0-9]{11,13}$", value) is not None

        @staticmethod
        def email(value: str) -> bool:
            return re.fullmatch(r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+", value) is not None

        @staticmethod
        def name(value: str, use_space: bool = False) -> bool:
            pattern = r"[а-яА-ЯёЁ" + (" " if use_space else "") + "]{" + str(CONST.NAME_POLICY.PART_ITEM_MIN_LENGTH) + ",}$"
            return re.fullmatch(pattern, value) is not None

        @staticmethod
        def full_name(value: str) -> bool:
            pattern = r"[а-яА-ЯёЁ]{" + str(CONST.NAME_POLICY.PART_ITEM_MIN_LENGTH) + ",} [а-яА-ЯёЁ]{" + str(CONST.NAME_POLICY.PART_ITEM_MIN_LENGTH) +",} [а-яА-ЯёЁ]{" + str(CONST.NAME_POLICY.PART_ITEM_MIN_LENGTH) + ",}$"
            return re.fullmatch(pattern, value) is not None

        @staticmethod
        def password(value: str, settings: PasswordSettings = None) -> bool:
            settings = settings or PASSWORD.SETTINGS.DEFAULT
            return PasswordTools.check_password(value, settings.length, settings.special_characters)

        @staticmethod
        def ping(host: str) -> bool:
            command = ['ping', "-n", '1', host]
            response = subprocess.call(command)
            return response == 0

    @staticmethod
    def log(message: str, channel: LogChannels = LogChannels.DEFAULT, level: Any = LogLevels.DEFAULT) -> Any:
        try:
            level_value: int = None
            level_list: List[LogLevels] = None
            if isinstance(level, LogLevels) :
                level_list = [level]
            if isinstance(level, int):
                level_value = level
            if level_value is None:
                level_value = 0
                for level_item in level_list:
                    level_value = level_value | level_item.value
            return RPC_COMMANDS.LOG.log(message, channel, level_value)
        except Error as error:
            print("Log send error")
        
    @staticmethod
    def log_command(command_name: LogCommands, parameters:Tuple = None) -> bool:
        try:
            log_commnad: LogCommand = LogCommands._member_map_[command_name.name].value[0]
            parameter_pattern_list: List = log_commnad.params
            parameter_dict: dict = {}
            index: int = 0
            if len(parameter_pattern_list) > len(parameters):
                raise Exception("Income parameter list length is less that parameter list length of command") 
            for index, parameter_pattern_item in enumerate(parameter_pattern_list):
                parameter_pattern: ParamItem = parameter_pattern_item
                parameter_dict[parameter_pattern.name] = parameters[index]
            return RPC_COMMANDS.LOG.command(command_name.name, parameter_dict)
        except Error as error:
            print("Log send error")

    class MESSAGE:

        class WHATS_APP:
    
            @staticmethod
            def send_message(phone_number: str, message: str) -> bool:
                import pywhatkit as pwk
                try:
                    pwk.sendwhatmsg_instantly(phone_number, message)
                except:
                    pass

            @staticmethod
            def send_message_by_login(login: str, message: str) -> bool:
                user = ResultTools.get_first(
                    PIH.RESULT.USER.by_login(login))
                if user:
                    PIH.MESSAGE.WHATS_APP.send_message(
                        PIH.RESULT.EXTRACT.telephone(user), message)
                else:
                    return False

        class COMMAND:
    
            @staticmethod
            def login() -> bool:
                return PIH.log_command(LogCommands.LOG_IN, (PIH.SESSION.get_login(), PIH.OS.get_host()))

            @staticmethod
            def hr_notify_about_new_employee(login: User) -> bool:
                user: User = PIH.RESULT.USER.by_login(login)
                hr_user: User = ResultTools.get_first(PIH.RESULT.USER.by_job_position(CONST.AD.JobPositions.HR))
                return PIH.log_command(LogCommands.HR_NOTIFY_ABOUT_NEW_EMPLOYEE, (FullNameTool.to_given_name(FullNameTool.from_string(hr_user.name)), 
                                                                                    user.name, user.mail))

            @staticmethod
            def it_notify_about_new_user(login: str, password: str) -> bool:
                it_user_list: List[User] = PIH.RESULT.USER.by_job_position(
                    CONST.AD.JobPositions.IT).data
                me_user_login: str = PIH.SESSION.get_login()
                it_user_list = list(filter(lambda user: user.samAccountName != me_user_login, it_user_list))
                it_user: User = it_user_list[0]
                user: User = PIH.RESULT.USER.by_login(login, True).data
                mark: Mark = PIH.RESULT.MARK.by_name(user.name, True).data
                return PIH.log_command(LogCommands.IT_NOTIFY_ABOUT_NEW_USER, (user.name, user.description, user.samAccountName, password, user.telephoneNumber, user.mail, mark.TabNumber)) and \
                    PIH.log_command(LogCommands.IT_TASK_AFTER_CREATE_NEW_USER, (FullNameTool.to_given_name(FullNameTool.from_string(it_user.name)), user.name, user.mail, password))

            @staticmethod
            def printer_report(name: str, location: str, report: str) -> bool:
                return PIH.log_command(LogCommands.PRINTER_REPORT, (name, location, report))


        @staticmethod
        def to_debug_bot(message: str, level: Any = LogLevels.DEFAULT) -> Any:
            return PIH.log(message, LogChannels.DEBUG_BOT, level)

        @staticmethod
        def to_system_group_from_debug_bot(message: str, level: Any = LogLevels.DEFAULT) -> Any:
            return PIH.log(message, LogChannels.DEBUG, level)

        @staticmethod
        def to_system_group_from_system_bot(message: str, level: Any = LogLevels.DEFAULT) -> Any:
            return PIH.log(message, LogChannels.SYSTEM, level)

        @staticmethod
        def backup(message: str, level: Any = LogLevels.DEFAULT) -> Any:
            return PIH.log(message, LogChannels.BACKUP, level)

        @staticmethod
        def notification(message: str, level: Any = LogLevels.DEFAULT) -> Any:
            return PIH.log(message, LogChannels.NOTIFICATION, level)

        @staticmethod
        def to_it_group_from_printer_bot(message: str, level: Any = LogLevels.DEFAULT) -> Any:
            return PIH.log(message, LogChannels.PRINTER, level)

        @staticmethod
        def to_printer_bot(message: str, level: Any = LogLevels.DEFAULT) -> Any:
            return PIH.log(message, LogChannels.PRINTER_BOT, level)

        @staticmethod
        def to_it_group_from_it_bot(message: str, level: Any = LogLevels.DEFAULT) -> Any:
            return PIH.log(message, LogChannels.IT, level)

        @staticmethod
        def to_it_bot(message: str, level: Any = LogLevels.DEFAULT) -> Any:
            return PIH.log(message, LogChannels.IT_BOT, level)


    class VISUAL:

        @staticmethod
        def init() -> None:
            PR.init()

        @staticmethod
        def clear_screen():
            os.system('cls' if os.name == 'nt' else 'clear')

        @staticmethod
        def pih_title() -> None:
            PR.cyan(
                "█▀█ ▄▀█ █▀▀ █ █▀▀ █ █▀▀   █ █▄░█ ▀█▀ █▀▀ █▀█ █▄░█ ▄▀█ ▀█▀ █ █▀█ █▄░█ ▄▀█ █░░   █░█ █▀█ █▀ █▀█ █ ▀█▀ ▄▀█ █░░")
            PR.cyan(
                "█▀▀ █▀█ █▄▄ █ █▀░ █ █▄▄   █ █░▀█ ░█░ ██▄ █▀▄ █░▀█ █▀█ ░█░ █ █▄█ █░▀█ █▀█ █▄▄   █▀█ █▄█ ▄█ █▀▀ █ ░█░ █▀█ █▄▄")
            print(f"Версия: {PIH.VERSION.local()}")


        class MARK:

            @staticmethod
            def by_any(value: str) -> None:
                PIH.VISUAL.marks_for_result(
                    PIH.RESULT.MARK.by_any(value), "Mark by tab number:")

        @staticmethod
        def rpc_service_header(service_host: str, service_port: int, service_name: str) -> None:
            PR.blue("PIH")
            PR.blue(f"Version: {PIH.VERSION.local()}")
            PR.blue(f"PyPi Version: {PIH.VERSION.remote()}")
            PR.green(f"Service host: {service_host}")
            PR.green(f"Service port: {service_port}")
            PR.green(f"Service name: {service_name}")

        @staticmethod
        def free_marks(use_index: bool = False) -> None:
            PIH.VISUAL.table_with_caption_first_title_is_centered(
                PIH.RESULT.MARK.free_list(), "Free marks:", use_index)

        @staticmethod
        def marks_for_result(result: Result, caption: str, use_index: bool = False) -> None:
            PIH.VISUAL.table_with_caption_first_title_is_centered(
                result, caption, use_index)

        @staticmethod
        def free_marks_group_statistics(use_index: bool = False) -> None:
            PIH.VISUAL.free_marks_group_statistics_for_result(
                PIH.RESULT.MARK.free_marks_group_statistics(), use_index)

        @staticmethod
        def free_marks_by_group(group: dict, use_index: bool = False) -> None:
            PIH.VISUAL.free_marks_by_group_for_result(
                PIH.RESULT.MARK.free_marks_by_group_id(group), group, use_index)

        @staticmethod
        def free_marks_group_statistics_for_result(result: Result, use_index: bool) -> None:
            PIH.VISUAL.table_with_caption_last_title_is_centered(
                result, "Свободные карты доступа:", use_index)

        @staticmethod
        def free_marks_by_group_for_result(group: MarkGroup, result: Result, use_index: bool) -> None:
            group_name = group.GroupName
            PIH.VISUAL.table_with_caption_last_title_is_centered(
                result, f"Свободные карты доступа для группы доступа '{group_name}':", use_index)

        @staticmethod
        def containers_for_result(result: Result, use_index: bool = False) -> None:
            PIH.VISUAL.table_with_caption(result, "Подразделение:", use_index)

        @staticmethod
        def table_with_caption_first_title_is_centered(result: Result, caption: str, use_index: bool = False, modify_data_handler: Callable = None) -> None:
            def modify_table(table: PrettyTable, caption_list: List[str]):
                table.align[caption_list[int(use_index)]] = "c"
            PIH.VISUAL.table_with_caption(
                result, caption, use_index, modify_table, modify_data_handler)

        @staticmethod
        def table_with_caption_last_title_is_centered(result: Result, caption: str, use_index: bool = False, modify_data_handler: Callable = None) -> None:
            def modify_table(table: PrettyTable, caption_list: List[str]):
                table.align[caption_list[-1]] = "c"
            PIH.VISUAL.table_with_caption(
                result, caption, use_index, modify_table, modify_data_handler)

        @staticmethod
        def table_with_caption(result: Any, caption: str = None, use_index: bool = False, modify_table_handler: Callable = None, modify_data_handler: Callable = None) -> None:
            if caption is not None:
                PR.cyan(caption)
            is_result_type = isinstance(result, Result)
            field_list = result.fields if is_result_type else result["fields"]
            data = result.data if is_result_type else result["data"]
            if DataTools.is_empty(data):
                PR.red("Not found!")
            else:
                if not isinstance(data, list):
                    data = [data]
                if use_index:
                    field_list.list.insert(0, FIELD_COLLECTION.INDEX)
                caption_list: List = field_list.get_caption_list()
                def create_table(caption_list: List[str]) -> PrettyTable:
                    table: PrettyTable = PrettyTable(caption_list)
                    table.align = "l"
                    if use_index:
                        table.align[caption_list[0]] = "c"
                    return table
                table: PrettyTable = create_table(caption_list)
                if modify_table_handler is not None:
                    modify_table_handler(table, caption_list)
                for index, item in enumerate(data):
                    row_data: List = []
                    for field_item_obj in field_list.get_list():
                        field_item: FieldItem = field_item_obj
                        if field_item.visible:
                            if field_item.name == FIELD_COLLECTION.INDEX.name:
                                row_data.append(str(index + 1))
                            elif not isinstance(item, dict):
                                item_data = getattr(item, field_item.name)
                                if modify_data_handler is not None:
                                    modify_item_data = modify_data_handler(
                                        field_item, item)
                                    row_data.append(DataTools.if_check(
                                        item_data, lambda: item_data, "") if modify_item_data is None else modify_item_data)
                                else:
                                    row_data.append(DataTools.if_check(item_data, lambda: item_data, ""))
                            elif field_item.name in item:
                                item_data = item[field_item.name]
                                if modify_data_handler is not None:
                                    modify_item_data = modify_data_handler(
                                        field_item, item)
                                    row_data.append(
                                        item_data if modify_item_data is None else modify_item_data)
                                else:
                                    row_data.append(item_data)
                    table.add_row(row_data)
                print(table)
                table.clear()

        @staticmethod
        def template_users_for_result(data: dict, use_index: bool = False) -> None:
            def data_handler(field_item: FieldItem, item: User) -> Any:
                filed_name = field_item.name
                if filed_name == FIELD_NAME_COLLECTION.DESCRIPTION:
                    return DataTools.get_first(item.description)
                return None
            PIH.VISUAL.table_with_caption(
                data, "Шаблоны для создания аккаунта пользователя:", use_index, None, data_handler)

    class ACTION:

        class USER:

            @staticmethod
            def create_from_template(container_dn: str,
                                          full_name: FullName, login: str, password: str, description: str, telephone: str, email: str) -> bool:
                return RPC_COMMANDS.USER.create_from_template(
                    container_dn, full_name, login, password, description, telephone, email)

            @staticmethod
            def create_in_container(container_dn: str,
                                         full_name: FullName, login: str, password: str, description: str, telephone: str, email: str) -> bool:
                return RPC_COMMANDS.USER.create_in_container(
                    container_dn, full_name, login, password, description, telephone, email)

            @staticmethod
            def set_telephone(user: User, telephone: str) -> bool:
                return RPC_COMMANDS.USER.set_telephone(user.distinguishedName, telephone)

            @staticmethod
            def set_password(user: User, password: str) -> bool:
                return RPC_COMMANDS.USER.set_password(user.distinguishedName, password)

            @staticmethod
            def set_status(user: User, status: str, container: UserContainer) -> bool:
                return RPC_COMMANDS.USER.set_status(user.distinguishedName, status, DataTools.if_check(container, lambda: container.distinguishedName))

            @staticmethod
            def remove(user: User) -> bool:
                return RPC_COMMANDS.USER.user_remove(user.distinguishedName)

            @staticmethod
            def authenticate() -> bool:
                if PIH.OS.USE_AUTHENTIFICATION:
                    PR.head1("Аутентификация пользователя")
                    login = PIH.OS.get_login()
                    if not PIH.INPUT.yes_no(f"Использовать пользователя: {login}?", True):
                        login = PIH.INPUT.login()
                    PR.input("Введите пароль:")
                    password = getpass("")
                    if RPC_COMMANDS.USER.authenticate(login, password):
                        PIH.SESSION.start(login)
                        PIH.MESSAGE.COMMAND.login()
                        PR.good(
                            f"Добро пожаловать {PIH.RESULT.USER.by_login(login, True).data.name}...")
                        return True
                    else:
                        PR.alert("Неверный пароль или логин. До свидания...")
                        return False

        class TIME_TRACKING:

            @staticmethod
            def report(path: str, start_date: datetime, end_date: datetime, tab_number: str = None) -> bool:
                start_date = datetime.now().replace(hour = 0, minute=0, day=start_date.day, second=0, month=start_date.month, year=start_date.year)
                end_date = datetime.now().replace(hour=23, minute=59, second=0, day=end_date.day,
                                                  month=end_date.month, year=end_date.year)
                return DataTools.rpc_unrepresent(RPC_COMMANDS.DOCS.create_time_tracking_report(PIH.PATH.resolve(path), start_date, end_date, tab_number))
        
        class INVENTORY:

            @staticmethod
            def create_barcodes(report_file_path: str, result_directory: str) -> bool:
                return DataTools.rpc_unrepresent(RPC_COMMANDS.DOCS.create_inventory_barcodes(report_file_path, result_directory))

            @staticmethod
            def save_report_item(report_file_path: str, item: InventoryReportItem) -> bool:
                return DataTools.rpc_unrepresent(RPC_COMMANDS.DOCS.save_report_item(report_file_path, item))

        class PRINTER:
    
            @staticmethod
            def report() -> bool:
                return not ResultTools.data_is_empty(PIH.RESULT.PRINTER.report())

            @staticmethod
            def status() -> bool:
                return not ResultTools.data_is_empty(PIH.RESULT.PRINTER.status())

        class MARK:

            @staticmethod
            def create(full_name: FullName, person_division_id: int,  tab_number: str, telephone: str = None) -> bool:
                return DataTools.rpc_unrepresent(RPC_COMMANDS.MARK.create(full_name, person_division_id, tab_number, telephone))

            @staticmethod
            def set_full_name_by_tab_number(full_name: FullName, tab_number: str) -> bool:
                return DataTools.rpc_unrepresent(RPC_COMMANDS.MARK.set_full_name_by_tab_number(full_name, tab_number))

            @staticmethod
            def set_telephone_by_tab_number(telephone: str, tab_number: str) -> bool:
                return DataTools.rpc_unrepresent(RPC_COMMANDS.MARK.set_telephone_by_tab_number(telephone, tab_number))

            @staticmethod
            def make_as_free_by_tab_number(tab_number: str) -> bool:
                return DataTools.rpc_unrepresent(RPC_COMMANDS.MARK.make_mark_as_free_by_tab_number(tab_number))

            @staticmethod
            def remove(mark: Mark) -> bool:
                return DataTools.rpc_unrepresent(RPC_COMMANDS.MARK.remove_by_tab_number(mark.TabNumber))

        def create_user_document(path: str, full_name: FullName, tab_number: str, pc: LoginPasswordPair, polibase: LoginPasswordPair, email: LoginPasswordPair) -> bool:
            locale.setlocale(locale.LC_ALL, 'ru_RU')
            date_now = datetime.now().date()
            date_now_string = f"{date_now.day} {calendar.month_name[date_now.month]} {date_now.year}"
            return RPC_COMMANDS.DOCS.create_user_document(path, date_now_string, CONST.SITE, CONST.SITE_PROTOCOL + CONST.SITE, CONST.EMAIL_ADDRESS, full_name, tab_number, pc, polibase, email)

        def generate_login(full_name: FullName) -> str:
            login_list: List[str] = []
            inactive_user_list: List[User] = []
            login_is_exists: bool = False
            def show_user_which_login_is_exists_and_return_user_if_it_inactive(login_string: str) -> User:
                user: User = PIH.RESULT.USER.by_login(login_string, True).data
                is_active: bool = PIH.CHECK.USER.is_acive(user)
                PR.alert(f"Логин '{login_string}' занят ({user.name} - {'активный' if is_active else 'неактивный'})")
                return user if not is_active else None
            login: FullName = NamePolicy.convert_to_login(full_name)
            login_string: str = FullNameTool.to_string(login, "")
            login_list.append(login_string)
            if PIH.CHECK.USER.is_exists_by_login(login_string):
                user: User = show_user_which_login_is_exists_and_return_user_if_it_inactive(login_string)
                if user is not None:
                    inactive_user_list.append(user)
                login_alt: FullName = NamePolicy.convert_to_alternative_login(
                    login)
                login_string = FullNameTool.to_string(login_alt, "")
                login_is_exists = login_string in login_list
                if not login_is_exists:
                    login_list.append(login_string)
                if login_is_exists or PIH.CHECK.USER.is_exists_by_login(login_string):
                    if not login_is_exists:
                        user = show_user_which_login_is_exists_and_return_user_if_it_inactive(login_string)
                        if user is not None:
                            inactive_user_list.append(user)
                    login_reversed: FullName = NamePolicy.convert_to_reverse_login(login)
                    login_is_exists = login_string in login_list
                    login_string = FullNameTool.to_string(login_reversed, "")
                    if not login_is_exists:
                        login_list.append(login_string)
                    if login_is_exists or PIH.CHECK.USER.is_exists_by_login(login_string):
                        if not login_is_exists:
                            user = show_user_which_login_is_exists_and_return_user_if_it_inactive(login_string)
                            if user is not None:
                                inactive_user_list.append(user)
                        enter_login: bool = False
                        if len(inactive_user_list) > 0:
                            if PIH.INPUT.yes_no("Удалить неактивных пользователей, чтобы освободить логин", True):
                                user_for_remove: User = inactive_user_list[0]
                                PR.value(f"Пользователь:", user_for_remove.name)
                                if PIH.INPUT.yes_no("Удалить пользователя?", True):
                                    PIH.ACTION.USER.remove(user_for_remove)
                                    login_string = user_for_remove.samAccountName
                                else:
                                    enter_login = True
                            else:
                                enter_login = True
                        if enter_login:
                            while True:
                                login_string = PIH.INPUT.login()
                                if PIH.CHECK.USER.is_exists_by_login(login_string):
                                    show_user_which_login_is_exists_and_return_user_if_it_inactive(login_string)
                                else:
                                    break
            PR.value("Свободный логин пользователя", login_string)
            if not PIH.INPUT.yes_no("Использовать этот логин?", True):
                login_string = PIH.INPUT.login(True)
            return login_string

        @staticmethod
        def generate_password(once: bool = False, settings: PasswordSettings = PASSWORD.SETTINGS.DEFAULT) -> str:
            def generate_password_interanal(settings: PasswordSettings = None) -> str:
                return PasswordTools.generate_random_password(settings.length, settings.special_characters,
                                                              settings.order_list, settings.special_characters_count,
                                                              settings.alphabets_lowercase_count, settings.alphabets_uppercase_count,
                                                              settings.digits_count, settings.shuffled)
            while True:
                password = generate_password_interanal(settings)
                if not once:
                    PR.value("Пароль",  password)
                if once or PIH.INPUT.yes_no("Использовать пароль?", True):
                    return password
                else:
                    pass

        @staticmethod
        def generate_email(login: str) -> str:
            return "@".join((login, CONST.SITE))

        @staticmethod
        def generate_user_principal_name(login: str) -> str:
            return "@".join((login, CONST.AD.DOMAIN_MAIN))


class PR:

    TEXT_AFTER: str = ""
    TEXT_BEFORE: str = ""

    @staticmethod
    def init() -> None:
        colorama.init()

    @staticmethod
    def clear_screen() -> None:
        ansi.clear_screen(2)

    @staticmethod
    def color_str(color: int, string: str, before_text: str = TEXT_BEFORE, after_text: str = TEXT_AFTER) -> str:
        string = f" {string} "
        return f"{before_text}{color}{string}{Back.RESET}{after_text}"

    @staticmethod
    def color(color: int, string: str, before_text: str = TEXT_BEFORE, after_text: str = " ") -> None:
        PR.write_line(PR.color_str(color, string, before_text, after_text))

    @staticmethod
    def write_line(string: str) -> None:
        print(string)

    @staticmethod
    def index(index: int, string: str) -> None:
        print(f"{index}. {string}")

    @staticmethod
    def input(caption: str) -> None:
        PR.write_line(PR.input_str(caption))

    @staticmethod
    def input_str(caption: str, before_text: str = TEXT_BEFORE, after_text: str = TEXT_AFTER) -> str:
        return f"{Fore.BLACK}{PR.color_str(Back.WHITE, caption, before_text, after_text)}{Fore.RESET}"

    @staticmethod
    def value(caption: str, value: str, before_text: str = TEXT_BEFORE) -> None:
        PR.cyan(caption, before_text, f" {value}")

    @staticmethod
    def get_action_value(caption: str, value: str, show: bool = True) -> ActionValue:
        if show:
            PR.value(caption, value)
        return ActionValue(caption, value)

    @staticmethod
    def head(caption: str) -> None:
        PR.cyan(caption)
    
    @staticmethod
    def head1(caption: str) -> None:
        PR.magenta(caption)

    @staticmethod
    def head2(caption: str) -> None:
        PR.nl()
        PR.yellow(caption)

    @staticmethod
    def nl() -> None:
        print()

    @staticmethod
    def alert_str(caption: str) -> str:
        return PR.red_str(caption)

    @staticmethod
    def alert(caption: str) -> str:
        PR.write_line(PR.alert_str(caption))

    @staticmethod
    def notify_str(caption: str) -> str:
        return PR.yellow_str(caption)

    @staticmethod
    def notify(caption: str) -> str:
        PR.write_line(PR.notify_str(caption))

    @staticmethod
    def good_str(caption: str) -> str:
        return PR.green_str(caption)

    @staticmethod
    def good(caption: str) -> str:
        PR.write_line(PR.good_str(caption))

    @staticmethod
    def green_str(string: str, before_text: str = TEXT_BEFORE, after_text: str = TEXT_AFTER) -> str:
        return PR.color_str(Back.GREEN, string, before_text, after_text)

    @staticmethod
    def green(string: str, before_text: str = TEXT_BEFORE, after_text: str = TEXT_AFTER) -> None:
        PR.write_line(PR.green_str(string, before_text, after_text))

    @staticmethod
    def yellow_str(string: str, before_text: str = TEXT_BEFORE, after_text: str = TEXT_AFTER) -> str:
        return PR.color_str(Back.YELLOW, string, before_text, after_text)

    @staticmethod
    def yellow(string: str, before_text: str = TEXT_BEFORE, after_text: str = TEXT_AFTER) -> None:
        PR.write_line(PR.yellow_str(string, before_text, after_text))

    @staticmethod
    def black_str(string: str, before_text: str = TEXT_BEFORE, after_text: str = TEXT_AFTER) -> str:
        return PR.color_str(Back.BLACK, string, before_text, after_text)

    @staticmethod
    def black(string: str, before_text: str = TEXT_BEFORE, after_text: str = TEXT_AFTER) -> None:
        PR.write_line(PR.black_str(string, before_text, after_text))

    @staticmethod
    def white_str(string: str, before_text: str = TEXT_BEFORE, after_text: str = TEXT_AFTER) -> str:
        return PR.color_str(Back.WHITE, string, before_text, after_text)

    @staticmethod
    def white(string: str, before_text: str = TEXT_BEFORE, after_text: str = TEXT_AFTER) -> None:
        PR.write_line(PR.white_str(string, before_text, after_text))

    @staticmethod
    def magenta_str(string: str, before_text: str = TEXT_BEFORE, after_text: str = TEXT_AFTER) -> str:
        return PR.color_str(Back.MAGENTA, string, before_text, after_text)

    @staticmethod
    def magenta(string: str, before_text: str = TEXT_BEFORE, after_text: str = TEXT_AFTER) -> None:
        PR.write_line(PR.magenta_str(string, before_text, after_text))

    @staticmethod
    def cyan(string: str, before_text: str = TEXT_BEFORE, after_text: str = TEXT_AFTER) -> None:
        PR.write_line(PR.cyan_str(string, before_text, after_text))

    @staticmethod
    def cyan_str(string: str, before_text: str = TEXT_BEFORE, after_text: str = TEXT_AFTER) -> str:
        return PR.color_str(Back.CYAN, string, before_text, after_text)

    @staticmethod
    def red(string: str, before_text: str = TEXT_BEFORE, after_text: str = TEXT_AFTER) -> None:
        PR.write_line(PR.red_str(string, before_text, after_text))

    @staticmethod
    def red_str(string: str, before_text: str = TEXT_BEFORE, after_text: str = TEXT_AFTER) -> str:
        return PR.color_str(Back.RED, string, before_text, after_text)

    @staticmethod
    def blue(string: str, before_text: str = TEXT_BEFORE, after_text: str = TEXT_AFTER) -> None:
        PR.write_line(PR.blue_str(string, before_text, after_text))

    @staticmethod
    def blue_str(string: str, before_text: str = TEXT_BEFORE, after_text: str = TEXT_AFTER) -> str:
        return PR.color_str(Back.BLUE, string, before_text, after_text)

    @staticmethod
    def bright(string: str, before_text: str = TEXT_BEFORE, after_text: str = TEXT_AFTER) -> None:
        PR.write_line(PR.bright_str(string, before_text, after_text))

    @staticmethod
    def bright_str(string: str, before_text: str = TEXT_BEFORE, after_text: str = TEXT_AFTER) -> str:
        return PR.color_str(Style.BRIGHT, string, before_text, after_text)


class ActionStack(List):
    
    def __init__(self, *argv):
        self.acion_value_list: List[ActionValue] = []
        for arg in argv:
            self.append(arg)
        self.start()

    def call_actions_by_index(self, index: int = 0, change: bool = False):
        previous_change: bool = False
        while True:
            try:
                action_value: ActionValue = self[index]()
                if action_value:
                    if change or previous_change:
                        previous_change = False
                        if index in self.acion_value_list:
                            self.acion_value_list[index] = action_value
                        else:
                            self.acion_value_list.append(action_value)
                    else:
                        self.acion_value_list.append(action_value)
                index = index + 1
                if index == len(self) or change:
                    break
            except KeyboardInterrupt:
                PR.red("Повтор предыдущих действия")
                if index > 0:
                    previous_change = True
                    #self.show_action_values()
                    #index = index - 1
                else:
                    continue

    def show_action_values(self) -> None:
        def label(item: ActionValue, index: int, ):
            return item.caption
        self.call_actions_by_index(PIH.INPUT.index(
            "Выберите свойство для изменения, введя индекс", self.acion_value_list, label), True)
        

    def start(self):
        self.call_actions_by_index()
        while True:
            PR.head2("Данные пользователя")
            for action_value in self.acion_value_list:
                PR.value(action_value.caption, action_value.value)
            if PIH.INPUT.yes_no("Данные верны?", True):
                break
            else:
               self.show_action_values()
