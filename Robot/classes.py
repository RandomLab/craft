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
        self.nbVivant = 0
        self.nbBeton = 0
        self.nbVehicule = 0
        self.nbArme = 0
        self.nbCharbon = 0
        self.nbPetrole = 0
        self.nbUranium = 0
        self.nbPain = 0

    def idle(self):

#il execute les if de manière séquentielle le mec
#c'est le dernier IF VRAI qui a raison

        if self.nbPain >= 1 and self.nbVivant >= 1 : self.brain.setState(self.pop)
        if self.nbBeton >= 5 : self.brain.setState(self.newUsine)
        if self.nbBeton >= 5 and self.nbArme >= 3 : self.brain.setState(self.newCaserne)
        if self.nbBeton >= 5 and self.nbVehicule >= 3 : self.brain.setState(self.newMarche)
        if self.nbBeton >= 5 and (self.nbCharbon >= 2 or self.nbPetrole >= 2 or self.nbUranium >= 1) : self.brain.setState(self.newCentrale)
        if self.nbBeton >= 8 : self.brain.setState(self.newUniversite)

    def pop(self):

        if self.nbVivant < 1 or self.nbPain < 1 :
            self.brain.setState(self.idle)

        if self.nbVivant >= 1 and self.nbPain >= 1 :
            self.spawn(Travailleur)
            self.remove(Pain)
            self.nbPain -= 1
       
        self.save()


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

        self.spawn(Centrale)
    
        self.brain.setState(self.idle)
        self.save()

    def newCaserne(self):
        for i in range(5):
            self.remove(Beton)
        for z in range(3):
            self.remove(Arme)

        self.spawn(Caserne)

        self.brain.setState(self.idle)
        self.save()

    def newUniversite(self):
        for i in range(8):
            self.remove(Beton)

        self.spawn(Universite)

        self.brain.setState(self.idle)
        self.save()

    def newMarche(self):
        for i in range(5):
            self.remove(Beton)
        for z in range(3):
            self.remove(Vehicule)

        self.spawn(Marche)

        self.brain.setState(self.idle)
        self.save()

    def update(self):
        # update Ville here
        self.nbBeton = self.countByType(Beton)
        self.nbArme = self.countByType(Arme)
        self.nbCharbon = self.countByType(Charbon)
        self.nbPetrole = self.countByType(Petrole)
        self.nbUranium = self.countByType(Uranium)
        self.nbVehicule = self.countByType(Vehicule)
        self.nbPain = self.countByType(Pain)
        self.nbVivant = self.countByType(Vivant)
        self.brain.update()

class Centrale(Entite):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.nbIngenieur = 0
        self.nbCharbon = 0
        self.nbPetrole = 0
        self.nbUranium = 0

    def idle(self):
        if self.nbIngenieur >= 2 and (self.nbCharbon >= 1 or self.nbPetrole >= 1) :
            self.brain.setState(self.production)
        if self.nbIngenieur >= 2 and self.nbUranium >= 1 :
            self.brain.setState(self.atom)

    def production(self):
        for i in range(3) :
            self.spawn(Electricite)

        for z in range(2) :
            self.remove(Fossile)
        
        if self.nbIngenieur < 2 or self.nbCharbon or self.nbPetrole < 1:
            self.brain.setState(self.idle)

        self.idle()

    def atom(self):
        for i in range(6) :
            self.spawn(Electricite)
        self.spawn(DechetRadioactif)
        self.remove(Uranium)
       
        if self.nbIngenieur < 2 or self.nbUranium < 1:
            self.brain.setState(self.idle)

        self.idle()

    def update(self):
        self.nbIngenieur = self.countByType(Ingenieur)
        self.nbCharbon = self.countByType(Charbon)
        self.nbPetrole = self.countByType(Petrole)
        self.nbUranium = self.countByType(Uranium)
        self.brain.update()

