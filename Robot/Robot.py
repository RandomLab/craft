# -*- coding: utf-8 -*-
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
root_items = []
cycles = 0
class Robot(object):
    """
        Robot :
            - Créé un Marché avec tous les éléments à disposition pour le joueur
            - sert un nouveau plateau au joueur au démarrage si son plateau (Bureau) est vide
            - met à jour le plateau toutes les 60 secondes
    """
    items = []
    root_items = []

    def __init__(self, base_path = base_path, secondes = 5):
        self.path = base_path
        self.secondes = secondes
        self.cycles = 0


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
            """
#mato grosso

            Robot.items.append(Ville(name="Sao Polo"))
            Robot.items.append(Champ(name="Champ1"))
            Robot.items.append(Champ(name="Champ2"))
            Robot.items.append(Champ(name="Champ3"))
            Robot.items.append(Foret(name="Foret1"))
            Robot.items.append(Foret(name="Foret2"))
            Robot.items.append(Foret(name="Foret3"))
            Robot.items.append(Foret(name="Foret4"))
            Robot.items.append(Foret(name="Foret5"))
            Robot.items.append(Foret(name="Foret6"))
            Robot.items.append(Foret(name="Foret7"))
            Robot.items.append(Foret(name="Foret8"))
            Robot.items.append(Foret(name="Foret9"))
            Robot.items.append(Foret(name="Foret10"))
            Robot.items.append(PuitsPetrole(name="Petrole"))
            Robot.items.append(MineCharbon(name="Charbon"))
            Robot.items.append(Mer(name="mer1"))
            Robot.items.append(Mer(name="mer2"))
            Robot.items.append(Travailleur(name="Travailleur1"))
            Robot.items.append(Travailleur(name="Travailleur2"))

            """

#texas-picardie

            addItem(Ville(name="Ville"))
            addItem(Champ(name="Champ1"))

      #      m = Mer(name="Mer1")
      #      m.save()
      #      m.spawn(Anchois, path = m.id)
      #      Robot.items.append(m)

            """
            Robot.items.append(Foret(name="Foret1"))
            Robot.items.append(Foret(name="Foret2"))
            Robot.items.append(Foret(name="Foret3"))
            Robot.items.append(Foret(name="Foret4"))
            Robot.items.append(Foret(name="Foret5"))
            Robot.items.append(Foret(name="Foret6"))
            Robot.items.append(Travailleur(name="Travailleur1"))
            Robot.items.append(Travailleur(name="Travailleur2"))
            Robot.items.append(Travailleur(name="Travailleur3"))
            Robot.items.append(Cereale(name="Cereale1"))
            Robot.items.append(Cereale(name="Cereale2"))
            Robot.items.append(Cereale(name="Cereale3"))
            """

            addItem(Foret(name="Foret1"))
            addItem(Foret(name="Foret2"))
            addItem(Foret(name="Foret3"))
            addItem(Foret(name="Foret4"))
            addItem(Foret(name="Foret5"))
            addItem(Foret(name="Foret6"))
            addItem(Travailleur(name="Travailleur1"))
            addItem(Travailleur(name="Travailleur2"))
            addItem(Travailleur(name="Travailleur3"))
            addItem(Cereale(name="Cereale1"))
            addItem(Cereale(name="Cereale2"))
            addItem(Cereale(name="Cereale3"))
            for i in range(250):
                addItem(Cereale(name="Cereale"+str(i)))


            """

#Nord-pas-de-calais Groningen

            Robot.items.append(Ville(name="Groningen"))
            Robot.items.append(Champ(name="Champ1"))
            Robot.items.append(Champ(name="Champ2"))
            Robot.items.append(Champ(name="Champ3"))
            Robot.items.append(Foret(name="Foret1"))
            Robot.items.append(Foret(name="Foret2"))
            Robot.items.append(Foret(name="Foret3"))
            Robot.items.append(Mer(name="mer1"))
            Robot.items.append(Mer(name="mer2"))
            Robot.items.append(Mer(name="mer3"))
            Robot.items.append(Mer(name="mer4"))
            Robot.items.append(Mer(name="mer5"))
            Robot.items.append(Mer(name="mer6"))
            Robot.items.append(Travailleur(name="Travailleur1"))
            Robot.items.append(Travailleur(name="Travailleur2"))

            """


            self.save()

    """
        Retourne le nombre d'items de type klass (dans tout le plateau)
        Paramètre anywhere identique à find.
        Par contre il est inverssé ici. (compte dans tout le plateau par défaut)
    """

    def countByType(self, klass, anywhere = True):
        global root_items, items
        source = root_items
        if anywhere:
            source = items
        n = 0
        for o in source:
            if klass == type(o) or klass in o.__class__.__bases__:
                n += 1
        return n


    """
        Créer des instances d'objet à partir du système de fichier
    """
    def loadFromFS(self):
        global items, root_items
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
                    addItem(o, root_path)
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
        while True:
            print("############################################")
            print("Cycle :", cycles)
            self.update()
            print("############################################")
            cycles += 1
            #Robot.cycles = self.cycles
            time.sleep(self.secondes)

    def update(self):
        # Conditions de victoire...
        #if self.countByType(Ble):
        #    alert("Whouaou")

        #if self.countByType(Foret) < 1 or self.countByType(Travailleur) >= 15:
        #    alert(text = "Ben bravo t'as gagné", title="Yeah", button = "Ok")



        self.loadFromFS()
        for item in items:
            item.update()
        self.save()



"""
    Ajouter un item à la liste du robot
"""
def addItem(what, where = base_path):
    if where == base_path:
        root_items.append(what)
    items.append(what)


"""
    Méthode static qui permet de trouver un item de type klass
    dans l'aire de jeu. Par défaut elle cherche uniquement dans
    le répertoire racine (sans parcourir les sous dossiers)

    Si anywhere = True lors de l'appel, la méthode cherchera partout

    La méthode retourne un tableau d'éléments. Vide si pas de résultat
"""

def find(klass, anywhere = False):
    r = []
    source = root_items
    if anywhere:
        source = items


    for o in source:
        if klass == type(o) or klass in o.__class__.__bases__:
            r.append(o)
    return r

"""
    Trouve un élément de type klass.
    cf find pour les paramètres
"""
def findOne(klass, anywhere = False):
    res = find(klass, anywhere)
    if len(res) > 0:
        return random.choice(res)
    else:
        return None