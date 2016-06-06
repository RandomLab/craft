# -*- coding: utf-8 -*-
class FSM(object):
    def __init__(self, initial_state):
        self.current_state = initial_state
    def setState(self, state):
        self.current_state = state
    def update(self):
        print("Updating Brain...")
        self.current_state()

class StackFSM(object):
    def __init__(self, initial_state):
        self.initial_state = initial_state
        self.stack = [initial_state]
    def getCurrentState(self):
        if len(self.stack) > 0:
            return self.stack[-1]
        else:
            return self.initial_state
    def setState(self, state):
        self.popState()
        self.pushState(state)
    def popState(self):
        if len(self.stack) > 0:
            return self.stack.pop()
        return self.initial_state
    def pushState(self, state):
        if self.getCurrentState() != state:
            self.stack.append(state)
    def update(self):
        current_state = self.getCurrentState()
        current_state()


if __name__ == "__main__":
    class ChampExample(object):
        def __init__(self, name):
            self.name = name
            self.tracteur = False
            self.ouvrier = False
            self.pesticide = False
            self.nbOuvriers = 0
            self.aliment = random.choice(["Blé", "Mais", "Semoule"])
            self.brain = FSM(self.idle)
            self.rendement = 0
        def idle(self):
            print("Idle", self)
            if self.nbOuvriers >= 5:
                self.brain.setState(self.production)
            if self.tracteur and self.ouvrier and self.pesticide:
                self.brain.setState(self.monoculture)
        def production(self):
            self.rendement += 1
            if self.nbOuvriers < 5:
                self.brain.setState(self.idle)
            print("Production", self)

        def monoculture(self):
            self.rendement += 5
            if not (self.tracteur and self.ouvrier and self.pesticide):
                self.brain.setState(self.idle)
            print("Monoculture", self)

        def update(self):
            self.brain.update()
            # update champ here
        def __str__(self):
            #return self.name + " : " + str(self.nbOuvriers) + " " + str(self.tracteur) + " " + str(self. ouvrier) + " " + str(self.pesticide)
            return self.name + " " + self.aliment + " " + str(self.rendement)
    champ = ChampExample("Champ 1")

    for i in range(150):
        champ.nbOuvriers = random.choice([1,5,5,5,2,3,2,55])
        champ.tracteur = champ.ouvrier = champ.pesticide = random.choice([False, False, False, True, True])
        champ.update()