class Usine(Entite):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.nbTravailleur = 0
        self.nbIngenieur = 0
        self.nbAcier = 0
        self.nbPhosphate = 0
        self.nbMetal = 0
        self.nbCharbon = 0
        self.nbPetrole = 0
        self.nbCalcaire = 0
        self.nbElectricite = 0

    def idle(self):

        if self.nbAcier < 1 :
            for i in range(10):
                self.spawn(Acier, self.id)

        if self.nbPhosphate >= 1 and self.nbIngenieur >= 1 and self.nbElectricite >= 1 and self.nbElectricite >= 1 : self.brain.setState(self.newPesticide)
        if self.nbCalcaire >= 1 and self.nbTravailleur >= 4 and self.nbElectricite >= 1 : self.brain.setState(self.newBeton)
        if self.nbMetal >= 1 and self.nbCharbon >= 1 and self.nbTravailleur >= 4 and self.nbElectricite >= 1 : self.brain.setState(self.newAcier)
        if self.nbAcier >= 1 and self.nbTravailleur >= 4 and self.nbIngenieur >= 1 : self.brain.setState(self.newArme)
        if self.nbPetrole >= 1 and self.nbAcier >= 2 and self.nbTravailleur >= 4 and self.nbIngenieur >= 1 and self.nbElectricite >= 1 : self.brain.setState(self.newVehicule)


    def newVehicule(self):
        self.spawn(Vehicule)

        self.remove(Petrole)
        self.remove(Acier)
        self.remove(Acier)
        self.remove(Electricite)

        if self.nbTravailleur < 4 or self.nbPetrole < 1 or self.nbAcier < 2 or self.nbIngenieur < 1 or self.nbElectricite < 1 :
            self.brain.setState(self.idle)

        self.idle()

    def newArme(self):
        self.spawn(Arme)
        
        self.remove(Acier)
        self.remove(Electricite)


        if self.nbTravailleur < 4 or self.nbAcier < 1 or self.nbIngenieur < 1 :
            self.brain.setState(self.idle)

        self.idle()

    def newBeton(self):
        self.spawn(Beton)
        
        self.remove(Calcaire)
        self.remove(Electricite)

        if self.nbTravailleur < 4 or self.nbCalcaire < 1 or self.nbElectricite < 1 :
            self.brain.setState(self.idle)

        self.idle()

    def newAcier(self):
        self.spawn(Acier)
        
        self.remove(Metal)
        self.remove(Charbon)
        self.remove(Electricite)

        if self.nbTravailleur < 4 or self.nbMetal < 1 or self.nbCharbon < 1 or self.nbElectricite < 1 :
            self.brain.setState(self.idle)

        self.idle()

    def newPesticide(self):
        self.spawn(Pesticide)
        self.spawn(Pesticide)
        
        self.remove(Phosphate)
        self.remove(Electricite)

        if self.nbPhosphate < 1 or self.nbIngenieur < 1 or self.nbElectricite < 1 :
            self.brain.setState(self.idle)

        self.idle()

    def update(self):
        self.nbTravailleur = self.countByType(Travailleur)
        self.nbPetrole = self.countByType(Petrole)
        self.nbAcier = self.countByType(Acier)
        self.nbCharbon = self.countByType(Charbon)
        self.nbIngenieur = self.countByType(Ingenieur)
        self.nbPhosphate = self.countByType(Phosphate)
        self.nbMetal = self.countByType(Metal)
        self.nbCalcaire = self.countByType(Calcaire)
        self.nbElectricite = self.countByType(Electricite)
        self.brain.update()

class Universite(Entite):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.nbIngenieur = 0
        self.nbTravailleur = 0

    def idle(self):
        if self.nbIngenieur >= 2 and self.nbTravailleur >= 1:
            self.brain.setState(self.production)

    def production(self):

        if Robot.cycles%3 == 0 : 
            self.spawn(Ingenieur)
            self.remove(Travailleur)

        if self.nbIngenieur < 2 or self.nbTravailleur < 1:
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

    def idle(self):
        if self.nbSoldat >= 2 and self.nbTravailleur >= 1 :
            self.brain.setState(self.production)

    def production(self):

        if self.nbSoldat >= 2 and self.nbTravailleur >= 1 and Robot.cycles%3 == 0 :
            self.spawn(Soldat)
            self.remove(Travailleur)


        if self.nbSoldat < 2 or self.nbTravailleur < 1 :
            self.brain.setState(self.idle)

        self.save()

    def update(self):
        self.nbSoldat = self.countByType(Soldat)
        self.nbTravailleur = self.countByType(Travailleur)
        self.brain.update()

