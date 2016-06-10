import os
from config import base_path
from FSM.FSM import StackFSM
import pickle
import uuid
from Robot import Robot
class Base(object):
    """
        Permet de charger et de sauvegarder un object
        sur le système de fichier de l'utilisateur sous forme de fichier
    """
    data = []
    def __init__(self, name = None, path = base_path, icon = "default.png"):
        self.path = path
        if not name:
            self.name = self.__class__.__name__
        else:
            self.name = name
        self.id = os.path.join(self.path, self.name)
        self.brain = StackFSM(self.idle)
        self.icon = icon
        self.init()
    def init(self): pass
    def checkPath(self, new_path, new_filename):
        if new_filename != ".config":
            self.path = new_path
            self.name = new_filename
            self.id = os.path.join(self.path, self.name)
    def update(self):
        self.brain.update()
    def save(self):
        pickle.dump(self, open(self.id, "wb"))

    def update_file(self):
        for e in Robot.items:
            if e.id == self.id:
                Robot.items.remove(e)
                Robot.items.append(self)
                self.update()
                self.save()
    def remove(self):
        print("REMOVE", self)
        for e in Robot.items:
            if e.id == self.id:
                Robot.items.remove(e)
                try:
                    os.remove(self.id)
                except:
                    pass
        for e in Robot.root_items:
            if e.id == self.id:
                Robot.root_items.remove(e)


    def idle(self): pass

    #@classmethod
    def findOneElement(self, klass):
        for root_path, folders, filenames in os.walk(base_path):
            for t in filenames:
                try:
                    tmp = pickle.load(open(os.path.join(base_path, t), "rb"))
                    if klass == type(tmp) or klass in tmp.__class__.__bases__:
                        return tmp
                except:
                    pass
        return None


    def find(self, klass):
        for o in Robot.items:
            if klass == type(o) or klass in o.__class__.__bases__:
                return o
        return None


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

    def countByType(self, klass):
        n = 0
        for root_path, folders, filenames in os.walk(self.id):
            for t in filenames:
                try:
                    tmp = pickle.load(open(os.path.join(self.id, t), "rb"))
                    if klass == type(tmp) or klass in tmp.__class__.__bases__:
                        n += 1
                except:
                    pass
        return n



    def mutate(self, klass):
        for e in Robot.items:
            if e.id == self.id:
                Robot.items.remove(e)
        self.__class__ = klass
        self.__init__(name = self.name)
        self.save()
    # Peut etre fusionnée avec celle de Base. !?
    def findOneElement(self, klass, local = False):
        if local:
            p = self.id
        else:
            p = self.path
        for root_path, folders, filenames in os.walk(p):
            for t in filenames:
                try:
                     tmp = pickle.load(open(os.path.join(p, t), "rb"))
                     if klass == type(tmp) or klass in tmp.__class__.__bases__:
                         return tmp
                except:
                    print("Oups")
        return None
    # TODO :implémenter ces deux méthodes !
    # Elles seront utiliser pour trouver un ou des éléments de type
    # what à l'interrieur de l'entité.
    def find(self, what):
        pass
    def findOne(self, what):
        return self.find(what)[0]


    def save(self):
        try:
            os.mkdir(os.path.join(self.path, self.name))
        except Exception as e:
            # print(e)
            pass
        pickle.dump(self, open(os.path.join(self.path, self.name, ".config"), "wb"))

    def remove(self, klass):
        o = self.findOneElement(klass, local = True)
        if o: o.remove()

    def __str__(self):
        return self.name + " " + self.getCurrentState()
