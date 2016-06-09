# -*- coding: utf-8 -*-
import time, os, sys
import uuid
import random
import pickle
from pymsgbox import alert
from FSM import FSM, StackFSM

"""
    # TODO :

    Icon
    Dossier Partagé

    travailleurs qui peuvent manger partout

    sam:
    implémenter la classe d'anchois (et virer tout le bazar dans la mer)

    implémenter le craft de ville (champ->ville)

    ça serait bien que les anchois changent de nom quand ils sont vieux


"""

base_path = "/Users/samuel/Desktop"
#base_path = "/home/jdpillon/Bureau/samuel"

class FileIO(object):
    @staticmethod
    def loadStegano(f):
        im = Image.open(f)
        o = stepic.decode(im)
        o = bytes(o, 'UTF-8')
        return pickle.loads(o)

    @staticmethod
    def saveStegano(o):
        s = str(pickle.dumps(o))
        im = Image.open(os.path.join("ressources",o.icon))
        secret = stepic.encode(im, s)
        secret.save(o.id + ".png")
    @staticmethod
    def saveBinaryFile(o):
        pickle.dump(o, open(o.id, "wb"))
    @staticmethod
    def loadBinaryFile(f):
        try:
            return pickle.load(open(f, "rb"))
        except:
            return None
    @staticmethod
    def save(o):
        FileIO.saveBinaryFile(o)
    @staticmethod
    def load(f):
        return FileIO.loadBinaryFile(f)

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
        self.save()
        for e in Robot.items:
            if e.id == self.id:
                Robot.items.remove(e)
                Robot.items.append(self)


    def remove(self):
        for e in Robot.items:
            if e.id == self.id:
                Robot.items.remove(e)
                os.remove(self.id)

    def idle(self): pass

    #@classmethod
    def findOneElement(self, klass):
        for root_path, folders, filenames in os.walk(base_path):
            for t in filenames:
                try:
                     tmp = pickle.load(open(os.path.join(self.path, t), "rb"))
                     if klass == type(tmp) or klass in tmp.__class__.__bases__:
                         return tmp
                except:
                    pass
        return None

    def spawn(self, klass = None, path = None):
        if path is None: path = base_path
        o = klass(name = klass.__name__ + "__" + str(uuid.uuid4()) ,path = path)
        o.save()
        return o

    def getCurrentState(self):
        return self.brain.getCurrentState().__name__
    """
    @classmethod
    def findOne(self):
        print("findOne", self.name)

    @classmethod
    def find(self):
        print("find", self.name)
    """
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
                    pass
        return None


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

class Robot(object):
    """
        Robot :
            - Créé un Marché avec tous les éléments à disposition pour le joueur
            - sert un nouveau plateau au joueur au démarrage si son plateau (Bureau) est vide
            - met à jour le plateau toutes les 60 secondes
    """
    cycles = 0
    items = []
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

            Robot.items.append(Ville(name="Austin"))
            Robot.items.append(Champ(name="Champ1"))
            Robot.items.append(Champ(name="Champ2"))

            m = Mer(name="Mer1")
            m.spawn(Anchois, path = m.path)
            Robot.items.append(m)

            Robot.items.append(Chimie(name="Chimie"))
            Robot.items.append(Bestiau(name="Vache"))
            Robot.items.append(GisementUranium(name="MineU1"))
            Robot.items.append(Foret(name="Foret1"))
            Robot.items.append(Foret(name="Foret2"))
            Robot.items.append(Travailleur(name="Travailleur1"))
            Robot.items.append(Travailleur(name="Travailleur2"))
            Robot.items.append(Travailleur(name="Travailleur3"))
            Robot.items.append(Acier(name="Acier1"))
            Robot.items.append(Acier(name="Acier2"))
            Robot.items.append(Acier(name="Acier3"))
            Robot.items.append(Acier(name="Acier4"))
            Robot.items.append(Cereale(name="miam"))
            Robot.items.append(Cereale(name="miam2"))
            Robot.items.append(Cereale(name="miam3"))


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

    def countByType(self, klass):
        n = 0
        for o in Robot.items:
            if klass == type(o) or klass in tmp.__class__.__bases__:
                n += 1
        return n

    def loadFromFS(self):
        Robot.items = []

        for root_path, folders, filenames in os.walk(self.path):
            try:
                filenames.remove('.DS_Store')
            except:
                pass
            for f in filenames:
                current_file = os.path.join(root_path, f)
                if f != ".config":
                    o = FileIO.load(current_file)
                    o.checkPath(root_path, f)
                    Robot.items.append(o)
                else:
                    o = pickle.load(open(current_file, "rb"))
                    o.checkPath(root_path, f)
                    Robot.items.append(o)
                    #pass

    def save(self):
        for o in Robot.items:
            o.save()

    def run(self):
        while True:
            print("############################################")
            print("Cycle :", self.cycles)
            self.update()
            print("############################################")
            self.cycles += 1
            Robot.cycles = self.cycles
            time.sleep(self.secondes)

    def update(self):
        # Conditions de victoire...
        #if self.countByType(Ble):
        #    alert("Whouaou")

        self.loadFromFS()
        for item in Robot.items:
            item.update()
        self.save()

