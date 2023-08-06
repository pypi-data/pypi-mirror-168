import tkinter
import ttkbootstrap
import pickle


class ScrollListbox(tkinter.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        scr1 = ttkbootstrap.Scrollbar(self)
        scr2 = ttkbootstrap.Scrollbar(self, orient=tkinter.HORIZONTAL)
        scr1.pack(side=tkinter.RIGHT, fill="y")
        scr2.pack(side=tkinter.BOTTOM, fill="x")

        lb1 = tkinter.Listbox(self, yscrollcommand=scr1.set, xscrollcommand=scr2.set)
        lb1.pack(side=tkinter.LEFT, fill="both")

        scr1.config(command=lb1.yview)
        scr2.config(command=lb1.xview)


class SetupHelper(object):
    def __init__(self, file):
        self.file_name = file

        try:
            file = open(self.file_name, "rb")
        except:
            file = open(self.file_name, "wb")
            pickle.dump({}, file)
            file.close()
            file = open(self.file_name, "rb")

        self.setup_dict: dict = pickle.load(file)
        file.close()

    def save_file(self):
        file = open(self.file_name, "wb")
        pickle.dump(self.setup_dict)
        file.close()

    def save_item(self, name, obj):
        self.setup_dict[name] = obj

    def get_item(self, name):
        item = self.setup_dict[name]
        return item

    def get_all_item(self):
        items = self.setup_dict.copy()
        return items
