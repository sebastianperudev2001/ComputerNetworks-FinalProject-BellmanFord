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
    
    '''
    Metodo auxiliar que permite generar el camino mas corto hacia cada nodo
    Recibe como parametro la lista de predecesor, la cual contiene el orden 
    de recorrido de los nodos
    '''
    
    def imprimirRutas(self, predecesor):        
        imprimir = ""     
        for nodo in range(self.cantV):
            current = nodo
            print("Ruta para llegar hasta el nodo {}".format(nodo))
            while(current != None):
                #Se agrega una verificacion de formato para el primer caso 
                if (imprimir == ""):
                    imprimir = imprimir + str(current)
                    current = predecesor[current]
                else:
                    imprimir =  imprimir +" <-- "+ str(current) 
                    current = predecesor[current]
            print(imprimir)
            imprimir = ""
    
    '''
    La funcion principal que nos permitira realizar la ejecucion del algoritmo
    de la ruta mas corta
    '''
    def BellmanFord(self, fuente):
        '''
        Paso 1: Inicializamos las distancias del nodo fuente a todos 
        los vertices valore infinitos
        '''
        infinito = np.inf    
        distancias = [infinito] * self.cantV
        distancias[fuente] = 0
        predecesor = [None] * self.cantV
        
        '''
        Paso 2: Aplicamos el relax V-1 a todos para hallar la ruta mas corta
        '''
        #Se inicializa una variable auxiliar para controlar las iteraciones posibles
        iteracion = 0
        
        #Se imprimer la tabla inicial antes de iterar 
        self.imprimir(distancias, fuente)
        
        #Se actualiza el valor de distancia si la rota es la mas corta posible
        for nodo in range(self.cantV-1):
            for u,v,w in self.matriz: 
                if  distancias[u] != infinito and distancias[u] + w < distancias[v]:
                    distancias[v] = distancias[u] + w
                    predecesor[v] = u
            iteracion = iteracion + 1
            #Por cada nodo recorrido se va mostrando la tabla de distancias
            print('\n'+BLUE+BOLD +"Iteracion {}".format(iteracion) + '\n')
            self.imprimir(distancias, fuente)
        
        #Se inicializa una variable que almacenara la cantidad total de iteraciones realizadas            
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
        
        #Se llama a la funcion auxiliar para imprimir las rutas generadas
        self.imprimirRutas(predecesor)
        
        #Se llama a la funcion auxiliar para imprimir la suma de pesos totales
        print(RED + BOLD + "\nALGORITMO BELLMAN-FORD")
        self.imprimir(distancias, fuente)
        
def main():   
    opcion = ""
    
    #Se solicita al usuario que ingrese la topologia que desee experimentar
    while(True):
        try:
            num_temp = int(input("Ingrese el numero segun la topologia deseada: \n [1] \t Topologia de Complejidad Baja \n [2] \t Topologia de Complejidad Media \n"))
            if (num_temp == 1):
                opcion = 'topologia1.txt'
                break
            elif (num_temp == 2):
                opcion = 'topologia2.txt'
                break
            else:
                print("INGRESE UN NUMERO VALIDO (1 o 2) \n")
        except ValueError:
                print("INGRESE UN VALOR VALIDO (1 o 2) \n")
    
    #Leemos el archivo txt que contiene las aristas en una lista
    try:
        with open(opcion, 'r') as f:
            temp = []
            for line in f:
                temp.append(line.rstrip().split())
            f.close() 
    except OSError:
        print("No se pudo abrir/leer el archivo: ", opcion)
        sys.exit()
    
    #La cantidad de nodos ya viene indicada en cada txt
    try:
        nodos= int(temp[0][0]) 
    except IndexError as error:
        print("{} es un error en la topografía dada. Revisar el archivo".format(error))
        sys.exit()
    except ValueError as mistake:
        print("{} es un error en la topografía dada. Revisar el archivo".format(mistake))
        sys.exit()

        
    #Se solicita al usuario que ingrese el nodo origen para iniciar el recorrido
    while (True):
        try:
            fuente = int(input("Ingresa el nodo origen para aplicar el algoritmo: \n"))
            if (fuente >= 0 and fuente < nodos):                
                break
            else:
                print("{} no está dentro del rango 0 y {}".format(fuente, nodos-1))            
        except ValueError:
            print("Ingresar un numero entre 0 y {}".format(nodos-1))
            
    #instanciamos el grafo
    g = Grafo(nodos)
    #Agregamos las aristas al grafo creado usando la lista anterior
    for i,line in enumerate(temp):
        if (i != 0): 
            try:
                g.agregarArista(int(line[0]), int(line[1]), int(line[2]))  
            except IndexError as error2:
                print("{} es un error en la topografía dada. Revisar el archivo".format(error2))
                sys.exit()
            except ValueError as mistake2:
                print("{} es un error en la topografía dada. Revisar el archivo".format(mistake2))
                sys.exit()
            
    #Metricas
    
    #Metodo para calcular la cantidad de segundos que se demora el algoritmo implementado
    execution_time = timeit.timeit(lambda: g.BellmanFord(fuente), number= 1)
    print(LIGHT_GREEN + "METRICAS")
    print("1) Tiempo de ejecucion (Segundos): ")
    print(execution_time)
    #Metodo para calcular la cantidad de memoria usada
    print("2) Cantidad de memoria usada (MB): ")
    print(psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2)
    #Se imprimen la cantidad de iteraciones que tuvo que realizar el algoritmo
    print("3) Numero de iteraciones para hallar la ruta más corta")
    print(nro_repeticiones)


main()