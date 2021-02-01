from bufferClass import Buffer
from h2oClass import H2o
import sys
import threading
import time
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow


class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setWindowTitle("Proyecto Final")
        self.setGeometry(800, 200, 300, 300)

        self.bt_buffer = QtWidgets.QPushButton(self)
        self.lb_buffer = QtWidgets.QLabel(self)
        self.buffer = Buffer()

        self.bt_h2o = QtWidgets.QPushButton(self)
        self.sb_h = QtWidgets.QSpinBox(self)
        self.sb_o = QtWidgets.QSpinBox(self)
        self.lb_h2o = QtWidgets.QLabel(self)
        self.lb_h = QtWidgets.QLabel(self)
        self.lb_o = QtWidgets.QLabel(self)
        self.h2o = H2o()

        self.bt_threads = QtWidgets.QPushButton(self)
        self.lb_threads = QtWidgets.QLabel(self)
        self.refresher = threading.Thread(target=self.thread_refresh)

        self.win_active = True
        self.init_ui()

    def init_ui(self):

        # Definicion del boton para rutina buffer
        self.bt_buffer.setText("Buffer")
        self.bt_buffer.setGeometry(0, 0, 100, 30)
        self.bt_buffer.clicked.connect(self.bt_buffer_clicked)

        # Definicion de labels para buffer
        self.lb_buffer.setGeometry(100, 0, 100, 30)

        # Definicion de boton h2o
        self.bt_h2o.setText("H2O")
        self.bt_h2o.setGeometry(0, 60, 100, 30)
        self.bt_h2o.clicked.connect(self.bt_h2o_clicked)

        # Definicion de Spinboxs para h2o
        self.sb_h.setGeometry(0, 90, 100, 30)
        self.sb_o.setGeometry(100, 90, 100, 30)

        # Definicion de labels para h2o
        self.lb_h2o.setGeometry(100, 60, 100, 30)
        self.lb_h.setGeometry(0, 120, 100, 30)
        self.lb_o.setGeometry(100, 120, 100, 30)

        # Definicion de boton threads
        self.bt_threads.setText("Threads")
        self.bt_threads.setGeometry(0, 30, 100, 30)
        self.bt_threads.clicked.connect(self.bt_threads_clicked)

        # Thread para actualizar la cantidad de thread y otras cosas
        self.refresher.start()

        # Definicion de label threads
        self.lb_threads.move(200, 270)
        self.lb_threads.setText(f"Threads: {Buffer.get_threads()}")

    def thread_refresh(self):
        while self.win_active:
            time.sleep(.001)
            self.lb_threads.setText(f"Extra Threads: {Buffer.get_threads()-2}")
            self.lb_buffer.setText(str(self.buffer.buff))
            self.lb_h2o.setText(f"{self.h2o.h2o} H2O particles")
            self.lb_h.setText(f"{self.h2o.hidrogeno} H particles")
            self.lb_o.setText(f"{self.h2o.oxigeno} O Particles")

    def closeEvent(self, event):
        self.win_active = False

        if self.buffer.is_active():
            self.buffer.buffer_stop()
        if self.h2o.oxigeno > 0:
            self.h2o.h2o_create_threads((2*self.h2o.oxigeno-(self.h2o.hidrogeno % 2)), 0)
        elif self.h2o.hidrogeno > 0 and self.h2o.oxigeno == 0:
            print(" h> 0 y o = 0")
            print(f" h{self.h2o.hidrogeno % 2} o{(self.h2o.hidrogeno + (self.h2o.hidrogeno % 2)) / 2}")
            self.h2o.h2o_create_threads(self.h2o.hidrogeno % 2, int((self.h2o.hidrogeno + (self.h2o.hidrogeno % 2)) / 2))
        self.h2o.h2o_run()
        self.refresher.join()
        print("Main Program ENDED".upper())
        event.accept()

    def bt_buffer_clicked(self):
        if self.buffer.is_active():
            self.buffer.buffer_stop()
        else:
            self.buffer.buffer_run()
        self.lb_threads.setText(f"Threads: {Buffer.get_threads()}")

    def bt_threads_clicked(self):
        self.lb_threads.setText(f"Threads: {Buffer.get_threads()}")

    def bt_h2o_clicked(self):
        self.h2o.h2o_create_threads(self.sb_h.value(), self.sb_o.value())
        self.sb_h.setValue(0)
        self.sb_o.setValue(0)
        # self.h2o.h2o_create_threads(2*self.sb_h2o.value(), self.sb_h2o.value())
        self.h2o.h2o_run()
        # self.h2o.h2o_wait()


def window():
    app = QApplication(sys.argv)
    win = MyWindow()
    win.show()
    sys.exit(app.exec_())


print("Main program".upper())

window()

