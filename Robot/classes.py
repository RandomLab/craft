# -*- coding: utf-8 -*-
import time, os, sys
import uuid
import random

from Entite.Base import Entite, Base

from . import Robot

"""
    # TODO :

    Icon
    Dossier Partagé

    travailleurs qui peuvent manger partout

    sam:
    implémenter la classe d'anchois (et virer tout le bazar dans la mer)

    implémenter le craft de ville (champ->ville)
        ok mais le self.remove ne marche pas

    ça serait bien que les anchois changent de nom quand ils sont vieux


"""

class Ville(Entite):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.nbTravailleur = 0
        self.nbBeton = 0
        self.nbVehicule = 0
        self.nbArme = 0
        self.nbCharbon = 0
        self.nbPetrole = 0
        self.nbUranium = 0

    def idle(self):

#il execute les if de manière séquentielle le mec
#c'est le dernier IF VRAI qui a raison

#les conditions ne sont pas a jour
        if self.nbBeton >= 5 : self.brain.setState(self.newUsine)
        if self.nbBeton >= 5 and self.nbArme >= 3 : self.brain.setState(self.newCaserne)
        if self.nbBeton >= 5 and self.nbVehicule >= 3 : self.brain.setState(self.newMarche)
        if self.nbBeton >= 5 and (self.nbCharbon >= 2 or self.nbPetrole >= 2 or self.nbUranium >= 1) : self.brain.setState(self.newCentrale)
        if self.nbBeton >= 8 : self.brain.setState(self.newUniversite)

    def newUsine(self):
        for i in range(5):
            self.remove(Beton)

        self.spawn(Usine)

        self.brain.setState(self.idle)
        self.save()


    def newCentrale(self):
        for i in range(5):
            self.remove(Beton)
        if self.nbCharbon >= 2 :
            for u in range(2):
               self.remove(Charbon)
        if self.nbPetrole >= 2 :
            for z in range(2):
                self.remove(Petrole)
        if self.nbUranium >= 1 :
            self.remove(Uranium)
    
        self.brain.setState(self.idle)
        self.save()



    def update(self):
        # update Ville here
        self.nbTravailleur = self.countByType(Travailleur)
        self.nbNourriture = self.countByType(Nourriture)
        self.nbBeton = self.countByType(Beton)
        self.nbAcier = self.countByType(Acier)
        self.nbCharbon = self.countByType(Charbon)
        self.nbPetrole = self.countByType(Petrole)
        self.nbVivant = self.countByType(Vivant)

        self.brain.update()

class Centrale(Entite):
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

class Usine(Entite):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.nbTravailleur = 0
        self.nbAcier = 0
        self.nbPetrole = 0

    def idle(self):

        if self.nbPetrole >= 1 and self.nbAcier >= 1 and self.nbTravailleur >= 4 : self.brain.setState(self.newVehicule)


    def newVehicule(self):
        self.spawn(Vehicule)
        self.remove(Petrole)
        self.remove(Acier)
        if self.nbTravailleur < 4 or self.nbPetrole < 1 or self.nbAcier < 1 :
            self.brain.setState(self.idle)
        self.idle()

    def update(self):
        self.nbTravailleur = self.countByType(Travailleur)
        self.nbPetrole = self.countByType(Petrole)
        self.nbAcier = self.countByType(Acier)
        self.nbMetalPrecieux = self.countByType(MetalPrecieux)
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


class GisementMetal(Entite):
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
            self.spawn(Metal)

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

