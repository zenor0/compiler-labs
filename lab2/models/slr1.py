from typing import List
from utils.hash import get_hash_digest
from . import Grammar, Production, Symbol, Item, State, Behavior, Action
from . import EPSILON, END_OF_INPUT, DOT
from .lr0 import LR0

class SLR1(LR0):
    def __init__(self, productions: List[Production]):
        super().__init__(productions)
    
    def dump_table(self):
        state_table = {}
        for state in self.states:
            state_table[state] = {}
            for item in state.states:
                if item.is_reduce():
                # TO-DO: detect conflicts
                # if a state is already set, means there is a conflict
                    if item.head != self.start_symbol:
                        for sym in self.get_follow_set()[item.head]:
                            state_table[state][sym] = Behavior(Action.REDUCE, self.productions.index(item.get_production()))
                    else:
                        state_table[state][Symbol(END_OF_INPUT)] = Behavior(Action.ACCEPT, 0)
                else:
                    next_sym = item.next_symbol()
                    if next_sym in self._terminals:
                        new_state = self.goto(state, next_sym)
                        state_table[state][next_sym] = Behavior(Action.SHIFT, new_state)
                    elif next_sym in self._non_terminals:
                        new_state = self.goto(state, next_sym)
                        state_table[state][next_sym] = Behavior(Action.GOTO, new_state)
        return state_table