import sys
import random
from window import Window
from utils import get_ayahs, get_surahs
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QFont

class Controller(QThread):
    ''' retrieves data and handles window '''
    signal = pyqtSignal(str, int, str)

    def __init__(self):
        super(Controller, self).__init__()

        self.start_ayah = None

        # self.send_msg = False

        self.surah_list, self.nums_of_ayahs = get_surahs()

        self.window = Window(self)

    def start_btn_pressed(self):
        ''' test '''

        if self.surah_num and self.start_ayah and self.end_ayah:
            self.num_of_ayahs = self.end_ayah - self.start_ayah + 1
            # print(f"start: {self.start_ayah}, end: {self.end_ayah}")
            # print(f"num_of_ayahs: {self.num_of_ayahs}")

            self.ayah_dict = get_ayahs(self.surah_num, self.start_ayah, self.num_of_ayahs)

            self.next_question()

    def surah_combobox_item_selected(self, item):
        if item > 0:
            self.surah_num = item
            print(f"item selected: {item}")
            num_of_ayahs = self.nums_of_ayahs[item]
            self.signal.emit("configure 1", num_of_ayahs, "")
            self.start_ayah_selected(0)

    def start_ayah_selected(self, item):
        ''' on start ayah selection in configuration screen '''
        self.start_ayah = item + 1
        self.end_ayah = self.start_ayah
        self.signal.emit("configure 2", self.start_ayah, "")

    def end_ayah_selected(self, item):
        ''' on end ayah selection '''
        self.end_ayah = item + 1

    def num_btn_pressed(self, n):
        ''' number button pressed '''
        print(f"number pressed: {n}")
        if n == self.answer:
            print("correct")
            self.signal.emit("result", 1, "")
        else:
            print("incorrect")
            self.signal.emit("result", 0, "")

    def cont_btn_pressed(self):
        ''' continue button pressed '''
        self.next_question()

    def next_question(self):

        self.answer = random.randint(1, self.num_of_ayahs)
        # print(f"answer: {self.answer}")

        self.state = "question"
        text = self.ayah_dict[self.answer]
        self.signal.emit(self.state, self.num_of_ayahs, text)

    def send_message(self):
        r = random.randint(1, 30)
        self.signal.emit(r)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setFont(QFont("Amiri", 16))
    ctrl = Controller()
    sys.exit(app.exec_())