"""
#ce tableau tu peux t'en servir pour piocher des ressources au hasard
entites = [Champ, Monoculture, Elevage, ElevageIntensif, BTP, Hopital, Universite, CentraleSol, CentraleAtom, CentraleThermique, GenieMecanique, Arsenal, IndustrieChimique, Acierie, Aeronautique, Electronique, Banque, Assurance, GisementPetrole, GisementCharbon, GisementMetaux, GisementMetauxPrecieux, GisementUranium, MineCharbon, PuitsPetrole, MineUranium, MineMetaux, MineMetauxPrecieux, Ville, Megapole, Megalopole, Foret, Mer, DechargeAtomique, Frontiere]
bio = [Pollinisateur, Mouton, Boeuf, Volaille, Porc, Anchois, Anguille, Baleine, Carpe, Colin, Hareng, Maquereau, Morue, Sardine, Saumon, Thon, Truite, Coton, Lin]
nourriture = [Mouton, Boeuf, Volaille, Porc, Poisson, Mais, Millet, Patate, Riz, Seigle, Soja, Sorgho, Ble]
fossile = [Bois, Charbon, Petrole, Uranium, Metaux, MetauxPrecieux]
produits = [Tracteur, VehiculeThermique, VehiculeElectrique, BateauUsine, Acier, Arme, Avion, Beton, Chimie, DechetRadioactif, Electricite, Fumier, Fusee, Ordinateur, Sante]
vivants = [Travailleur, Ingenieur, Soldat]
"""

########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################

class Ville(Entite):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.nbTravailleur = 0
        self.nbVivant = 0
        self.nbNourriture = 0
        self.nbBois = 0
        self.nbBeton = 0
        self.nbVehicule = 0
        self.nbAcier = 0
        self.nbCharbon = 0
        self.nbPetrole = 0
        self.produit = Travailleur

    def idle(self):

#il execute les if de manière séquentielle le mec
#c'est le dernier IF VRAI qui a raison
        if self.nbNourriture >= 1 and self.nbVivant >= 1 : self.brain.setState(self.pop)
        if self.nbBois >= 5 and self.nbTravailleur >= 4 : self.brain.setState(self.newBTP)
        if self.nbBois >= 8 and self.nbTravailleur >= 4 : self.brain.setState(self.newAcierie)
        if self.nbBois >= 5 and self.nbTravailleur >= 4 and self.nbAcier >= 1 : self.brain.setState(self.newGenieMecanique)
        if self.nbBois >= 5 and self.nbTravailleur >= 2 and self.nbCharbon >= 1 or self.nbPetrole >= 1 : self.brain.setState(self.newCentraleThermique)
        if self.nbBeton >= 10 and self.nbVehicule >= 10 : self.mutate(Megapole)

    def pop(self):
        self.spawn(self.produit)
        if self.nbNourriture <1 or self.nbVivant <1 :
            self.brain.setState(self.idle)
        self.idle()

#alors ce self.idle() c'est un peu chelou mais c'est pour l'aider à sortir de la boucle si jamais
#le client veut fabriquer un truc dans sa ville.

    def newBTP(self):
        newbtp = self.spawn(BTP)
        for i in range(5):
            self.remove(Bois)
        for u in range(4):
            self.remove(Travailleur)
            self.spawn(Travailleur, newbtp.id)

        if self.nbBois < 5 or self.nbTravailleur < 4:
            self.brain.setState(self.idle)
            self.save()

        self.idle()


    def newAcierie(self):
        newacierie = self.spawn(Acierie)
        for i in range(8):
            self.remove(Bois)
        for u in range(4):
            self.remove(Travailleur)
            self.spawn(Travailleur, newacierie.id)

        if self.nbBois < 8 or self.nbTravailleur < 4:
            self.brain.setState(self.idle)
            self.save()

        self.idle()

    def newGenieMecanique(self):
        newgeniemecanique = self.spawn(GenieMecanique)
        for i in range(5):
            self.remove(Bois)
        for u in range(4):
            self.remove(Travailleur)
            self.spawn(Travailleur, newgeniemecanique.id)

        self.remove(Acier)

        if self.nbBois < 5 or self.nbTravailleur < 4 or self.nbAcier < 1 :
            self.brain.setState(self.idle)
            self.save()

        self.idle()

    def newCentraleThermique(self):
        newcentralethermique= self.spawn(CentraleThermique)
        for i in range(5):
            self.remove(Bois)
        for u in range(2):
            self.remove(Travailleur)
            self.spawn(Travailleur, newcentralethermique.id)

        self.remove(Acier)

        if self.nbBois < 5 or self.nbTravailleur < 2 or self.nbPetrole < 1 and self.nbCharbon < 1 :
            self.brain.setState(self.idle)
            self.save()

        if self.nbPetrole >= 1 :
            self.remove(Petrole)
        else :
            self.remove(Charbon)


    def update(self):
        # update Ville here
        self.nbTravailleur = self.countByType(Travailleur)
        self.nbNourriture = self.countByType(Nourriture)
        self.nbBois = self.countByType(Bois)
        self.nbBeton = self.countByType(Beton)
        self.nbVehicule = self.countByType(Vehicule)
        self.nbCoton = self.countByType(Coton)
        self.nbLin = self.countByType(Lin)
        self.nbAcier = self.countByType(Acier)
        self.nbCharbon = self.countByType(Charbon)
        self.nbPetrole = self.countByType(Petrole)
        self.nbVivant = self.countByType(Vivant)

        self.brain.update()

class BTP(Entite):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.nbTravailleur = 0
        self.produit = Beton
    def idle(self):
        if self.nbTravailleur >= 2:
            self.brain.setState(self.production)
    def production(self):
        self.spawn(self.produit)
        if self.nbTravailleur < 2:
            self.brain.setState(self.idle)

    def update(self):
        # update BTP here
        self.nbTravailleur = self.countByType(Travailleur)
        self.brain.update()

