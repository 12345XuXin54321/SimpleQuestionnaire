import remi.gui as gui
from remi import start, App


class BaseWindowVBox(gui.VBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.base_item = []
        self.permanent_item = []

    def reshow_items(self):
        for w in self.base_item:
            self.append(w)

    def add_item(self, w):
        self.base_item.append(w)
        self.append(w)

    def add_permanent_item(self, w):
        self.permanent_item.append(w)
        self.append(w)

    def open_weight(self, w):
        for bw in self.base_item:
            self.remove_child(bw)
        self.append(w)


class WindowVBox(BaseWindowVBox):
    def __init__(self, father_window, *args, **kwargs):
        super().__init__(*args, **kwargs)
        assert (isinstance(father_window, BaseWindowVBox))

        self.fa_window = father_window

        self.close_button = gui.Button("关闭")
        self.close_button.onclick.do(self.onclose)

        hb = gui.HBox()
        hb.append(self.close_button)
        self.base_item.append(hb)

        self.append(hb)

    def onclose(self, w):
        self.fa_window.remove_child(self)
        self.fa_window.reshow_items()


class ChoosableItem(gui.HBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = gui.Label("")
        self.view = gui.Button("查看")
        self.append(self.name)
        self.append(self.view)

    def call_back_func(self, weight):
        self.cb_func(self)

    def set_data(self, name, func):
        self.name.set_text(name)
        self.view.onclick.do(self.call_back_func)
        self.cb_func = func
