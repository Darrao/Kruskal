from math import inf
from tkinter import *
from random import randint



class graphe:
    """classe simpliste de mémorisation d'un graphe.
        Les sommets sont des String et les distances entières.
        Pas d'affichage graphique"""
    __sommets ={}

    def __init__(self, liste_sommets,his, matrice=[[]]):
        """List[String]->graphe
            Prépare un graphe donc les sommets seront les éléments de
            liste_sommets, avec la matrice d'adjacence matrice ou
            sans arête si matrice = [[]]"""
        for s in liste_sommets:
            self.__sommets[s] = []
        if matrice != [[]]:
            for i in range(len(matrice)):
                for j in range(i+1, len(matrice)):
                    if matrice[i][j] != inf :
                        self.ajouter_arete(list(self.__sommets.keys())[i],list(self.__sommets.keys())[j],matrice[i][j])
        self.stokdis = {}
        self.parents = {} 
        self.pierre = his
        self.g = 0
        self.h = 0
        self.f = 0

    def __repr__(self):
        return str(self.__sommets)
    
    def ajouter_arete(self, s1, s2, dist):
        """String*String*int->None
            Ajoute une arête entre s1 et s2 de poids dist dans le graphe"""
        vs1 = self.voisins(s1)
        vs2 = self.voisins(s2)
        if s1 in vs2 :
            for i in range(len(vs2)) :
                if self.__sommets[s2][i][0] == s1 :
                    self.__sommets[s2][i][1] = dist
            for i in range(len(vs1)) :
                if self.__sommets[s1][i][0] == s2 :
                    self.__sommets[s1][i][1] = dist
        else :       
            self.__sommets[s1].append([s2,dist])
            self.__sommets[s2].append([s1,dist])
    
    def ajouter_sommet(self, s):
        """String->None
            Ajoute le sommet s au graphe, sans aucun voisins"""
        if s not in self.__sommets.keys():
            self.__sommets[s] = []

    def voisins(self, s):
        """String->List[String]
            retourne la liste des voisins du sommet s"""
        return [v[0] for v in self.__sommets[s]]

    def distance(self, s1, s2):
        """String*String->int
            Retourne la distance entre s1 et s2 s'ils sont voisins
            et infini sinon"""
        if s2 in self.voisins(s1):
            for i in range(len(self.voisins(s1))) :
                if self.__sommets[s1][i][0] == s2 :
                    return self.__sommets[s1][i][1]
        else : 
            return inf

    def matrice_adjacence(self):
        """None->List[List[int]]
            Retourne la matrice d'adjacence du graphe"""
        n = len(self.__sommets.keys())
        matrice = [[0 for _ in range(n)] for _ in range(n)]
        for s1 in range(n):
            for s2 in range(n):
                matrice[s1][s2] = self.distance(list(self.__sommets.keys())[s1], list(self.__sommets.keys())[s2])
        return matrice

    def Parcours (self, S, L):
        pe = ""
        V = self.voisins(S)
        for i in V[:]:
            if i not in L:
                V.remove(i)
        pe += S
        L.remove(S)
        for i in V:
            if i in L:
                pe += self.Parcours(i, L)
        return pe

    def dijkstra(self, S):
        """ String -> Dict[String : (int, String)]
            renvoie dictionnaire dont clefs = sommets du graphe et les valeurs sont formées par le couple, distance à S et prédécesseur sur le chemin."""
        dict = {}
        non_visite = list(self.__sommets.keys())
        for s in self.__sommets:
            if s == S :
                dict[s] = (0, S)
            else :
                dict[s] = (inf, S)
        while len(non_visite) != 0:
            min = (inf, S)
            sommet_courant = ""
            for s in non_visite:
                if dict[s][0] < min[0] :
                    min = dict[s]
                    sommet_courant = s
            for v in self.voisins(sommet_courant):
                if v in non_visite :
                    d = dict[sommet_courant][0] + self.distance(sommet_courant, v)
                    if d < dict[v][0] :
                        dict[v] = (d, sommet_courant)
            non_visite.remove(sommet_courant)
        return dict

    def aStarAlgo(self, debut, fin):
        self.visite = set(debut)
        self.non_visi = set()
        self.stokdis[debut] = 0
        self.parents[debut] = debut
        while len(self.visite) > 0:
            n = None
            for v in self.visite:
                if n == None or self.stokdis[v] + self.heuristic(v) < self.stokdis[n] + self.heuristic(n):
                    n = v
            if n == fin or self.__sommets[n] == None:
                pass
            else:
                for (m, long) in self.av_voisin(n, self.__sommets):
                    if m not in self.visite and m not in self.non_visi:
                        self.visite.add(m)
                        self.parents[m] = n
                        self.stokdis[m] = self.stokdis[n] + long
                    else:
                        if self.stokdis[m] > self.stokdis[n] + long:  # maj m
                            self.stokdis[m] = self.stokdis[n] + long  # change parent m a n
                            self.parents[m] = n
                            if m in self.non_visi:
                                self.non_visi.remove(m)
                                self.visite.add(m)
            if n == None:
                print('pas de chemin')
                return None
            if n == fin:
                self.path = []
                while self.parents[n] != n:
                    self.path.append(n)
                    n = self.parents[n]

                self.path.append(debut)
                self.path.reverse()
                print('chemin trouve:', self.path)
                return self.path
            self.visite.remove(n) 
            self.non_visi.add(n)
        print('pas de chemin')
        return None

    def av_voisin(self,v, graphe): 
        if v in graphe:
            return graphe[v]
        else:
            return None

    def heuristic(self,n):
        H_dist = self.pierre
        return H_dist[n]

    def test(self):
        return self.__sommets


if __name__ == "__main__":
    G = graphe(["A", "B", "C", "D"],{'A': 43,'B': 3,'C': 99,'D': 23,'E': 10,'F': 5,})
    #print(G)
    G.ajouter_arete("A", "B", 10)
    G.ajouter_arete("A", "C", 1 )
    G.ajouter_arete("B", "C", 5 )
    G.ajouter_arete("B", "D", 4 )
    G.ajouter_arete("D", "C", 3 )
    #print(G)
    G.ajouter_sommet("E")
    G.ajouter_arete("C", "E", 2)
    #print(G)
    #print(G.voisins("A"))
    G.ajouter_arete("A", "B", 9)
    #print(G)
    #print(G.distance("A", "B"))
    #print(G.matrice_adjacence(),)
    H = graphe(["A", "B", "C", "D", "E"],{'A': 43,'B': 3,'C': 99,'D': 23,'E': 10,'F': 5,}, G.matrice_adjacence())
    print(H)
    #print("parcours :", H.Parcours("A", ["A", "B", "C", "D", "E"]))
    #print(G.dijkstra("B"))
    G.aStarAlgo("A", "B")
    G.aStarAlgo("A", "C")
    G.aStarAlgo("A", "D")
    G.aStarAlgo("A", "E")
    G.aStarAlgo("B", "A")
    G.aStarAlgo("B", "C")
    G.aStarAlgo("B", "D")
    G.aStarAlgo("B", "E")
    G.aStarAlgo("B", "F")
    print(G.test())