class CentraleThermique(Entite):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.nbIngenieur = 0
        self.nbFossile = 0
        self.produit = Electricite
    def idle(self):
        if self.nbIngenieur >= 2 and self.nbFossile >= 1:
            self.brain.setState(self.production)
    def production(self):
        self.spawn(self.produit)
        if self.nbIngenieur < 2 or self.nbFossile < 1:
            self.brain.setState(self.idle)

    def update(self):
        self.nbIngenieur = self.countByType(Ingenieur)
        self.nbFossile = self.countByType(Fossile)
        self.brain.update()

class Acierie(Entite):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.nbTravailleur = 0
        self.nbCharbon = 0
        self.nbMetaux = 0
        self.produit = Acier
    def idle(self):
        if self.nbTravailleur >= 4 and self.nbCharbon >= 1 and self.nbMetaux >= 1:
            self.brain.setState(self.production)
    def production(self):
        self.spawn(self.produit)
        if self.nbTravailleur < 4 or self.nbCharbon < 1 or self.nbMetaux < 1:
            self.brain.setState(self.idle)

    def update(self):
        self.nbTravailleur = self.countByType(Travailleur)
        self.nbCharbon = self.countByType(Charbon)
        self.nbMetaux = self.countByType(Metaux)
        self.brain.update()

class GenieMecanique(Entite):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.nbTravailleur = 0
        self.nbAcier = 0
        self.nbPetrole = 0
        self.nbMetauxPrecieux = 0

    def idle(self):

        condition_VTH = self.nbPetrole >= 1 and self.nbAcier >= 1 and self.nbTravailleur >= 4
        condition_VTE = self.nbMetauxPrecieux >= 1 and self.nbAcier >= 1 and self.nbTravailleur >= 4
        condition_Tracteur = self.nbPetrole >= 2 and self.nbAcier >= 1 and self.nbTravailleur >= 4
        condition_BateauUsine = self.nbPetrole >= 2 and self.nbAcier >= 2 and self.nbTravailleur >= 4

        if condition_VTH : self.brain.setState(self.newVTH)
        if condition_VTE : self.brain.setState(self.newVTE)
        if condition_Tracteur : self.brain.setState(self.newTracteur)
        if condition_BateauUsine : self.brain.setState(self.newBateauUsine)


    def newVTH(self):
        self.spawn(VehiculeThermique)
        self.remove(Petrole)
        self.remove(Acier)
        if self.nbTravailleur < 4 or self.nbPetrole < 1 or self.nbAcier < 1 :
            self.brain.setState(self.idle)
        self.idle()

    def newVTE(self):
        self.spawn(VehiculeElectrique)
        self.remove(MetauxPrecieux)
        self.remove(Acier)
        if self.nbTravailleur < 4 or self.nbMetauxPrecieux < 1 or self.nbAcier < 1 :
            self.brain.setState(self.idle)
        self.idle()

    def newTracteur(self):
        self.spawn(Tracteur)
        for x in range(2):
            self.remove(Petrole)
        self.remove(Acier)
        if self.nbTravailleur < 4 or self.nbPetrole < 2 or self.nbAcier < 1 :
            self.brain.setState(self.idle)
        self.idle()

    def newBateauUsine(self):
        self.spawn(BateauUsine)
        for x in range(2):
            self.remove(Petrole)
            self.remove(Acier)
        if self.nbTravailleur < 4 or self.nbPetrole < 2 or self.nbAcier < 2 :
            self.brain.setState(self.idle)
        self.idle()

    def update(self):
        self.nbTravailleur = self.countByType(Travailleur)
        self.nbPetrole = self.countByType(Petrole)
        self.nbAcier = self.countByType(Acier)
        self.nbMetauxPrecieux = self.countByType(MetauxPrecieux)
        self.brain.update()

class Megapole(Entite):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.nbTravailleur = 0
        self.nbVivant = 0
        self.nbIngenieur = 0
        self.nbBeton = 0
        self.nbVehiculeThermique = 0
        self.nbSoldat = 0
        self.nbAcier = 0
        self.nbPetrole = 0
        self.nbUranium = 0
        self.nbMetauxPrecieux = 0
        self.produit = Travailleur

    def idle(self):
        condition_pop = self.nbNourriture >= 1 and self.nbVivant >= 1
        condition_newIndustrieChimique = self.nbBeton >= 5 and self.nbPetrole >= 3 and self.nbTravailleur >= 3
        condition_newArsenal = self.nbBeton >= 5 and self.nbAcier >= 3 and self.nbTravailleur >= 4
        condition_newHopital = self.nbBeton >= 5 and self.nbIngenieur >= 4
        condition_newUniversite = self.nbBeton >= 5 and self.nbIngenieur >= 4 and self.nbTravailleur >= 1
        condition_newAeronautique = self.nbBeton >= 5 and self.nbTravailleur >= 4 and self.nbVehiculeThermique >= 3
        condition_newCentraleAtom = self.nbBeton >= 5 and self.nbUranium >= 1 and self.nbIngenieur >= 1
        condition_newCentraleSol = self.nbBeton >= 5 and self.nbIngenieur >= 1 and nbMetauxPrecieux >= 2
        condition_newCaserne = self.nbBeton >= 5 and self.nbSoldat >= 2 and nbTravailleur >= 1

