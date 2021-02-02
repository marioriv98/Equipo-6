import threading
import time


class Filosofos:
    # Inicializacion de un objeto buffer
    def __init__(self):
        self.running = False

        self.fComiendo = [False, False, False, False, False]

        self.semPal1 = threading.Semaphore(1)    # Semaforo de disponibles
        self.semPal2 = threading.Semaphore(1)    # Semaforo de disponibles
        self.semPal3 = threading.Semaphore(1)    # Semaforo de disponibles
        self.semPal4 = threading.Semaphore(1)    # Semaforo de disponibles
        self.semPal5 = threading.Semaphore(1)    # Semaforo de disponibles

    # Deinicion del thread de Filosofo1
    def filosofo1_thread(self):
        while True:
            time.sleep(.1)
            if not self.running:
                return
            self.semPal1.acquire()
            self.semPal2.acquire()
            #Seccion Critica
            self.fComiendo[0]= True
            print("comer f1")
            time.sleep(.5)
            self.fComiendo[0] = False
            #Seccion Critica
            self.semPal1.release()
            self.semPal2.release()

    # Deinicion del thread de Filosofo2
    def filosofo2_thread(self):
        while True:
            time.sleep(.1)
            if not self.running:
                return
            self.semPal3.acquire()
            self.semPal2.acquire()
            # Seccion Critica
            self.fComiendo[1] = True
            print("comer f2")
            time.sleep(.5)
            self.fComiendo[1] = False
            # Seccion Critica
            self.semPal2.release()
            self.semPal3.release()

    # Deinicion del thread de Filosofo3
    def filosofo3_thread(self):
        while True:
            time.sleep(.1)
            if not self.running:
                return
            if not self.running:
                return
            self.semPal3.acquire()
            self.semPal4.acquire()
            #Seccion Critica
            self.fComiendo[2] = True
            print("comer f3")
            time.sleep(.5)
            self.fComiendo[2] = False
            #Seccion Critica
            self.semPal3.release()
            self.semPal4.release()

    # Deinicion del thread de Filosofo4
    def filosofo4_thread(self):
        while True:
            time.sleep(.1)
            if not self.running:
                return
            self.semPal5.acquire()
            self.semPal4.acquire()
            #Seccion Critica
            self.fComiendo[3] = True
            print("comer f4")
            time.sleep(.5)
            self.fComiendo[3] = False
            #Seccion Critica
            self.semPal4.release()
            self.semPal5.release()

    # Deinicion del thread de Filosofo5
    def filosofo5_thread(self):
        while True:
            time.sleep(.1)
            if not self.running:
                return
            self.semPal5.acquire()
            self.semPal1.acquire()
            # Seccion Critica
            self.fComiendo[4] = True
            print("comer f5")
            time.sleep(.5)
            self.fComiendo[4] = False
            # Seccion Critica
            self.semPal5.release()
            self.semPal1.release()

    # Definicion de la rutina para que comience la mesa
    def filosofos_run(self):
        print("FILOSOFOS INIT")
        self.running = True
        # Definicion de los 2 threads
        self.filosofo1 = threading.Thread(target=self.filosofo1_thread)
        self.filosofo2 = threading.Thread(target=self.filosofo2_thread)
        self.filosofo3 = threading.Thread(target=self.filosofo3_thread)
        self.filosofo4 = threading.Thread(target=self.filosofo4_thread)
        self.filosofo5 = threading.Thread(target=self.filosofo5_thread)
        # Inicio de los 2 threads
        self.filosofo5.start()
        self.filosofo1.start()
        self.filosofo2.start()
        self.filosofo3.start()
        self.filosofo4.start()

    # Definicion de la rutina para que termine de correr el buffer
    def filosofos_stop(self):
        self.running = False

        # Espera a que terminen de ejecutarse ambos threads
        self.filosofo1.join()
        self.filosofo2.join()
        self.filosofo3.join()
        self.filosofo4.join()
        self.filosofo5.join()
        print("FILOSOFOS ENDED")

    def is_active(self):
        return self.running

    @staticmethod
    def get_threads():
        return threading.activeCount()