class Marche(Entite): 
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.nbPetrole = 0

    def idle(self):
        if  self.nbPetrole >= 2 :
            self.brain.setState(self.production)

    def production(self):
        if self.nbPetrole >= 2 and self.nbPetrole < 10 :
            self.spawn(Arme)
            for z in range(2):
                self.remove(Petrole)

        if self.nbPetrole >= 10 :
            self.spawn(Uranium)
            for y in range(10):
                self.remove(Petrole)

        #self.spawn(random.choice(Robot.listeBase))

        if self.nbPetrole < 2 :
            self.brain.setState(self.idle)
 
    def update(self):
        self.nbPetrole = self.countByType(Petrole)
        self.brain.update()


class GisementMetal(Entite):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.nbTravailleur = 0
        self.nbAcier = 0

    def idle(self):
        if  self.nbTravailleur >= 2 :
            self.brain.setState(self.production)

    def production(self):
        for z in range(2):
            self.spawn(Metal)

        if self.nbTravailleur < 2 :
            self.brain.setState(self.idle)

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
        if  self.nbTravailleur >= 2 :
            self.brain.setState(self.production)

    def production(self):
        for z in range(2):
            self.spawn(Charbon)

        if self.nbTravailleur < 2 :
            self.brain.setState(self.idle)

    def update(self):
        self.nbTravailleur = self.countByType(Travailleur)
        self.nbAcier = self.countByType(Acier)
        self.brain.update()

class GisementPetrole(Entite):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.nbTravailleur = 0
        self.energy = random.randint(5, 10)

    def idle(self):
        if  self.nbTravailleur >= 2 and self.energy >= 1 :
            self.brain.setState(self.production)

    def production(self):

        self.energy -= 1

        if  self.nbTravailleur >= 2 and self.energy >= 1 :
            self.spawn(Petrole)

        if self.nbTravailleur < 2 :
            self.brain.setState(self.idle)

        if self.energy < 1:
            self.mutate(GisementEpuise)

        self.save()

    def update(self):
        self.nbTravailleur = self.countByType(Travailleur)
        self.brain.update()

class GisementEpuise(Entite): pass

class GisementUranium(Entite): 

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.nbTravailleur = 0
        self.nbAcier = 0
        self.energy = random.randint(5, 10)

    def idle(self):
        if self.nbTravailleur >= 2 and self.nbAcier >= 2 and self.energy >= 1 :
            for y in range(2):
                self.remove(Acier)
            self.brain.setState(self.production)

    def unmanned(self):
        if self.nbTravailleur >= 2 :
            self.brain.setState(self.production)

    def production(self):
        self.spawn(Uranium)
        self.energy -= 1

        if self.nbTravailleur < 2 :
            self.brain.setState(self.unmanned)

        if self.energy < 1 :
            self.brain.setState(self.idle)

    def update(self):
        self.nbTravailleur = self.countByType(Travailleur)
        self.nbAcier = self.countByType(Acier)
        self.brain.update()


class GisementPhosphate(Entite):
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
        self.nbVehicule = 0
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
        self.nbVehicule = self.countByType(Vehicule)

        if self.nbVehicule >= 1 :
            v = Robot.find(Vehicule, self.id)
            for z in v :
                z.mutate(BateauUsine, path = self.id)

        self.brain.update()