#il execute les if de manière séquentielle le mec
#c'est le dernier IF VRAI qui a raison
        if condition_pop : self.brain.setState(self.pop)
        if condition_newIndustrieChimique : self.brain.setState(self.newIndustrieChimique)
        if condition_newArsenal : self.brain.setState(self.newArsenal)
        if condition_newHopital : self.brain.setState(self.newHopital)
        if condition_newUniversite : self.brain.setState(self.newUniversite)
        if condition_newAeronautique : self.brain.setState(self.newAeronautique)
        if condition_newCentraleAtom : self.brain.setState(self.newCentraleAtom)
        if condition_newCentraleSol : self.brain.setState(self.newCentraleSol)
        if condition_newCaserne : self.brain.setState(self.newCaserne)

    def pop(self):
        self.spawn(self.produit)
        if self.nbNourriture <1 or self.nbVivant <1 :
            self.brain.setState(self.idle)
        self.idle()

#alors ce self.idle() c'est un peu chelou mais c'est pour l'aider à sortir de la boucle si jamais
#le client veut fabriquer un truc dans sa ville.

    def newIndustrieChimique(self):
        newindustriechimique = self.spawn(IndustrieChimique)
        for i in range(5):
            self.remove(Beton)
        for z in range(3):
            self.remove(Petrole)
        for u in range(4):
            self.remove(Travailleur)
            self.spawn(Travailleur, newindustriechimique.id)

        if self.nbBeton < 5 or self.nbTravailleur < 4 or self.nbAcier < 3 :
            self.brain.setState(self.idle)
            self.save()

        self.idle()


    def newArsenal(self):
        newarsenal = self.spawn(Arsenal)
        for i in range(5):
            self.remove(Beton)
        for z in range(3):
            self.remove(Acier)
        for u in range(4):
            self.remove(Travailleur)
            self.spawn(Travailleur, newarsenal.id)

        if self.nbBeton < 5 or self.nbTravailleur < 4 or self.nbAcier < 3:
            self.brain.setState(self.idle)
            self.save()

        self.idle()

    def newHopital(self):
        newhopital = self.spawn(Hopital)
        for i in range(5):
            self.remove(Beton)
        for u in range(4):
            self.remove(Ingenieur)
            self.spawn(Ingenieur, newhopital.id)

        if self.nbBeton < 5 or self.nbIngenieur < 4 :
            self.brain.setState(self.idle)
            self.save()

        self.idle()

    def newUniversite(self):
        newuniversite = self.spawn(Universite)
        for i in range(5):
            self.remove(Beton)
        for u in range(3):
            self.remove(Ingenieur)
            self.spawn(Ingenieur, newuniversite.id)
        self.remove(Travailleur)
        self.spawn(Travailleur, newuniversite.id)

        if self.nbBeton < 5 or self.nbTravailleur < 1 or self.nbIngenieur < 3 :
            self.brain.setState(self.idle)
            self.save()

        self.idle()

    def newAeronautique(self):
        newaeronautique = self.spawn(Aeronautique)
        for i in range(5):
            self.remove(Beton)
        for z in range(3):
            self.remove(VehiculeThermique)
        for u in range(4):
            self.remove(Travailleur)
            self.spawn(Travailleur, newaeronautique.id)

        if self.nbBeton < 5 or self.nbTravailleur < 4 or self.nbVehiculeThermique < 3 :
            self.brain.setState(self.idle)
            self.save()

        self.idle()

    def newCentraleAtom(self):
        newcentraleatom = self.spawn(CentraleAtom)
        for i in range(5):
            self.remove(Beton)
        self.remove(Uranium)
        self.remove(Ingenieur)
        self.spawn(Ingenieur, newcentraleatom.id)

        if self.nbBeton < 5 or self.nbIngenieur < 1 or self.nbUranium < 1 :
            self.brain.setState(self.idle)
            self.save()

        self.idle()

    def newCentraleSol(self):
        newcentralesol = self.spawn(CentraleSol)
        for i in range(5):
            self.remove(Beton)
        self.remove(MetauxPrecieux)
        self.remove(Ingenieur)
        self.spawn(Ingenieur, newcentralesol.id)

        if self.nbBeton < 5 or self.nbTravailleur < 4 or self.nbVehiculeThermique < 3 :
            self.brain.setState(self.idle)
            self.save()

        self.idle()

    def newCaserne(self):
        newcaserne = self.spawn(Caserne)
        for i in range(5):
            self.remove(Beton)
        for u in range(2):
            self.remove(Soldat)
            self.spawn(Soldat, newcaserne.id)
        self.remove(Travailleur)
        self.spawn(Travailleur, newcaserne.id)

        if self.nbBeton < 5 or self.nbTravailleur < 1 or self.nbSoldat < 2 :
            self.brain.setState(self.idle)
            self.save()

        self.idle()


    def update(self):
        # update Ville here
        self.nbTravailleur = self.countByType(Travailleur)
        self.nbNourriture = self.countByType(Nourriture)
        self.nbBois = self.countByType(Bois)
        self.nbBeton = self.countByType(Beton)
        self.nbVehicule = self.countByType(Vehicule)
        self.nbCoton = self.countByType(Coton)
        self.nbLin = self.countByType(Lin)
        self.nbAcier = self.countByType(Acier)
        self.nbCharbon = self.countByType(Charbon)
        self.nbPetrole = self.countByType(Petrole)
        self.nbVivant = self.countByType(Vivant)

        self.brain.update()

