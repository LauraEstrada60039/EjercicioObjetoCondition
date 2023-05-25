import logging
import threading
import time
#Agregar el buffer finito (10 elementos)
buffer = 10
#Agregar condición de parada del productor
stopProducer = 0
#Agregar condición de consumo
startConsumer = 1
#Lista de conexiones
listProducts = [buffer] #Genero una lista de los productos que serán consumidos con una cantidad de 10 pieza
counter = 0
#Agregar producción y el consumo (manipulación de buffer)


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s (%(threadName)-2s) %(message)s',
                    )


def consumer(cond):
    """wait for the condition and use the resource"""
    logging.debug('Iniciando hilo consumidor')
    #t = threading.currentThread()
    with cond:
        #sección critica
        cond.wait()
        logging.debug('El recurso está disponible para el consumidor')
        listProducts.pop(len(listProducts)-1)
        print(listProducts)


def producer(cond):
    """set up the resource to be used by the consumer"""
    logging.debug('Iniciando el hilo productor')
    with cond:
        logging.debug('Poniendo los recursos disponibles')
        global counter
        counter+=1
        listProducts.append(counter)
        print(listProducts)
        cond.notifyAll()


condition = threading.Condition()
c1 = threading.Thread(name='c1', target=consumer, args=(condition,))
c2 = threading.Thread(name='c2', target=consumer, args=(condition,))
p = threading.Thread(name='p', target=producer, args=(condition,))

c1.start()
time.sleep(2)
c2.start()
time.sleep(2)
p.start()