class Champ(Entite):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.nbBiodiversite = 0
        self.nbTracteur = 0
        self.nbTravailleur = 0
        self.nbCereale = 0
        self.nbBeton = 0
        self.nbSoja = 0

    def idle(self):
        if self.nbBiodiversite < 1 and self.nbCereale < 1 and self.nbSoja < 1:
            self.spawn(Cereale, self.id)
            self.spawn(Soja, self.id)
            self.spawn(Biodiversite, self.id)

        if Robot.cycles%12 == 0 : self.spawn(Biodiversite, self.id)

        if self.nbTravailleur >= 2 and self.nbBiodiversite >= 1 and self.nbSoja >= 1:
            self.brain.setState(self.cultureS)

        if self.nbTravailleur >= 2 and self.nbBiodiversite >= 1 and self.nbCereale >= 1:
            self.brain.setState(self.cultureC)

        if self.nbTracteur >= 1 and self.nbSoja >= 1:
            self.brain.setState(self.monocultureS)

        if self.nbTracteur >= 1 and self.nbCereale >= 1:
            self.brain.setState(self.monocultureC)

        """
        if self.nbBeton >= 10 and self.nbVehicule >= 5 :
            for z in range(10):
                self.remove(Beton)

            for y in range(5):
                self.remove(Vehicule)
                self.spawn(Travailleur, self.id)

            self.mutate(Ville)
        """

    def cultureC(self):

        if self.nbTravailleur < 2 or self.nbCereale < 1 or self.nbBiodiversite < 1 :
            self.brain.setState(self.idle)
        self.idle()

        if Robot.cycles%8 == 0 : self.spawn(Biodiversite, self.id)

        for i in range(1):
            self.spawn(Pain)
    
    def cultureS(self):

        if self.nbTravailleur < 2 or self.nbSoja < 1 or self.nbBiodiversite < 1 :
            self.brain.setState(self.idle)
        self.idle()

        if Robot.cycles%12 == 0 : self.spawn(Biodiversite, self.id)

        for i in range(1):
            self.spawn(Soja)

    def monocultureC(self):

        if self.nbTravailleur < 1 or self.nbBiodiversite < 1 or self.nbCereale < 1:
            self.brain.setState(self.idle)

        for i in range(3):
            self.spawn(Pain)

    def monocultureS(self):

        if self.nbTracteur < 1 or self.nbBiodiversite < 1 or self.nbSoja < 1:
            self.brain.setState(self.idle)

        for i in range(3):
            self.spawn(Soja)

    def update(self):
        self.nbBiodiversite = self.countByType(Biodiversite)
        self.nbTravailleur = self.countByType(Travailleur)
        self.nbTracteur = self.countByType(Tracteur)
        self.nbPesticide = self.countByType(Pesticide)
        self.nbCereale = self.countByType(Cereale)
        self.nbBeton = self.countByType(Beton)
        self.nbSoja = self.countByType(Soja)
        self.brain.update()


class Foret(Entite):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.nbArbre = 0
        self.nbTravailleur = 0
        self.nbTigreDeSumatra = 0
        self.probatigre = [True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]

    def idle(self):

        if self.nbArbre <= 16:
          self.spawn(Arbre, self.id)

        if Robot.cycles%4 == 0: self.spawn(Arbre, self.id)

        if self.nbTravailleur >= 2:
            self.brain.setState(self.production)

        bob = random.choice(self.probatigre)
        if bob : self.spawn(TigreDeSumatra, self.id)  
        # chaine de markov des pauvres


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
            for x in range(nbTigreDeSumatra):
                self.remove(TigreDeSumatra)

            self.mutate(Champ)


    def update(self):
        self.nbTravailleur = self.countByType(Travailleur)
        self.nbArbre = self.countByType(Arbre)
        self.nbTigreDeSumatra = self.countByType(TigreDeSumatra)
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
            - Biodiversite
            - Anchois

            Représentation sous forme de fichier

    """
    pass

class Arbre(Bio): pass
class TigreDeSumatra(Bio): pass
class Biodiversite(Bio): pass

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
        - Pesticide
        - DechetRadioactif
        - Electricite
        - Tracteur
        - Vehicule
        - Soja
        - Cereale

    Représentation sous forme de fichier

    """
    pass

class Acier(Produit): pass
class Arme(Produit): pass
class Beton(Produit): pass
class Pesticide(Produit): pass
class DechetRadioactif(Produit): pass
class Electricite(Produit): pass
class Metal(Produit): pass
class Phosphate(Produit): pass
class Calcaire(Produit): pass


class Vehicule(Produit): 
    """
        Vehicule
            -Tracteur
            -BateauUsine
    """

    def init(self):
        self.energy = 3

    def idle(self):
        self.energy -= 1
        o = Robot.findOne(Petrole)
        if o:
            self.energy += 1
            o.energy -= 1
            o.update()
        if self.energy < 1:
            self.remove()


class Tracteur(Vehicule): pass
class BateauUsine(Vehicule): pass


class Soja(Produit): pass
class Cereale(Produit): pass

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

class Petrole(Fossile): 

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.energy = 3

    def idle(self):
        if self.energy < 1:
            self.remove()

class Charbon(Fossile): pass
class Uranium(Fossile): pass

class Vivant(Base):
    """
        Vivants
            - Travailleur
            - Ingenieur
            - Soldat
        Représentation sous forme de fichier

    """
    def init(self):
        self.energy = 4

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
            - Pain
            - Poisson

    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.energy = 6

    def idle(self):
        if self.energy < 1:
            self.remove()


class Pain(Nourriture): pass
class Poisson(Nourriture): pass