class Arsenal(Entite):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.nbTravailleur = 0
        self.nbAcier = 0
        self.nbVehicule = 0
        self.nbAvion = 0
        self.nbFusee = 0

    def idle(self):

        condition_Fusil = self.nbAcier >= 1 and self.nbTravailleur >= 4
        condition_Tank = self.nbVehicule >= 1 and self.nbTravailleur >= 4
        condition_Bombardier = self.nbAvion >= 1 and self.nbTravailleur >= 4
        condition_Missile = self.nbFusee >= 1 and self.nbTravailleur >= 4

        if condition_Fusil : self.brain.setState(self.newFusil)
        if condition_Tank : self.brain.setState(self.newTank)
        if condition_Bombardier : self.brain.setState(self.newBombardier)
        if condition_Missile : self.brain.setState(self.newMissile)

    def newTank(self):
        self.spawn(Arme)
        self.remove(Acier)

        if self.nbTravailleur < 4 or self.nbAcier < 1 :
            self.brain.setState(self.idle)
        self.idle()

    def newTank(self):
        for x in range(3):
            self.spawn(Arme)

        self.remove(Vehicule)

        if self.nbTravailleur < 4 or self.nbVehicule < 1 :
            self.brain.setState(self.idle)
        self.idle()

    def newBombardier(self):
        for x in range(6):
            self.spawn(Arme)

        self.remove(Avion)

        if self.nbTravailleur < 4 or self.nbAvion < 1 :
            self.brain.setState(self.idle)
        self.idle()

    def newMissile(self):
        for x in range(9):
            self.spawn(Arme)

        self.remove(Fusee)

        if self.nbTravailleur < 4 or self.nbFusee < 1 :
            self.brain.setState(self.idle)
        self.idle()

    def update(self):
        self.nbTravailleur = self.countByType(Travailleur)
        self.nbVehicule = self.countByType(Vehicule)
        self.nbAcier = self.countByType(Acier)
        self.nbAvion = self.countByType(Avion)
        self.nbFusee = self.countByType(Fusee)
        self.brain.update()


class Hopital(Entite):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.nbIngenieur = 0
        self.produit = Sante
    def idle(self):
        if self.nbIngenieur >= 4 :
            self.brain.setState(self.production)
    def production(self):
        self.spawn(self.produit)
        if self.nbIngenieur < 4 :
            self.brain.setState(self.idle)

    def update(self):
        # update BTP here
        self.nbIngenieur = self.countByType(Ingenieur)
        self.brain.update()

class Universite(Entite):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.nbIngenieur = 0
        self.nbTravailleur = 0
        self.produit = Ingenieur
    def idle(self):
        if self.nbIngenieur >= 4 and self.nbTravailleur >= 1:
            self.brain.setState(self.production)
    def production(self):
        self.spawn(self.produit)
        if self.nbIngenieur < 4 or self.nbTravailleur < 1:
            self.brain.setState(self.idle)

    def update(self):
        self.nbIngenieur = self.countByType(Ingenieur)
        self.nbTravailleur = self.countByType(Travailleur)
        self.brain.update()

class IndustrieChimique(Entite):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.nbIngenieur = 0
        self.nbPetrole = 0
        self.produit = Chimie
    def idle(self):
        if self.nbIngenieur >= 4 and self.nbPetrole >= 1:
            self.brain.setState(self.production)
    def production(self):
        for z in range(3):
            self.spawn(self.produit)

        if self.nbIngenieur < 4 or self.nbPetrole < 1:
            self.brain.setState(self.idle)

    def update(self):
        self.nbIngenieur = self.countByType(Ingenieur)
        self.nbTravailleur = self.countByType(Petrole)
        self.brain.update()

class CentraleAtom(Entite):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.nbIngenieur = 0
        self.nbUranium = 0
        self.produit1 = Electricite
        self.produit2 = DechetRadioactif
    def idle(self):
        if self.nbIngenieur >= 2 and self.nbUranium >= 1:
            self.brain.setState(self.production)
    def production(self):
        for i in range(3):
           self.spawn(self.produit1)
        if Robot.cycles%3 == 0 :
           self.spawn(self.produit2)
        if self.nbIngenieur < 2 or self.nbUranium < 1:
           self.brain.setState(self.idle)

    def update(self):
        self.nbIngenieur = self.countByType(Ingenieur)
        self.nbUranium = self.countByType(Uranium)
        self.brain.update()

class CentraleSol(Entite):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.nbIngenieur = 0
        self.produit = Electricite
    def idle(self):
        if self.nbIngenieur >= 1 :
            self.brain.setState(self.production)
    def production(self):
        if Robot.cycles%2 == 0 : self.spawn(self.produit)
        if self.nbIngenieur < 1 :
            self.brain.setState(self.idle)

    def update(self):
        self.nbIngenieur = self.countByType(Ingenieur)
        self.brain.update()

class Electronique(Entite):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.nbIngenieur = 0
        self.nbMetauxPrecieux = 0
        self.produit = Ordinateur
    def idle(self):
        if self.nbIngenieur >= 2 and self.nbMetauxPrecieux >= 2:
            self.brain.setState(self.production)

    def production(self):
        self.spawn(self.produit)
        if self.nbIngenieur < 2 or self.nbMetauxPrecieux < 2:
            self.brain.setState(self.idle)

    def update(self):
        self.nbIngenieur = self.countByType(Ingenieur)
        self.nbTravailleur = self.countByType(MetauxPrecieux)
        self.brain.update()

