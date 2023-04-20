#!/usr/bin/env python3
"""
Developpez votre projet de TP automates finis dans ce fichier.
"""

from contextfree import StackAutomaton, EPSILON, Grammar

def is_deterministic(a):
    for state in a.states:
        transitions = {}
        for symbol in a.input_symbols:
            next_states = a.transitions.get((state, symbol), [])
            if len(next_states) > 1:
                return False
            elif len(next_states) == 1:
                next_state = next_states[0]
                if symbol in transitions and transitions[symbol] != next_state:
                    return False
                transitions[symbol] = next_state
    return True


def is_deterministic(a: 'StackAutomaton') -> bool:
    for state in a.statesdict.values():
        for char in a.alphabet:
            for stack_char in a.stack_alphabet:
                trans_count = len(list(filter(lambda t: t[0] == char and t[1] == stack_char, state.transitions)))
                if trans_count > 1:
                    return False
    return True

def execute(a: 'StackAutomaton', s: str) -> Union[str, bool]:
    if not is_deterministic(a):
        return "ERROR"

    stack = [a.initial_stack_symbol]

    for char in s:
        current_state = a.statesdict[a.current_state]
        transition = None
        for t in current_state.transitions:
            if t[0] == char and t[1] == stack[-1]:
                transition = t
                break
        if not transition:
            return False
        a.current_state = transition[2]
        stack.pop()
        stack.extend(transition[3][::-1])
    
    return a.current_state in a.final_states


def recognizes(a:'StackAutomaton', word:str)->bool:
    currentState = str(a.initial)
    stack = [a.initial_stack]
    charIndex=0
    if word!="%":
        while charIndex<len(word):
            stackHead = stack.pop()
            transitionFound = False
            for (source, letter, head, push, dest) in a.transitions:
                if source==currentState and (letter=="%" or letter==word[charIndex]) and head==stackHead:
                    transitionFound = True
                    if(letter!="%"): #on passe au caractère suivant si c'est pas epsilon
                        charIndex+=1
                    currentState=dest
                    i = len(push)-1
                    while i>=0:
                        stack.append(push[i])
                        i-=1
                    break
            if not transitionFound:
                return False
        
    #plus que des epsilon a voir d'ici car on a lu tous les caractères du mot
    transitionFound = True
    while transitionFound:
        transitionFound = False
        if currentState in a.acceptstates:
            return True
        stackHead = stack.pop()
        for (source, letter, head, push, dest) in a.transitions:
            if source==currentState and letter=="%" and head==stackHead:
                transitionFound = True
                currentState=dest
                i = len(push)-1
                while i>=0:
                    stack.append(push[i])
                    i-=1
                break
    return False

def newName(G : 'Grammar', name=None):
    if name!=None and name not in G.variablesdict:
        return name
    index=0
    while True:
        name = "I" + str(index)
        if name not in G.variablesdict:
            return name
        index+=1
        
##############################################################################

'''Returns if a given grammar is in Chomsky's normal form'''
def is_CNF(G:'Grammar')->bool:
    return checkStep1_CNF(G) and checkStep2_CNF(G) and checkStep3_CNF(G) and checkStep4_CNF(G) and checkStep5_CNF(G)
  
##############################################################################
  
'''Puts the given grammar into Chomsky's normal form'''
def to_CNF(G:'Grammar'):
  step1_CNF(G)
  step2_CNF(G)
  step3_CNF(G)
  step4_CNF(G)
  step5_CNF(G)
  
##############################################################################

'''Checks if the given grammar respects the first step of Chomsky's normal form'''
def checkStep1_CNF(G:'Grammar'):
    start = G.initial.name
    for (source, prod) in G.rules :
        if source==start and start in prod:
            return False
    return True
        

##############################################################################

'''Makes the given grammar respect the first step of Chomsky's normal form'''
def step1_CNF(G:'Grammar'):
  if not checkStep1_CNF(G):
      newInitialName = newName(G, "S0")
      newInitial = Variable(newInitialName)
      G.add_rule(newInitialName,[G.initial.name])
      G.initial = newInitial
  print("step 1 done")


##############################################################################

'''Checks if the given grammar respects the second step of Chomsky's normal form'''
def checkStep2_CNF(G:'Grammar'):
    for (source, prod) in G.rules :
        count = 0
        for symbol in prod:
            if symbol in G.alphabet:
                count+=1
        if count >=2 or (count>=1 and len(prod)>=2) :
            return False
    return True

