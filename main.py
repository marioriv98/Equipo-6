from bufferClass import Buffer
from h2oClass import H2o
from filosofosClass import Filosofos
import sys
import threading
import time
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt


class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setWindowTitle("Proyecto Final")
        self.setGeometry(800, 200, 300, 300)
        self.greenBrush = QtGui.QBrush(Qt.green)
        self.redBrush = QtGui.QBrush(Qt.red)
        self.whiteBrush = QtGui.QBrush(Qt.white)
        self.pen = QtGui.QPen(Qt.black)

        # Elementos de buffer
        self.bt_buffer = QtWidgets.QPushButton(self)
        self.lb_buffer = QtWidgets.QLabel(self)
        self.sc_buffer = QtWidgets.QGraphicsScene(self)
        self.gv_b1 = QtWidgets.QGraphicsView(self.sc_buffer, self)
        self.gv_b2 = QtWidgets.QGraphicsView(self.sc_buffer, self)
        self.buffer = Buffer()
        # Elemntos de h2o
        self.bt_h2o = QtWidgets.QPushButton(self)
        self.sb_h = QtWidgets.QSpinBox(self)
        self.sb_o = QtWidgets.QSpinBox(self)
        self.lb_h2o = QtWidgets.QLabel(self)
        self.lb_h = QtWidgets.QLabel(self)
        self.lb_o = QtWidgets.QLabel(self)
        self.h2o = H2o()
        # Elementos filosofos
        self.bt_filosofos = QtWidgets.QPushButton(self)
        self.sc_filosofos = QtWidgets.QGraphicsScene(self)
        self.gv_filosofos = QtWidgets.QGraphicsView(self.sc_filosofos, self)
        self.f_squares = []
        self.lb_filosofos = QtWidgets.QLabel(self)
        self.filosofos = Filosofos()

        # Elementos de threads
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
        self.lb_buffer.setGeometry(165, 0, 30, 30)

        # Def Gv de buffer
        self.gv_b1.setGeometry(100, 1, 28, 28)
        self.gv_b1.setBackgroundBrush(self.greenBrush)
        self.gv_b2.setGeometry(130, 1, 28, 28)
        self.gv_b2.setBackgroundBrush(self.greenBrush)

        # Definicion de boton h2o
        self.bt_h2o.setText("H2O")
        self.bt_h2o.setGeometry(0, 30, 100, 30)
        self.bt_h2o.clicked.connect(self.bt_h2o_clicked)

        # Definicion de Spinboxs para h2o
        self.sb_h.setGeometry(0, 60, 100, 30)
        self.sb_h.setMaximum(200)
        self.sb_o.setGeometry(100, 60, 100, 30)
        self.sb_o.setMaximum(200)

        # Definicion de labels para h2o
        self.lb_h2o.setGeometry(100, 30, 130, 30)
        self.lb_h.setGeometry(0, 90, 100, 30)
        self.lb_o.setGeometry(100, 90, 100, 30)

        # Definicion de boton filosofos
        self.bt_filosofos.setText("Filosofos")
        self.bt_filosofos.setGeometry(0, 120, 100, 30)
        self.bt_filosofos.clicked.connect(self.bt_filosofos_clicked)

        # Definicion de label filosofos
        self.lb_filosofos.setGeometry(0, 150, 300, 30)
        self.lb_filosofos.setText("    F1        F2        F3         F4        F5")

        # Definicion de Graphics view de filosofos

        self.gv_filosofos.setGeometry(0, 180, 200, 30)

        for _ in range(5):
            self.f_squares.append(self.sc_filosofos.addRect(0, 0, 20, 20, self.pen, self.redBrush))

        x = -160
        for _ in range(len(self.f_squares)):
            self.f_squares[_].moveBy(x, 0)
            x += 40

        # Thread para actualizar la cantidad de thread y otras cosas
        self.refresher.start()

        # Definicion de label threads
        self.lb_threads.move(200, 270)
        self.lb_threads.setText(f"Threads: {Buffer.get_threads()}")

    def thread_refresh(self):
        while self.win_active:
            self.refresh()

    def refresh(self):
        time.sleep(.001)
        self.lb_threads.setText(f"Extra Threads: {Buffer.get_threads() - 2}")
        self.refresh_buffer()
        self.lb_h2o.setText(f"Particulas de H2O: {self.h2o.h2o}")
        self.lb_h.setText(f"Particulas de H: {self.h2o.hidrogeno}")
        self.lb_o.setText(f"Particulas de O: {self.h2o.oxigeno}")
        self.refresh_filosofos()

    def refresh_buffer(self):
        self.lb_buffer.setText(str(self.buffer.buff))
        if self.buffer.buff == 0:
            self.gv_b1.setBackgroundBrush(self.whiteBrush)
            self.gv_b2.setBackgroundBrush(self.whiteBrush)
        elif self.buffer.buff == 1:
            self.gv_b1.setBackgroundBrush(self.greenBrush)
            self.gv_b2.setBackgroundBrush(self.whiteBrush)
        elif self.buffer.buff == 2:
            self.gv_b1.setBackgroundBrush(self.greenBrush)
            self.gv_b2.setBackgroundBrush(self.greenBrush)

    def refresh_filosofos(self):
        for _ in range(5):
            if self.filosofos.fComiendo[_]:
                self.f_squares[_].setBrush(self.greenBrush)
            else:
                self.f_squares[_].setBrush(self.redBrush)

    def closeEvent(self, event):
        self.win_active = False
        self.buffer.pause = False
        if self.buffer.is_active():
            self.buffer.buffer_stop()
        if self.filosofos.is_active():
            self.filosofos.filosofos_stop()
        if self.h2o.oxigeno > 0:
            self.h2o.h2o_create_threads((2*self.h2o.oxigeno-(self.h2o.hidrogeno % 2)), 0)
        elif self.h2o.hidrogeno > 0 and self.h2o.oxigeno == 0:
            self.h2o.h2o_create_threads(self.h2o.hidrogeno % 2,
                                        int((self.h2o.hidrogeno + (self.h2o.hidrogeno % 2)) / 2))
        self.h2o.h2o_run()
        self.refresher.join()
        print("Main Program ENDED".upper())
        event.accept()

    def bt_buffer_clicked(self):
        if self.buffer.is_active():
            self.buffer.buffer_stop()
        else:
            self.buffer.buffer_run()

    def bt_filosofos_clicked(self):
        if self.filosofos.is_active():
            self.filosofos.filosofos_stop()
        else:
            self.filosofos.filosofos_run()

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
