# -*- coding: utf-8 -*-
import time, os, sys

from pymsgbox import alert
from FSM import FSM, StackFSM
from robot import Robot



"""
    # TODO :
    Icon
    Mutation X --> il faut que Jackda m'expliquasse
    Dossier Partagé

    ré-implémenter la monoculture
    faire crafter un fichier de plante aléatoire dans l'init du champ

    vérifier que la mer marche bien

    class d'anchois qui vieillit
    implémenter le remove qui prend des arguments

"""

from config import base_path



"""
#ce tableau tu peux t'en servir pour piocher des ressources au hasard
entites = [Champ, Monoculture, Elevage, ElevageIntensif, Tissage, BTP, Hopital, Universite, CentraleSol, CentraleAtom, CentraleThermique, GenieMecanique, Arsenal, IndustrieChimique, Acierie, Aeronautique, Electronique, Banque, Assurance, GisementPetrole, GisementCharbon, GisementMetaux, GisementMetauxPrecieux, GisementUranium, MineCharbon, PuitsPetrole, MineUranium, MineMetaux, MineMetauxPrecieux, Ville, Megapole, Megalopole, Foret, Mer, DechargeAtomique, Frontiere]
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


#alert(text = "Ready?", title="Fuck a duck and try to fly", button = "Ok")

robot = Robot()
# Robot(secondes=1)
robot.run()
