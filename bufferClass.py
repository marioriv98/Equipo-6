import threading
import time


class Buffer:
    # Inicializacion de un objeto buffer
    def __init__(self):
        self.running = False
        self.cons = False                       # Variable para Consumiendo
        self.full = False
        self.buff = 0
        self.semDis = threading.Semaphore(2)    # Semaforo de disponibles
        self.semUti = threading.Semaphore(0)    # Semaforo de Utilizados

    # Defnicion del thread de Producir
    def produce_thread(self):
        while True:
            if not (self.running or (not self.full and self.cons)):
                return
            self.semDis.acquire()

            # Inicia seccion critica para producir
            time.sleep(.1)
            print("Produce")

            self.buff += 1
            time.sleep(.1)
            # Termina seccion critica para producir

            self.semUti.release()

    # Defnicion del thread de Consumir
    def consume_thread(self):
        while True:

            self.cons = True
            self.semUti.acquire()
            self.semUti.acquire()
            self.full = True
            # Inicia seccion critica para consumir
            time.sleep(.1)
            print("Consume")
            self.buff -= 2
            time.sleep(.1)
            # Termina seccion critica para consumir

            self.full = False
            self.cons = False
            self.semDis.release(2)

            if not self.running:
                return

    # Definicion de la rutina para que comience a correr el buffer
    def buffer_run(self):
        print("BUFFER INIT")
        self.running = True
        # Definicion de los 2 threads
        self.producer = threading.Thread(target=self.produce_thread)
        self.consumer = threading.Thread(target=self.consume_thread)
        # Inicio de los 2 threads
        self.consumer.start()
        self.producer.start()

    # Definicion de la rutina para que termine de correr el buffer

    def buffer_stop(self):
        self.running = False

        # Espera a que terminen de ejecutarse ambos threads
        self.consumer.join()
        self.producer.join()
        print("BUFFER ENDED")

    def is_active(self):
        return self.running

    @staticmethod
    def get_threads():
        return threading.activeCount()