##############################################################################

'''Makes the given grammar respect the second step of Chomsky's normal form'''
def step2_CNF(G:'Grammar'):
    if not checkStep2_CNF(G):          
        
        #ajout des variables "X" + lettre
        for letter in G.alphabet:
            newVariableName = newName(G, "X" + letter)
            if newVariableName != "X" + letter:
                print("The grammar contains variables named 'X' + an alphabet symbol : please rename these variables")
                return None
            G.add_rule(newVariableName, [letter])
            
        #modifications des regles
        for (source, prod) in G.rules :
            count = 0
            for symbol in prod:
                if symbol in G.alphabet:
                    count+=1
            if count >=2 or (count>=1 and len(prod)>=2) : #on est sur une règle à modifier
                newRule = []
                for symbol in prod:
                    if symbol in G.alphabet:
                        newRule.append("X" + symbol)
                    else :
                        newRule.append(symbol)
                G.add_rule(source, newRule)
                G.remove_rule(source, prod)
    print("step 2 done")


##############################################################################

'''Checks if the given grammar respects the third step of Chomsky's normal form'''
def checkStep3_CNF(G:'Grammar'):
    for (source, prod) in G.rules :
        count=0
        for symbol in prod:
            if symbol in G.variables:
                count+=1
        if count>=3:
            return False
    return True

##############################################################################

'''Makes the given grammar respect the third step of Chomsky's normal form'''
def step3_CNF(G:'Grammar'):
  if not checkStep3_CNF(G):

      for (source, prod) in G.rules :
        count=0
        for symbol in prod:
            if symbol in G.variables:
                count+=1
        if count>=3: #on est sur une regle à réduire
            G.remove_rule(source, prod)
            while count!=2:
                newRule = []
                newVariableName = newName(G)
                newRule.append(prod[0])
                newRule.append(newVariableName)
                G.add_rule(source, newRule)
                source = newVariableName
                prod.pop(0)
                count-=1
            G.add_rule(source, prod)
  print("step 3 done")


##############################################################################

'''Checks if the given grammar respects the fourth step of Chomsky's normal form'''
def checkStep4_CNF(G:'Grammar'):
    for (source, prod) in G.rules :
        if len(prod)==0 and source!=G.initial.name:
            return False
    return True

##############################################################################

'''Makes the given grammar respect the fourth step of Chomsky's normal form'''
def step4_CNF(G:'Grammar'):
  if not checkStep4_CNF(G):

      #recherche des variables annulables
      voidables = []
      lengthChanged = True
      while lengthChanged:
          lengthChanged = False
          for (source, prod) in G.rules :#on regarde si tout ce qu'il y a dans la production est annulable
              allVoidableInProd = True
              for symbol in prod:
                  if symbol not in voidables:
                      allVoidableInProd = False
              if len(prod)==0 or allVoidableInProd: #on a trouvé une variable annulable
                  if source not in voidables:
                      lengthChanged=True
                      voidables.append(source)

      #modification de la grammaire
      for (source, prod) in G.rules :
          indexVoidables = []#tableau contenant les index des anulables dans la regle courante
          newRule = []#on crée une nouvelle régle dans laquelle on va mettre tous les symboles pour le moment (on les enlevera par la suite selon les annulables)
          index = 0
          for symbol in prod:#on cherche les index des annulables et on initialise newRule
              if symbol in voidables:
                  indexVoidables.append(index)
              newRule.append(symbol)
              index+=1
          if len(indexVoidables) == 1:#s'il y a exactement un annulable
              if len(prod)==2:#si la production est de longueur 2, on va essayer d'enlever la variable annulable
                  newRule.pop(indexVoidables[0])
                  G.add_rule(source, newRule)
              else:
                  G.add_rule(source, [])#dans le cas ou il n'y a qu'une seule variable, on ajoute la regle epsilon
          elif len(indexVoidables)==2:#s'il y a deux annulables, on va enlever chacune d'elles, et ajouter la regle epsilon
              newRule2 = newRule.copy()    
              newRule.pop(0)
              G.add_rule(source, newRule)#première variable uniquement enlevée
              newRule2.pop(1)#deuxieme variable uniquement enlevée
              G.add_rule(source, newRule2)
              G.add_rule(source, [])#les deux variables enlevées
      
      #on enleve toutes les regles epsilon sauf celle de de l'axiome si elle existe
      #on enleve en même temps les regles de type S-->S qui ne servent à rien
      for (source, prod) in G.rules :
          if (prod==[] and source!=G.initial.name) or (len(prod)==1 and source==prod[0]):
                G.remove_rule(source, prod)
                                 
  print("step 4 done")


