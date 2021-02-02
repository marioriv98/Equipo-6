import threading
import time


class H2o:

    def __init__(self):
        self.init = False
        self.running = False
        self.hidrogeno = 0
        self.oxigeno = 0
        self.temp = 0
        self.h2o = 0
        self.h_threads = []
        self.o_threads = []
        self.semHdisp = threading.Semaphore(2)
        self.semHocup = threading.Semaphore(0)
        self.semUlista = threading.Semaphore(0)
        self.semOdisp = threading.Semaphore(1)
        self.semU = threading.Semaphore(1)

    def hidrogeno_thread(self):
        self.hidrogeno += 1
        self.semHdisp.acquire()

        self.semHocup.release()
        self.semUlista.acquire()

        self.semU.acquire()
        # Seccion critica union

        self.union('h')
        # Seccion critica union
        self.semU.release()

        self.semHdisp.release()

    def oxigeno_thread(self):
        self.oxigeno += 1
        self.semOdisp.acquire()
        self.semHocup.acquire()
        self.semHocup.acquire()
        self.semUlista.release()
        self.semUlista.release()

        self.semU.acquire()

        # Seccion critica
        self.union('o')

        self.semU.release()
        # Seccion critica
        self.semOdisp.release()

    def h2o_create_threads(self, h, o):

        for _ in range(0, h):
            self.h_threads.append(threading.Thread(target=self.hidrogeno_thread))

        for _ in range(0, o):
            self.o_threads.append(threading.Thread(target=self.oxigeno_thread))

        print(f"{len(self.h_threads)} H Threads Created")
        print(f"{len(self.o_threads)} O Threads Created")

    def h2o_run(self):

        for _ in range(0, len(self.h_threads)):
            self.h_threads[_].start()

        for _ in range(0, len(self.o_threads)):
            self.o_threads[_].start()

        self.h_threads.clear()
        self.o_threads.clear()

    def union(self, x):
        time.sleep(.1)
        if x.upper() == 'H':
            print("Hydrogen agregado".upper())
            self.hidrogeno -= 1
            self.temp += 1
        elif x.upper() == 'O':
            print("oxygen agregado".upper())
            self.oxigeno -= 1
            self.temp += 1
        if self.temp == 3:
            print("h2o creado".upper())
            self.temp = 0
            self.h2o += 1

    def is_active(self):
        return self.running

    @staticmethod
    def get_threads():
        return threading.activeCount()