class Caserne(Entite):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.nbSoldat = 0
        self.nbTravailleur = 0
        self.nbArme = 0
        self.produit = Soldat
    def idle(self):
        if self.nbSoldat >= 2 and self.nbTravailleur >= 1 and self.nbArme >= 1 :
            self.brain.setState(self.production)
    def production(self):
        self.spawn(self.produit)
        if self.nbSoldat < 2 or self.nbTravailleur < 1 or self.nbArme < 1 :
            self.brain.setState(self.idle)

    def update(self):
        self.nbSoldat = self.countByType(Soldat)
        self.nbArme = self.countByType(Arme)
        self.nbTravailleur = self.countByType(Travailleur)
        self.brain.update()

class Megalopole(Entite):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.nbVivant = 0
        self.nbIngenieur = 0
        self.nbBeton = 0
        self.nbAcier = 0
        self.nbOrdinateur = 0
        self.nbMetauxPrecieux = 0
        self.produit = Travailleur

    def idle(self):
        condition_pop = self.nbNourriture >= 1 and self.nbVivant >= 1
        condition_newElectronique = self.nbBeton >= 5 and self.nbMetauxPrecieux >= 2 and self.nbIngenieur >= 2
        condition_newBanque = self.nbBeton >= 5 and self.nbAcier >= 5 and self.nbIngenieur >= 4
        condition_newAssurance = self.nbBeton >= 5 and self.nbOrdinateur >= 3 and self.nbIngenieur >= 4

#il execute les if de manière séquentielle le mec
#c'est le dernier IF VRAI qui a raison
        if condition_pop : self.brain.setState(self.pop)
        if condition_newElectronique : self.brain.setState(self.newElectronique)
        if condition_newBanque : self.brain.setState(self.newBanque)
        if condition_newAssurance : self.brain.setState(self.newAssurance)

    def pop(self):
        self.spawn(self.produit)
        if self.nbNourriture <1 or self.nbVivant <1 :
            self.brain.setState(self.idle)
        self.idle()

#alors ce self.idle() c'est un peu chelou mais c'est pour l'aider à sortir de la boucle si jamais
#le client veut fabriquer un truc dans sa ville.

    def newElectronique(self):
        newelectronique = self.spawn(Electronique)
        for i in range(5):
            self.remove(Beton)
        for z in range(2):
            self.remove(MetauxPrecieux)
        for u in range(2):
            self.remove(Ingenieur)
            self.spawn(Ingenieur, newelectronique.id)

        if self.nbBeton < 5 or self.nbMetauxPrecieux < 2 or self.nbIngenieur < 2 :
            self.brain.setState(self.idle)
            self.save()

        self.idle()

    def newBanque(self):
        newbanque = self.spawn(Banque)
        for i in range(5):
            self.remove(Beton)
        for z in range(5):
            self.remove(Acier)
        for u in range(2):
            self.remove(Ingenieur)
            self.spawn(Ingenieur, newelectronique.id)

        if self.nbBeton < 5 or self.nbMetauxPrecieux < 2 or self.nbIngenieur < 2 :
            self.brain.setState(self.idle)
            self.save()

        self.idle()

    def newElectronique(self):
        newelectronique = self.spawn(Electronique)
        for i in range(5):
            self.remove(Beton)
        for z in range(2):
            self.remove(MetauxPrecieux)
        for u in range(2):
            self.remove(Ingenieur)
            self.spawn(Ingenieur, newelectronique.id)

        if self.nbBeton < 5 or self.nbMetauxPrecieux < 2 or self.nbIngenieur < 2 :
            self.brain.setState(self.idle)
            self.save()

        self.idle()

    def update(self):
        # update Ville here
        self.nbTravailleur = self.countByType(Travailleur)
        self.nbNourriture = self.countByType(Nourriture)
        self.nbBeton = self.countByType(Beton)
        self.nbAcier = self.countByType(Acier)
        self.nbMetauxPrecieux = self.countByType(MetauxPrecieux)
        self.nbOrdinateur = self.countByType(Ordinateur)
        self.nbVivant = self.countByType(Vivant)

        self.brain.update()


class GisementMetauxPrecieux(Entite):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.nbTravailleur = 0
        self.nbAcier = 0

    def idle(self):
        if  self.nbTravailleur >= 3 and self.nbAcier >= 2:
            self.brain.setState(self.production)

    def unmanned(self):
        if self.nbTravailleur >= 3 :
            self.brain.setState(self.production)

    def production(self):
        for z in range(2):
            self.spawn(MetauxPrecieux)

        if self.nbTravailleur < 3 :
            self.brain.setState(self.unmanned)

    def update(self):
        self.nbTravailleur = self.countByType(Travailleur)
        self.nbAcier = self.countByType(Acier)
        self.brain.update()

class GisementMetaux(Entite):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.nbTravailleur = 0
        self.nbAcier = 0

    def idle(self):
        if  self.nbTravailleur >= 3 and self.nbAcier >= 2 :
            self.brain.setState(self.production)

    def unmanned(self):
        if self.nbTravailleur >= 3 :
            self.brain.setState(self.production)

    def production(self):
        for z in range(3):
            self.spawn(Metaux)

        if self.nbTravailleur < 3 :
            self.brain.setState(self.unmanned)

    def update(self):
        self.nbTravailleur = self.countByType(Travailleur)
        self.nbAcier = self.countByType(Acier)
        self.brain.update()

