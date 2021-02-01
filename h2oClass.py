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

        # time.sleep(.1)
        self.union('h')
        #seccion critica union
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
            print("Hydrogen added".upper())
            self.hidrogeno -= 1
            self.temp += 1
        elif x.upper() == 'O':
            print("oxygen added".upper())
            self.oxigeno -= 1
            self.temp += 1
        if self.temp == 3:
            print("h2o created".upper())
            self.temp = 0
            self.h2o += 1
            print(f"there are {self.h2o} H2o molecules ".upper())

    # def h2o_wait(self):
    #     for _ in range(0, 2*self.n):
    #         self.h_threads[_].join()
    #         if _ < self.n:
    #             self.o_threads[_].join()
    #     self.running = False
    #
    #     print(self.get_threads())
    #     print(self.h_threads)
    #     print(self.o_threads)
    #
    #     self.h_threads.clear()
    #     self.o_threads.clear()
    #     self.n = 0
    #     print(self.h_threads)
    #     print(self.o_threads)
    #     print("H2O ENDED")

    def is_active(self):
        return self.running

    @staticmethod
    def get_threads():
        return threading.activeCount()
