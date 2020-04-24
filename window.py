import sys
from time import sleep
import random
from PyQt5.QtCore import Qt, QDir
from PyQt5.QtGui import QIcon, QFont, QFontDatabase
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel,
    QPushButton, QGridLayout, QVBoxLayout, QHBoxLayout, QGroupBox,
    QWidget, QComboBox)


class Window(QMainWindow):
    X, Y = 400, 200  # upperleft coordinates of window
    WIDTH, HEIGHT = 600, 200 # width and height of window

    def __init__(self, ctrl, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)

        self.arabic_font = QFont("Amiri", 36)
        self.num_of_cols = 4  # button grid

        self.ctrl = ctrl
        self.ctrl.signal.connect(self.relay)
        self.ctrl.setup_signal.connect(self.init_values)

        self.setWindowProperties() # size, title, icon

        self.configure_screen(self.ctrl.surah_list)

    def setWindowProperties(self):
        ''' set dimensions, title, logo '''
        self.setGeometry(Window.X, Window.Y, Window.WIDTH, Window.HEIGHT)
        self.setWindowTitle("Quran Quiz")
        self.setWindowIcon(QIcon('pythonlogo.png'))

    def relay(self, state, n, text):
        ''' receive message from controller '''
        # print(f"message relayed: {n}")

        if state == "configure 1":
            self.ayahs_in_surah = n
            self.populate_combobox_1()

        elif state == "configure 2":
            print(f"configuring second combobox: {n}")
            self.populate_combobox_2(n)

        # elif state == "start":
        #     self.question_screen(n)
        elif state == "question":
            self.question_screen(n, text)
        elif state == "result":
            res = True if n == 1 else 0
            self.result_screen(res)

    def init_values(self, start_ayah, num_of_ayahs):
        self.start_ayah = start_ayah
        self.num_of_ayahs = num_of_ayahs
        self.create_buttons(num_of_ayahs, start_ayah)

    def populate_combobox_1(self):
        self.from_ayah_combobox.clear()
        for i in range(1, self.ayahs_in_surah + 1):
            self.from_ayah_combobox.addItem(str(i))

    def populate_combobox_2(self, start):
        self.to_ayah_combobox.clear()
        for i in range(start, self.ayahs_in_surah + 1):
            self.to_ayah_combobox.addItem(str(i))

    def configure_screen(self, surah_list):
        ''' select surah and ayahs '''

        self.surah_combobox = QComboBox()
        self.surah_combobox.addItem("")
        for ind, surah in enumerate(surah_list[1:]):
            self.surah_combobox.addItem(f"{ind+1} - {surah}")
        self.surah_combobox.activated.connect(self.ctrl.surah_combobox_item_selected)

        self.from_ayah_combobox = QComboBox()
        self.from_ayah_combobox.activated.connect(self.ctrl.start_ayah_selected)

        self.to_ayah_combobox = QComboBox()
        self.to_ayah_combobox.activated.connect(self.ctrl.end_ayah_selected)

        start_btn = QPushButton("Start")
        start_btn.pressed.connect(self.ctrl.start_btn_pressed)

        self.components = [
            [QLabel("Select surah:"), self.surah_combobox],
            [
                QLabel("Select ayah range:"),
                self.from_ayah_combobox,
                QLabel("to"),
                self.to_ayah_combobox,
            ],
            start_btn,
        ]

        self.setup_layout()

    def start_screen(self):
        ''' start screen '''

        next_btn = QPushButton("Start")
        next_btn.pressed.connect(self.ctrl.start_btn_pressed)

        self.components = [
            QLabel("Ready?"),
            next_btn,
            ]
        self.setup_layout()
     
    def question_screen(self, answer, txt):
        ''' question screen 
        n: answer
        '''
        # self.answer = answer

        text = QLabel(txt)
        text.setFont(self.arabic_font)

        # self.create_buttons()
        self.create_buttons(self.num_of_ayahs, self.start_ayah)

        self.components = [
            text, 
            # self.create_buttons(n, start),
            self.button_grid_group_box,
            ]
        self.setup_layout()

    def result_screen(self, res):
        ''' display correct or incorrect '''
        if res:
            text = QLabel("That's correct")
        else:
            text = QLabel("That is not correct")

        cont_btn = QPushButton("Continue")
        cont_btn.pressed.connect(self.ctrl.cont_btn_pressed)

        self.components = [
            text,
            cont_btn,
            ]
        self.setup_layout()

    def create_buttons(self, num_btns, start):
        num_of_cols = 6
        self.button_grid_group_box = QGroupBox()
        self.button_grid_layout = QGridLayout()
        for i in range(num_btns):
            row = i / num_of_cols
            col = i % num_of_cols
            btn = QPushButton(str(i+start))
            btn.pressed.connect(lambda i=i: self.ctrl.num_btn_pressed(i+start))
            self.button_grid_layout.addWidget(btn, row, col)
        self.button_grid_group_box.setLayout(self.button_grid_layout)
        # return group_box
        # self.button_grid_group_box = group_box

    def setup_layout(self):
        ''' add components to screen '''
        layout = QVBoxLayout()

        for cmp in self.components:
            row = QHBoxLayout()
            row.setAlignment(Qt.AlignCenter)
            if isinstance(cmp, list):
                for elem in cmp:
                    row.addWidget(elem)
            else:
                row.addWidget(cmp)
            layout.addLayout(row)

        self.mainWidget = QWidget()
        self.setCentralWidget(self.mainWidget)
        self.mainWidget.setLayout(layout)
        self.show()


if __name__ == "__main__":
    pass
    # app = QApplication(sys.argv)
    # app.setFont(QFont("Amiri", 32))
    # window = Window()
    # sys.exit(app.exec_())