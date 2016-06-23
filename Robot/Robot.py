# -*- coding: utf-8 -*-

"""
    TODO:

    afficher le score en Soja de chaque joueur via la fenetre TK
    
    fichier config a éditer par chaque joueur
   
    conditions de victoire :
        le jeu stoppe quand Foret(entite) < 1
            confère deux points de victoire
        le robot compte alors le nombre de Soja(base)
            le joueur qui en a le plus gagne un point de victoire
        puis le robot compte le nombre de TigresDeSumatra(bio)
            chaque joueur qui en a plus de 5 gagne un point de victoire

    lancement du jeu via signal MIDI


"""



from config import base_path

import time, os, sys
import uuid
import random
import pickle
from pymsgbox import alert
from FSM.FSM import StackFSM

from .classes import *
from .FileIO import FileIO

items = []
listeBase = [Cereale, Soja, Beton, Acier, Travailleur, Ingenieur, Soldat, Poisson, Metal, Phosphate, Uranium, Charbon, Petrole, Calcaire, Arme, Vehicule, Pesticide, Electricite]
root_items = []
cycles = 0

class Robot(object):
    """
        Robot :
            - Créé un Marché avec tous les éléments à disposition pour le joueur
            - sert un nouveau plateau au joueur au démarrage si son plateau (Bureau) est vide
            - met à jour le plateau toutes les 60 secondes
    """
    def __init__(self, base_path = base_path, secondes = 5):
        self.path = base_path
        self.secondes = secondes
        self.cycles = 0
        self.win = False


        self.createOrLoadGame()

    def createOrLoadGame(self):
        # only in macos
        #files = os.listdir(self.path)
        #for f in files:
        #    if f == ".DS_Store":
        #        os.remove(os.path.join(self.path, f))
        filenames = os.listdir(self.path)
        try:
            filenames.remove('.DS_Store')
        except:
            pass

        if not filenames:
            print("Create new game")

# patrimoine de départ ici

# game n°1
            addItem(Ville())
            addItem(Champ())

            addItem(Foret())
            addItem(Foret())
            addItem(Foret())
            addItem(Foret())
            addItem(Foret())
            addItem(Foret())

            addItem(Travailleur())
            addItem(Travailleur())
            addItem(Travailleur())
            addItem(Travailleur())
            addItem(Travailleur())

            addItem(Cereale())
            addItem(Cereale())
            addItem(Cereale())
            addItem(Cereale())

            self.save()

    """
        Retourne le nombre d'items de type klass (dans tout le plateau)
        Paramètre anywhere identique à find.
        Par contre il est inverssé ici. (compte dans tout le plateau par défaut)
    """
    """
    def countByType(self, klass, anywhere = True):
        global items
        n = 0
        for o in items:
            if klass == type(o) or klass in o.__class__.__bases__:
                n += 1
        return n
    """

    def countByType(self, klass, anywhere = True):

        return len(Robot.find(klass, anywhere = anywhere))

    """
        Créer des instances d'objet à partir du système de fichier
    """
    def loadFromFS(self):
        global items
        items = []
        Base.counts = {}
        for root_path, folders, filenames in os.walk(self.path):
            try:
                filenames.remove('.DS_Store')
            except Exception as e:
                pass
            for f in filenames:
                current_file = os.path.join(root_path, f)
                try:
                    o = FileIO.load(current_file)
                    o.checkPath(root_path, f)
                    Base.register(o)
                    addItem(o)
                except Exception as e:
                    print("ERROR", e)
    """
        Sauvegarder le plateau
    """
    def save(self):
        global items
        for o in items:
            o.save()

    def run(self):
        global cycles
        #while not self.win :
        print("############################################")
        print("Cycle :", cycles)
        self.update()
        print("############################################")
        cycles += 1
        #time.sleep(self.secondes)
        """
        self.loadFromFS()
        for item in items:
            print(item)
        """
        #alert(text = "Ben bravo t'as gagné", title="Yeah", button = "Ok")

    def update(self):
        global items
        # Conditions de victoire...
        #if self.countByType(Ble):
        #    alert("Whouaou")

        #if self.countByType(Foret) < 1 or self.countByType(Travailleur) >= 15:
        #    alert(text = "Ben bravo t'as gagné", title="Yeah", button = "Ok")



        self.loadFromFS()
        for item in items:
            item.update()
        self.save()

        if len(find(Centrale)) >= 1 and len(find(Uranium)) >= 1 and len(find(Soldat)) >= 10 :
            win = True



"""
    Ajouter un item à la liste du robot
"""
def addItem(what):
    global items
    items.append(what)


"""
    Méthode static qui permet de trouver un item de type klass
    dans l'aire de jeu. Par défaut elle cherche uniquement dans
    le répertoire racine (sans parcourir les sous dossiers)

    Si anywhere = True lors de l'appel, la méthode cherchera partout

    La méthode retourne un tableau d'éléments. Vide si pas de résultat
"""


def find(what, where = None, anywhere = False):
    global items
    r = []
    #where = base_path + "/Champ1"
    for o in items:
        if where:
            if o.path == where and (what == type(o) or what in o.__class__.__bases__):
                r.append(o)
        else:
            if anywhere:
                if what == type(o) or what in o.__class__.__bases__:
                    r.append(o)
            else:
                if o.root and (what == type(o) or what in o.__class__.__bases__):
                    r.append(o)
    return r

"""
    Trouve un élément de type klass.
    cf find pour les paramètres
"""
def findOne(klass, where = None, anywhere = False):
    global items
    res = find(klass, where, anywhere)
    if len(res) > 0:
        return random.choice(res)
    else:
        return None
