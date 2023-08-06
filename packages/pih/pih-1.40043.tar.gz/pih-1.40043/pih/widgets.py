from tkinter import Text

class BarcodeInput(Text):
    def __init__(self, *args, **kwargs):
        Text.__init__(self, *args, **kwargs)
        self._orig = self._w + "_orig"
        self.tk.call("rename", self._w, self._orig)
        self.tk.createcommand(self._w, self._proxy)

    def _proxy(self, command, *args):
        cmd = (self._orig, command) + args
        result = self.tk.call(cmd)
        if command in ("insert", "delete", "replace"):
            self.event_generate("<<TextModified>>")
        return result

    def set_text(self, value: str) -> None:
        self.delete(1.0, "end")
        self.insert(1.0, value)
        self.tag_configure("center", justify='center')
        self.tag_add("center", "1.0", "end")
