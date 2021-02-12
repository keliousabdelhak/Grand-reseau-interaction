
from collections import deque
import numpy as np
import time
import os, psutil
import sys

sys.setrecursionlimit(10**6)
arg=sys.argv

fonc=str(arg[1])
file=str(arg[2])
estimNbAretes=int(arg[3])
numSommetDepart=int(arg[4])

class Graph:
 
    def __init__(self, vertices):
        #constructeur du graph
        self.vertices = vertices
        self.adj = {i: [] for i in range(self.vertices)}
 
    def addEdge(self, u, v):
        self.adj[u].append(v)
        self.adj[v].append(u)
 
   
    def BFS(self, u,getMilieu=False,m=0):
        # getMilieu=True en parametre cela nous permet de trouver le sommet du milieu de chemain (exo2)
        
        visited = [False for i in range(self.vertices + 1)]
       
        distance = [-1 for i in range(self.vertices + 1)]
 
     
        distance[u] = 0
      
        queue = deque()
        queue.append(u)
       
        visited[u] = True
 
        while queue:
            front = queue.popleft()
            for i in self.adj[front]:
                if not visited[i]:
                    visited[i] = True                   
                    distance[i] = distance[front]+1
                    queue.append(i)
 
        maxDis = 0

        if getMilieu==False :
            for i in range(self.vertices):
                if distance[i] > maxDis:
                    maxDis = distance[i]
                    nodeIdx = i
        else:
            for i in range(self.vertices):
                if distance[i] ==m :
                    maxDis = distance[i]
                    nodeIdx = i

        return nodeIdx, maxDis
 
  
    def double_bfs(self,d):
        # on fait appel au bfs 2 fois 
        node, Dis = self.BFS(d)
        node_2, LongDis = self.BFS(node)
        return [node,node_2,LongDis]
    
    def double_double_bfs(self,d):
        doublBFS= self.double_bfs(d)
        #on recupre le sommet du milieu
        distance_m=int(round((doublBFS[2])/2))
        #on applique le bfs a partir de m
        bfs_m=self.BFS(doublBFS[0],True,distance_m)
        resault = self.double_bfs(bfs_m[0])

        return resault
    
    def sum_sweep(self,d):
        ecc_u=self.BFS(d)
        ecc_v=self.BFS(ecc_u[0])
        ecc_w=self.BFS(ecc_v[0])
        ecc_x=self.BFS(ecc_w[0])

        distances=[ecc_u[1],ecc_v[1],ecc_w[1],ecc_x[1]]
        return max(distances)
    
    
    def getComposante(self, temp, v, visited):
        # retourne les sommet d'une composante 
        visited[v] = True
        temp.append(v)
        for i in self.adj[v]:
            if visited[i] == False:
                temp = self.getComposante(temp, i, visited)
        return temp


    def getSommetPlusGrandeComposante(self):
        #retounre le sommet de la plus grande composante connexe
        visited = []
        sommet=None
        lenght=0
        for i in range(self.vertices):
            visited.append(False)
        for v in range(self.vertices):
            if visited[v] == False:
                temp = []
                getComp=self.getComposante(temp, v, visited)
                
                if len(getComp)>lenght:
                    sommet=getComp[0]
                    lenght=len(getComp)
        return sommet

    def exact(self,d):
        # nous n'avons pas compris cet exercice 
        return "Not-Implemented"



 
 

#-------------- Main -------------------------

# Lire les donnees 
data = np.loadtxt(file,dtype=int)

# Construction du graph 
G= Graph(np.amax(data)+1)
for sommet in data:
    G.addEdge(sommet[0],sommet[1])


# different fonctions 

if fonc == "2-sweep":
    resultat=G.double_bfs(numSommetDepart)
    print("v=",resultat[0])
    print("w=",resultat[1])
    print("diam>=",resultat[2])


if fonc == "4-sweep":
    resultat=G.double_double_bfs(numSommetDepart)
    print("diam>=",resultat[2])


if fonc == "sum-sweep":
    resultat=G.sum_sweep(numSommetDepart)
    print("diam>=",resultat)


if fonc == "diametre":
    resultat=G.exact(numSommetDepart)
    print("diam>=",resultat)