class GisementCharbon(Entite):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.nbTravailleur = 0
        self.nbAcier = 0

    def idle(self):
        if  self.nbTravailleur >= 3 and self.nbAcier >= 2 :
            self.brain.setState(self.production)

    def unmanned(self):
        if self.nbTravailleur >= 3 :
            self.brain.setState(self.production)

    def production(self):
        for z in range(3):
            self.spawn(Charbon)

        if self.nbTravailleur < 3 :
            self.brain.setState(self.unmanned)

    def update(self):
        self.nbTravailleur = self.countByType(Travailleur)
        self.nbAcier = self.countByType(Acier)
        self.brain.update()

class GisementPetrole(Entite):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.nbTravailleur = 0
        self.nbAcier = 0

    def idle(self):
        if  self.nbTravailleur >= 3 and self.nbAcier >= 2 :
            self.brain.setState(self.production)

    def unmanned(self):
        if self.nbTravailleur >= 3 :
            self.brain.setState(self.production)

    def production(self):
        for z in range(3):
            self.spawn(Petrole)

        if self.nbTravailleur < 3 :
            self.brain.setState(self.unmanned)

    def update(self):
        self.nbTravailleur = self.countByType(Travailleur)
        self.nbAcier = self.countByType(Acier)
        self.brain.update()

class GisementUranium(Entite):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.nbTravailleur = 0
        self.nbAcier = 0
        self.energy = 3

    def idle(self):
        if  self.nbTravailleur >= 3 and self.nbAcier >= 2 and self.energy >= 1 :
            self.brain.setState(self.production)

    def unmanned(self):
        if self.nbTravailleur >= 3 :
            self.brain.setState(self.production)

    def production(self):
        for z in range(2):
            self.spawn(Uranium)

        if self.nbTravailleur < 3 :
            self.brain.setState(self.unmanned)

        if self.energy < 1 :
            self.brain.setState(self.idle)

        self.energy =- 1


    def update(self):
        self.nbTravailleur = self.countByType(Travailleur)
        self.nbAcier = self.countByType(Acier)
        self.brain.update()

class Mer(Entite):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.nbTravailleur = 0
        self.nbBateauUsine = 0
        self.nbAnchois = 0

    def idle(self):

        if self.nbTravailleur >= 2 :
            self.brain.setState(self.peche)

    def peche(self):
        for i in range(3):
            self.spawn(Poisson)
            self.remove(Anchois, self.id)

        if self.nbAnchois < 1 :
            self.brain.setState(self.idle)


    def update(self):
        self.nbAnchois = self.countByType(Anchois)
        self.nbTravailleur = self.countByType(Travailleur)
        self.nbBateauUsine = self.countByType(BateauUsine)
        self.brain.update()


class Champ(Entite):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.nbPollinisateur = 0
        self.nbTracteur = 0
        self.nbTravailleur = 0
        self.nbChimie = 0
        self.nbCereale = 0
        self.nbBestiau = 0
        self.nbLait = 0

    def idle(self):

        if self.nbCereale < 1 and self.nbPollinisateur < 1:
            self.spawn(Pollinisateur, self.id)
        if self.nbCereale < 1:
            self.spawn(Cereale, self.id)

        if Robot.cycles%6 == 0 : self.spawn(Pollinisateur, self.id)

        if self.nbTravailleur >= 2 and self.nbPollinisateur >= 1 or self.nbTravailleur >= 3:
            self.brain.setState(self.culture)

        if self.nbTravailleur >= 1 and self.nbTracteur >= 1 and self.nbChimie >= 1:
            self.brain.setState(self.monoculture)

        if self.nbTravailleur >= 1 and self.nbBestiau >= 1 :
            self.brain.setState(self.elevage)

        if self.nbTravailleur >= 1 and self.nbBestiau >= 1 and self.nbChimie >= 1 and self.nbCereale >= 10:
            self.brain.setState(self.elevageIntensif)

    def culture(self):

        if self.nbTravailleur < 3 or self.nbTravailleur < 2 and self.nbPollinisateur < 1 :
            self.brain.setState(self.idle)
        self.idle()

        if Robot.cycles%12 == 0 : self.spawn(Pollinisateur, self.id)

        for i in range(4):
            self.spawn(Cereale)

    def monoculture(self):

        if self.nbTravailleur < 1 or self.nbTracteur < 1 or self.nbChimie < 1 or self.nbPollinisateur < 1:
            self.brain.setState(self.idle)

        for i in range(8):
            self.spawn(Cereale)

        self.remove(Pollinisateur, self.id)
        self.remove(Chimie, self.id)

    def elevage(self):

        if self.nbTravailleur < 1 or self.nbBestiau < 1 :
            self.brain.setState(self.idle)

        for i in range(2):
            self.spawn(Lait)
 
        if Robot.cycles%12 == 0 : self.spawn(Pollinisateur, self.id)

    def elevageIntensif(self):

        self.remove(Chimie)
        for z in range(10) : self.remove(Cereale)
        # a priori ce remove marche
        for y in range(9) : self.spawn(Bestiau, self.id)

        if self.nbTravailleur < 1 or self.nbBestiau < 1 or self.nbCereale < 1 :
            self.brain.setState(self.idle)

        for i in range(3):
            self.spawn(Viande)

        self.remove(Bestiau)
        # mais celui-ci non.
        self.remove(Cereale)

    def update(self):
        self.nbPollinisateur = self.countByType(Pollinisateur)
        self.nbTravailleur = self.countByType(Travailleur)
        self.nbTracteur = self.countByType(Tracteur)
        self.nbChimie = self.countByType(Chimie)
        self.nbCereale = self.countByType(Cereale)
        self.nbBestiau = self.countByType(Bestiau)
        self.nbLait = self.countByType(Lait)
        self.brain.update()


