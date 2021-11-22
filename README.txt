Simplemente correr el archivo desde su IDE de preferencia

Las librerías usadas son:
import numpy as np
import timeit
import os, psutil

En caso no las tenga instalarlas desde su terminal usando:

pip install {nombre del paquete}


Se esta usando 2 archivos txt para leer el grafo.
Dado que Bellman Ford solo trabaja con grafos dirigidos, 
he tenido que repetir las aristas una vez adicional para que
el programa pueda entender bien las conexiones entre nodos.
