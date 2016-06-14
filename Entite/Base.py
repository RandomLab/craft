import os
from config import base_path
from FSM.FSM import StackFSM
import pickle
import uuid
from Robot import Robot
from Robot.FileIO import FileIO
class Base(object):
    """
        Permet de charger et de sauvegarder un object
        sur le système de fichier de l'utilisateur sous forme de fichier
    """
    data = []
    def __init__(self, name = None, path = base_path, icon = "default.bmp"):
        self.path = path
        if not name:
            self.name = self.__class__.__name__
        else:
            self.name = name
        self.id = os.path.join(self.path, self.name)
        self.brain = StackFSM(self.idle)
        if icon == "default.bmp":
            # Try to find an icon based on class name
            if os.path.isfile(os.path.join("ressources", self.__class__.__name__) + ".bmp"):
                self.icon = os.path.join("ressources", self.__class__.__name__) + ".bmp"
            else:
                self.icon = icon
        self.root = True
        self.init()
    def init(self): pass
    def checkPath(self, new_path, new_filename):
        if new_filename != ".config":
            self.path = new_path
            self.name = new_filename
            self.id = os.path.join(self.path, self.name)
            if new_path == base_path:
                self.root = True
            else:
                self.root = False
        else:
            self.root = True
    def update(self):
        self.brain.update()
    def save(self):
        FileIO.save(self)

    def remove(self):
        for e in Robot.items:
            if e.id == self.id:
                Robot.items.remove(e)
                try:
                    os.remove(self.id)
                except:
                    pass

    def idle(self): pass

    def spawn(self, klass = None, path = None):
        if path is None: path = base_path
        o = klass(name = klass.__name__ + "__" + str(uuid.uuid4()) ,path = path)
        o.save()
        return o

    def getCurrentState(self):
        return self.brain.getCurrentState().__name__

    def __str__(self):
        #return self.name + " : " + str(self.nbtravailleur) + " " + str(self.tracteur) + " " + str(self. travailleur) + " " + str(self.chimie)
        return self.name + " " + self.getCurrentState()

    def __repr__(self):
        return ", ".join([self.name, self.path, self.getCurrentState()])

class Entite(Base):
    """
        Entités
            - Ville
            - Megapole
            - Megalopole
            - CentraleThermique
            - CentraleAtom
            - CentraleSol
            - Caserne
            - BTP
            - Acierie
            - GenieMecanique
            - Arsenal
            - IndustrieChimique
            - Universite
            - Hopital
            - Aeronautique
            - Electronique
            - Assurance
            - Banque
            - GisementCharbon
            - GisementPetrole
            - GisementUranium
            - GisementMetaux
            - GisementMetauxPrecieux
            - MineCharbon
            - PuitsPetrole
            - MineUranium
            - MineMetaux
            - MineMetauxPrecieux
            - DechargeAtomique
            - Frontiere
            - Mer

            Représentation sous forme de répertoire

    """
    def countByType(self, klass, where = None, anywhere = False):
        n = len(Robot.find(klass, where = self.id, anywhere = anywhere))
        return n

    def mutate(self, klass):
        for e in Robot.items:
            if e.id == self.id:
                Robot.items.remove(e)
        self.__class__ = klass
        self.__init__(name = self.name)
        self.save()

    def save(self):
        """
        try:
            os.mkdir(os.path.join(self.path, self.name))
        except Exception as e:
            # print(e)
            pass
        pickle.dump(self, open(os.path.join(self.path, self.name, ".config"), "wb"))
        """
        FileIO.saveEntite(self)
    def load(self):
        return FileIO.loadEntite(self.id)
    def remove(self, klass):
        #o = self.findOneElement(klass, local = True)
        o = Robot.findOne(klass, where = self.id)
        if o: o.remove()

    def __str__(self):
        return self.name + " " + self.getCurrentState()
