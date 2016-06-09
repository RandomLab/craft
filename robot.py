
from config import base_path, items, cycles
import os, time

from userclass import *

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
        self.createOrLoadGame()

    def createOrLoadGame(self):
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

            items.append(Ville(name="Sao Polo"))
            items.append(Champ(name="Champ1"))
            items.append(Champ(name="Champ2"))
            items.append(Champ(name="Champ3"))
            items.append(Foret(name="Foret1"))
            items.append(Foret(name="Foret2"))
            items.append(Foret(name="Foret3"))
            items.append(Foret(name="Foret4"))
            items.append(Foret(name="Foret5"))
            items.append(Foret(name="Foret6"))
            items.append(Foret(name="Foret7"))
            items.append(Foret(name="Foret8"))
            items.append(Foret(name="Foret9"))
            items.append(Foret(name="Foret10"))
            items.append(PuitsPetrole(name="Petrole"))
            items.append(MineCharbon(name="Charbon"))
            items.append(Mer(name="mer1"))
            items.append(Mer(name="mer2"))
            items.append(Travailleur(name="Travailleur1"))
            items.append(Travailleur(name="Travailleur2"))

            """

#texas-picardie
            """
            items.append(Ville(name="Austin"))
            items.append(Champ(name="Champ2"))
            items.append(Mer(name="Mer1"))
            items.append(PuitsPetrole(name="Puits1"))
            items.append(PuitsPetrole(name="Puits2"))
            items.append(PuitsPetrole(name="Puits3"))
            items.append(PuitsPetrole(name="Puits4"))
            items.append(PuitsPetrole(name="Puits5"))
            items.append(PuitsPetrole(name="Puits6"))
            items.append(MineMetauxPrecieux(name="MineP1"))
            items.append(MineUranium(name="MineU1"))
            items.append(Foret(name="Foret1"))
            items.append(Foret(name="Foret2"))
            """
            items.append(Champ(name="Champ1"))

            items.append(Cereale())
            items.append(Travailleur(name="Travailleur1"))
            items.append(Travailleur(name="Travailleur2"))
            items.append(Travailleur(name="Travailleur3"))
            items.append(Travailleur(name="Travailleur4"))


            """

#Nord-pas-de-calais Groningen

            items.append(Ville(name="Groningen"))
            items.append(Champ(name="Champ1"))
            items.append(Champ(name="Champ2"))
            items.append(Champ(name="Champ3"))
            items.append(Foret(name="Foret1"))
            items.append(Foret(name="Foret2"))
            items.append(Foret(name="Foret3"))
            items.append(Mer(name="mer1"))
            items.append(Mer(name="mer2"))
            items.append(Mer(name="mer3"))
            items.append(Mer(name="mer4"))
            items.append(Mer(name="mer5"))
            items.append(Mer(name="mer6"))
            items.append(Travailleur(name="Travailleur1"))
            items.append(Travailleur(name="Travailleur2"))

            """


            self.save()

    def countByType(self, klass):
        n = 0
        for o in items:
            if klass == type(o) or klass in tmp.__class__.__bases__:
                n += 1
        return n

    def loadFromFS(self):
        global items
        items = []

        for root_path, folders, filenames in os.walk(self.path):
            try:
                filenames.remove('.DS_Store')
            except:
                pass
            for f in filenames:
                current_file = os.path.join(root_path, f)
                o = FileIO.load(current_file)
                o.checkPath(root_path, f)
                items.append(o)

    def save(self):
        for o in items:
            o.save()

    def run(self):
        global cycles, items
        while True:
            print("############################################")
            print("Cycle :", cycles)
            self.update()
            print("############################################")
            cycles += 1
            cycles = cycles
            time.sleep(self.secondes)

    def update(self):
        global items
        # Conditions de victoire...
        #if self.countByType(Ble):
        #    alert("Whouaou")

        self.loadFromFS()
        for item in items:
            item.update()
        self.save()