class Foret(Entite):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.nbArbres = 0
        self.nbTravailleur = 0

    def idle(self):
        self.spawn(Arbre, self.id)
        if Robot.cycles%3 == 0: self.spawn(Arbre, self.id)
        if self.nbTravailleur >= 2:
            self.brain.setState(self.production)

    def production(self):
        if  self.nbTravailleur < 2:
            self.brain.setState(self.idle)
        else:
            self.spawn(Bois)
            self.remove(Arbre)
            #le remove ne marche plus
        if self.nbArbres < 1:
            self.mutate(Champ)

    def update(self):
        self.nbTravailleur = self.countByType(Travailleur)
        self.nbArbres = self.countByType(Arbre)
        self.brain.update()


class Bio(Base):
    """
        bio
            - Arbre
            - Bois
            - Coton
            - Lin
            - Sucre
            - Vin
            - Pollinisateur (§)
            - Mouton
            - Boeuf
            - Volaille
            - Porc
            - Anchois  (§)
            - Anguille
            - Baleine
            - Carpe
            - Colin
            - Hareng
            - Maquereau
            - Morue (§)
            - Sardine
            - Saumon
            - Thon
            - Truite

            Représentation sous forme de fichier

    """
    pass

class Arbre(Bio): pass
class Bois(Bio): pass
class Coton(Bio): pass
class Lin(Bio): pass
class Sucre(Bio): pass
class Vin(Bio): pass
class Pollinisateur(Bio): pass

class Bestiau(Bio): pass

class Poisson(Bio) :
    """
        Poissons
            - Anchois
            - Anguille
            - Baleine
            - Carpe
            - Colin
            - Hareng
            - Maquereau
            - Morue
            - Sardine
            - Saumon
            - Thon
            - Truite

            - LarveAnchois


        """
pass

class Anchois(Poisson):

    def init(self):
        self.age = 0

    def update(self):

        self.age += 1
        super(Anchois, self).update()

        if self.age == 2 : 
            self.spawn(Anchois)

        if self.age == 4 :
            self.spawn(Anchois)
            self.remove()


class Anguille(Poisson): pass
class Baleine(Poisson): pass
class Carpe(Poisson): pass
class Colin(Poisson): pass
class Hareng(Poisson): pass
class Maquereau(Poisson): pass
class Morue(Poisson): pass
class Sardine(Poisson): pass
class Saumon(Poisson): pass
class Thon(Poisson): pass
class Truite(Poisson): pass

class Pollinisateur(Bio) :
    """
    Pollinisateurs
        - Papillon
        - Abeille

    """
    pass

class Papillon(Pollinisateur) : pass
class Abeille(Pollinisateur) : pass
class Coccinelle(Pollinisateur) : pass


class Produit(Base):
    """
    Produits
        - Acier
        - Arme
        - Avion
        - BateauUsine
        - Beton
        - Chimie
        - DechetRadioactif
        - Electricite
        - Fumier
        - Fusee
        - Ordinateur
        - Tracteur
        - Sante
        - Vehicule

    Représentation sous forme de fichier

    """
    pass

class Acier(Produit): pass
class Arme(Produit): pass
class Avion(Produit): pass
class BateauUsine(Produit): pass
class Beton(Produit): pass
class Chimie(Produit): pass
class DechetRadioactif(Produit): pass
class Electricite(Produit): pass
class Fumier(Produit): pass
class Fusee(Produit): pass
class Ordinateur(Produit): pass
class Tracteur(Produit): pass
class Sante(Produit): pass

class Vehicule(Produit):
    """
        Vehicules
            -VehiculeThermique
            -VehiculeElectrique

    """

    pass

class VehiculeThermique(Vehicule): pass
class VehiculeElectrique(Vehicule): pass

class Fossile(Base):
    """
        Fossiles
            - Petrole
            - Charbon
            - Metaux
            - MetauxPrecieux
            - Uranium

        Représentation sous forme de fichier

    """
    pass

class Bois(Fossile): pass
class Petrole(Fossile): pass
class Charbon(Fossile): pass
class Uranium(Fossile): pass
class Metaux(Fossile): pass
class MetauxPrecieux(Fossile): pass

class Vivant(Base):
    """
        Vivants
            - Travailleur
            - Ingenieur
            - Soldat
        Représentation sous forme de fichier

    """
    def init(self):
        self.energy = 3


class Travailleur(Vivant):
    def update(self):
        self.energy -= 1
        o = self.findOneElement(Nourriture)
        if o:
            self.energy += 1
            o.energy -= 1
            o.update_file()
        super(Travailleur, self).update()
        if self.energy < 1:
            self.remove()

#il faut que la nourriture soit dans le même folder que le travailleur (ça va pas)


class Ingenieur(Vivant): pass
class Soldat(Vivant): pass

class Nourriture(Base):
    """
        Nourritures
            - Cereale
            - Poisson
            - Viande
            - Lait

    """
    def init(self):
        self.energy = 10

    def update(self):
        super(Nourriture, self).update()
        if self.energy < 1:
            self.remove()        


class Cereale(Nourriture): pass
class Poisson(Nourriture): pass
class Viande(Nourriture): pass
class Lait(Nourriture): pass

alert(text = "Ready?", title="Fuck a duck and try to fly", button = "Ok")
robot = Robot()
# Robot(secondes=1)
robot.run()