##############################################################################

'''Checks if the given grammar respects the fifth step of Chomsky's normal form'''
def checkStep5_CNF(G:'Grammar'):
    for (source, prod) in G.rules :
        if len(prod)==1 and prod[0] in G.variables:
            return False
    return True

##############################################################################

'''Makes the given grammar respect the fifth step of Chomsky's normal form'''
def step5_CNF(G:'Grammar'):

  ruleAdded = True
  while ruleAdded:
      ruleAdded = False
      for (source, prod) in G.rules :
          if len(prod)==1 and prod[0] in G.variables:#si la regle est unitaire
              for (src, rule) in G.rules :
                  if src == prod[0]:
                      G.add_rule(source, rule)
                      ruleAdded=True
              G.remove_rule(source, prod)
         
  print("step 5 done")


def CYK(G, word):
    
    if not is_CNF(G):
        to_CNF(G)

    #cas du mot vide
    if word=="":
        for (source, prod) in G.rules :
            if source==G.initial.name and prod==[]:
                return True
        return False

    #création du tableau de facteurs
    factors = []
    for i in range(0,len(word)):
        factors.append([])
        for j in range(0, len(word) + 1):
            factors[i].append(set())
            
    #initialisation premiere ligne (facteurs de longueur 1)
    factorLength = 1
    for left in range(0, len(word) - factorLength + 1):
        right = left + 1
        character = word[left]
        for (source, prod) in G.rules :
            if len(prod)==1 and character == prod[0]:
                factors[left][right].add(str(source))
            
    #complétion des autres cases du tableau
    for factorLength in range(2, len(word)+1):
        for left in range(0, len(word) - factorLength + 1):
            right = left + factorLength
            for middle in range(left+1, right):
                for (source, prod) in G.rules :
                    if len(prod)==2 and prod[0] in factors[left][middle] and prod[1] in factors[middle][right]:
                        factors[left][right].add(str(source))
    
    return G.initial.name in factors[0][len(word)]


if __name__ == "__main__": # If the module is run from command line, test it
    # a=StackAutomaton("aut")
    # # a.add_transition("0","a","Z0",["A","Z0"],"1")
    # # a.add_transition("1","b","A",[],"0")
    # # a.set_initialstate("0")
    # # a.set_initialstack("Z0")
    # # a.make_final("1")
    # # a.to_txtfile("/home/yukino/Works/Langages formels/projet-tp-langages/tests/automaton0.pa")
    # a.from_txtfile("/home/yukino/Works/Langages formels/projet-tp-langages/tests/automaton0.pa")
    # print(a)
    # #//////////////////////////////
    # a1=StackAutomaton("aut1")
    # a1.from_txtfile("/home/yukino/Works/Langages formels/projet-tp-langages/tests/automaton1.pa")
    # print(a1)
    # #//////////////////////////////
    # a2=StackAutomaton("aut2")
    # a2.from_txtfile("/home/yukino/Works/Langages formels/projet-tp-langages/tests/automaton2.pa")
    # print(a2)
    # #//////////////////////////////
    # print(a1.get_alphabet())
    # print(a1.get_stackalphabet())
    # print(a1.get_states())
    # print(a1.get_transitions())
    #////////////////////////////////
    g=Grammar("gr")
    # g.add_rule("X",["a","X","a"])
    # g.add_rule("X",["a","a"])
    # g.set_axiom("X")
    g.from_txtfile("/home/yukino/Works/Langages formels/projet-tp-langages/tests/grammar0.gr")
    print(g)
    #////////////////////////////////
    g1=Grammar("gr1")
    g1.from_txtfile("/home/yukino/Works/Langages formels/projet-tp-langages/tests/grammar1.gr")
    print(g1)
    #////////////////////////////////
    g2=Grammar("gr2")
    g2.from_txtfile("/home/yukino/Works/Langages formels/projet-tp-langages/tests/grammar2.gr")
    print(g2)
    #////////////////////////////////
    print(g1.get_alphabet())
    print(g1.get_symbolalphabet())
    print(g1.get_rules())
    