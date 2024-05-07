from typing import List
from utils.hash import get_hash_digest
from . import Grammar, Production, Symbol, Item, State, Behavior, Action
from . import EPSILON, END_OF_INPUT, DOT, logger
from .lr0 import LR0

class SLR1(LR0):
    def __init__(self, productions: List[Production]):
        super().__init__(productions)
        
        
        logger.debug('Checking for conflicts')
        _, conflicts = self.dump_table()
        if conflicts:
            for k, v in conflicts.items():
                logger.error(f'Conflict in state {k[0]} on symbol "{k[1]}" between {v}')
        logger.debug('Done checking for conflicts')
    
        logger.info('Done initializing SLR1')
    def dump_table(self):
        state_table = {}
        
        conflicts = {}
        def _write_to_table(state, symbol, behavior):
            if state_table[state].get(symbol) is None:
                state_table[state][symbol] = behavior
            elif state_table[state].get(symbol) == behavior:
                pass
            else:
                if (state, symbol) not in conflicts:
                    conflicts[(state, symbol)] = [state_table[state][symbol]]
                conflicts[(state, symbol)] += [behavior]
                
        for state in self.states:
            state_table[state] = {}
            for item in state.states:
                if item.is_reduce():
                # TO-DO: detect conflicts
                # if a state is already set, means there is a conflict
                    if item.head != self.start_symbol:
                        for sym in self.get_follow_set()[item.head]:
                            _write_to_table(state, sym, Behavior(Action.REDUCE, item.get_production()))
                    else:
                        _write_to_table(state, Symbol(END_OF_INPUT), Behavior(Action.ACCEPT, 0))
                else:
                    next_sym = item.next_symbol()
                    if next_sym in self._terminals:
                        new_state = self.goto(state, next_sym)
                        _write_to_table(state, next_sym, Behavior(Action.SHIFT, new_state))
                    elif next_sym in self._non_terminals:
                        new_state = self.goto(state, next_sym)
                        _write_to_table(state, next_sym, Behavior(Action.GOTO, new_state))
        return state_table, conflicts