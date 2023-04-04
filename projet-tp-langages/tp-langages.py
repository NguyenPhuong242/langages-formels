#!/usr/bin/env python3
"""
Developpez votre projet de TP automates finis dans ce fichier.
"""

from contextfree import StackAutomaton, EPSILON, Grammar

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
    