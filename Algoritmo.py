"""
Proyecto de Redes
Autor: Sebastian Chavarry
Codigo: 20200498
Numero de Orden: 13
Tema: Vector Distancia //Bellman-Ford
"""

#Se importan las librerias que vamos a necesitar para el codigo
import numpy as np, timeit, os, psutil, sys

#Definimos variables String con codigo ASCII que nos permitiran dar color a nuestro codigo
RED = "\033[0;31m"
BLUE = "\033[0;34m"
LIGHT_GREEN = "\033[1;32m"
BOLD = "\033[1m"

#Esta clase permitira realizar todas las funciones necesarias para ejecutar el algoritmo
class Grafo:
    #Creamos metodo constructor que recibe como parametros la cantidad de vertices/nodos
    def __init__(self, vertices):
        self.cantV = vertices
        self.matriz = []
    '''
    Creamos metodo para agregar arista al grafo
    u = Nodo fuente
    v = nodo destino
    w = peso
    '''
    def agregarArista(self, u, v, w):
        #En estado tendremos una matriz de multiples arrays que representan las aristas
        self.matriz.append([u,v,w])
        
    '''
    Metodo auxiliar que permitira imprimir una tabla la suma de los pesos del camino 
    más corto hacia X nodo
    Distancias = Lista que contiene las distancias entre los nodos
    Fuente = Nodo origen desde donde se busca obtener la distancia mas corta
    '''
    def imprimir(self, distancias, fuente):
        print("Vertice \tDistancia desde el nodo {}\n".format(fuente))
        for i in range(self.cantV):
            print("{}\t\t\t{}".format(i, distancias[i]))
    
    def imprimirRutas(self, predecesor):        
        imprimir = ""     
        for nodo in range(self.cantV):
            current = nodo
            print("Ruta para llegar hasta el nodo {}".format(nodo))
            while(current != None):
                if (imprimir == ""):
                    imprimir = imprimir + str(current)
                    current = predecesor[current]
                else:
                    imprimir =  imprimir +" <-- "+ str(current) 
                    current = predecesor[current]
            print(imprimir)
            imprimir = ""
    
    
    def BellmanFord(self, fuente):
        '''
        Paso 1: Inicializamos las distancias del nodo fuente a todos 
        los vertices valore infinito
        '''
        infinito = np.inf    
        distancias = [infinito] * self.cantV
        distancias[fuente] = 0
        predecesor = [None] * self.cantV
        
        '''
        Paso 2: Aplicamos el relax V-1 a todos 
        '''
        iteracion = 0
        
        self.imprimir(distancias, fuente)
        
        for nodo in range(self.cantV-1):
            for u,v,w in self.matriz: 
                if  distancias[u] != infinito and distancias[u] + w < distancias[v]:
                    distancias[v] = distancias[u] + w
                    predecesor[v] = u
                iteracion = iteracion + 1
            print('\n'+BLUE+BOLD +"Iteracion {}".format(iteracion) + '\n')
            self.imprimir(distancias, fuente)
            
        global nro_repeticiones
        nro_repeticiones = iteracion 
        
    
        '''
        Paso 3:
        Verificacion de parte del algoritmo para asegurarnos que no existen 
        ciclos negativos 
        '''
        for u,v,w in self.matriz:
            if distancias[u] != infinito and distancias[u] + w < distancias[v]:
                print("El Grafo contiene ciclos de peso negativo")
                break    
        
        self.imprimirRutas(predecesor)
        print(RED + BOLD + "\nALGORITMO BELLMAN-FORD")
        self.imprimir(distancias, fuente)
       
  

def main():   
    #Leemos el archio txt que contiene las aristas en una lista
    opcion = ""
    while(True):
        try:
            num_temp = int(input("Ingrese el numero segun la topologia deseada: \n [1] \t Topologia de Complejidad Baja \n [2] \t Topologia de Complejidad Media \n"))
            if (num_temp == 1):
                opcion = 'topologia1.txt'
                break
            elif (num_temp == 2):
                opcion = 'topologia2.txt'
                break
        except ValueError:
                print("INGRESE UN VALOR VALIDO (1 o 2) \n")
    
    try:
        with open(opcion, 'r') as f:
            temp = []
            for line in f:
                temp.append(line.rstrip().split())
            f.close() 
    except OSError:
        print("No se pudo abrir/leer el archivo: ", opcion)
        sys.exit()
        
    nodos= int(temp[0][0]) 
    while (True):
        try:
            fuente = int(input("Ingresa el nodo origen para aplicar el algoritmo: \n"))
            break
        except ValueError:
            print("Ingresar un numero entre 0 y {}".format(nodos-1))
    #instanciamos el grafo
    g = Grafo(nodos)
    #Agregamos las aristas al grafo creado usando la lista anterior
    for i,line in enumerate(temp):
        if (i != 0): 
            g.agregarArista(int(line[0]), int(line[1]), int(line[2]))           
    
    execution_time = timeit.timeit(lambda: g.BellmanFord(fuente), number= 1)
    print(LIGHT_GREEN + "METRICAS")
    print("1) Tiempo de ejecucion (Segundos): ")
    print(execution_time)
    #Metodo para calcular la cantidad de memoria usada
    print("2) Cantidad de memoria usada (MB): ")
    print(psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2)
    print("3) Numero de iteraciones para hallar la ruta más corta")
    print(nro_repeticiones)


main()