class GisementPhosphates(Entite):
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
            self.spawn(Phosphate)

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
        self.nbBeton = 0
        self.nbSoja = 0

    def idle(self):
        if self.nbPollinisateur < 1 and self.nbCereale < 1:
            self.spawn(Cereale, self.id)
            self.spawn(Soja, self.id)

        if Robot.cycles%12 == 0 : self.spawn(Pollinisateur, self.id)

        if self.nbTravailleur >= 2 and self.nbPollinisateur >= 1 and self.nbCereale >= 1:
            self.brain.setState(self.cultureC)

        if self.nbTravailleur >= 2 and self.nbPollinisateur >= 1 and self.nbSoja >= 1:
            self.brain.setState(self.cultureS)

        if self.nbTravailleur >= 1 and self.nbTracteur >= 1 and self.nbChimie >= 1 and self.nbCereale >= 1:
            self.brain.setState(self.monocultureC)

        if self.nbTravailleur >= 1 and self.nbTracteur >= 1 and self.nbChimie >= 1 and self.nbSoja >= 1:
            self.brain.setState(self.monocultureS)

        if self.nbBeton >= 10 :
            for z in range(10):
                self.remove(Beton)
        #le self.remove ne marche pas
            self.mutate(Ville)

    def cultureC(self):

        if self.nbTravailleur < 2 or self.nbCereale < 1 or self.nbPollinisateur < 1 :
            self.brain.setState(self.idle)
        self.idle()

        if Robot.cycles%8 == 0 : self.spawn(Pollinisateur, self.id)

        for i in range(4):
            self.spawn(Cereale)
    
    def cultureS(self):

        if self.nbTravailleur < 2 or self.nbSoja < 1 or self.nbPollinisateur < 1 :
            self.brain.setState(self.idle)
        self.idle()

        if Robot.cycles%12 == 0 : self.spawn(Pollinisateur, self.id)

        for i in range(4):
            self.spawn(Soja)

    def monocultureC(self):

        if self.nbTravailleur < 1 or self.nbTracteur < 1 or self.nbChimie < 1 or self.nbPollinisateur < 1 or self.nbCereale < 1:
            self.brain.setState(self.idle)

        for i in range(8):
            self.spawn(Cereale)

        # self.remove(Pollinisateur, self.id)
        # self.remove(Chimie, self.id)

    def monocultureS(self):

        if self.nbTravailleur < 1 or self.nbTracteur < 1 or self.nbChimie < 1 or self.nbPollinisateur < 1 or self.nbSoja < 1:
            self.brain.setState(self.idle)

        for i in range(8):
            self.spawn(Soja)

        # self.remove(Pollinisateur, self.id)
        # self.remove(Chimie, self.id)


    def update(self):
        self.nbPollinisateur = self.countByType(Pollinisateur)
        self.nbTravailleur = self.countByType(Travailleur)
        self.nbTracteur = self.countByType(Tracteur)
        self.nbChimie = self.countByType(Chimie)
        self.nbCereale = self.countByType(Cereale)
        self.nbBeton = self.countByType(Beton)
        self.nbSoja = self.countByType(Soja)
        self.brain.update()


class Foret(Entite):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.nbArbre = 0
        self.nbTravailleur = 0

    def idle(self):

        if self.nbArbre <= 8:
          self.spawn(Arbre, self.id)

        if Robot.cycles%4 == 0: self.spawn(Arbre, self.id)

        if self.nbTravailleur >= 2:
            self.brain.setState(self.production)

    def production(self):
        if  self.nbTravailleur < 2:
            self.brain.setState(self.idle)
        else:
            if self.nbArbre >= self.nbTravailleur :
                for z in range(self.nbTravailleur):
                    self.remove(Arbre)
            else:
                for u in range(self.nbArbre):
                    self.remove(Arbre)

        if Robot.cycles%4 == 0: self.spawn(Arbre, self.id)

        if self.nbArbre < 1:
            self.mutate(Champ)


    def update(self):
        self.nbTravailleur = self.countByType(Travailleur)
        self.nbArbre = self.countByType(Arbre)
        self.brain.update()

class Colline(Entite):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.nbTravailleur = 0
        self.nbCalcaire = 0

    def idle(self):
        if self.nbTravailleur >= 2:
            self.brain.setState(self.production)

    def production(self):
        if  self.nbTravailleur < 2:
            self.brain.setState(self.idle)
        for u in range(3):
            self.spawn(Calcaire)

    def update(self):
        self.nbTravailleur = self.countByType(Travailleur)
        self.nbCalcaire = self.countByType(Calcaire)
        self.brain.update()


class Bio(Base):
    """
        bio
            - Arbre
            - TigreDeSumatra
            - Pollinisateur
            - Anchois

            Représentation sous forme de fichier

    """
    pass

class Arbre(Bio): pass
class TigreDeSumatra(Bio): pass
class Pollinisateur(Bio): pass

class Anchois(Bio):

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


class Produit(Base):
    """
    Produits
        - Acier
        - Arme
        - BateauUsine
        - Beton
        - Chimie
        - DechetRadioactif
        - Electricite
        - Tracteur
        - Vehicule
        - Soja

    Représentation sous forme de fichier

    """
    pass

class Acier(Produit): pass
class Arme(Produit): pass
class BateauUsine(Produit): pass
class Beton(Produit): pass
class Chimie(Produit): pass
class DechetRadioactif(Produit): pass
class Electricite(Produit): pass
class Tracteur(Produit): pass
class Vehicule(Produit): pass
class Soja(Produit): pass

class Fossile(Base):
    """
        Fossiles
            - Petrole
            - Charbon
            - Metal
            - Phosphate
            - Uranium
            - Calcaire

        Représentation sous forme de fichier

    """
    pass

class Calcaire(Fossile): pass
class Petrole(Fossile): pass
class Charbon(Fossile): pass
class Uranium(Fossile): pass
class Metal(Fossile): pass
class Phosphate(Fossile): pass

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

    def idle(self):
        self.energy -= 1
        o = Robot.findOne(Nourriture)
        if o:
            self.energy += 1
            o.energy -= 1
            o.update()
        if self.energy < 1:
            self.remove()

class Travailleur(Vivant): pass
class Ingenieur(Vivant): pass
class Soldat(Vivant): pass

class Nourriture(Base):
    """
        Nourritures
            - Cereale
            - Poisson

    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.energy = 2

    def idle(self):
        if self.energy < 1:
            self.remove()


class Cereale(Nourriture): pass
class Poisson(Nourriture): pass
