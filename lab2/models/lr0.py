from typing import List
from utils.hash import get_hash_digest
from . import Grammar, Production, Symbol, Item, State, Behavior, Action
from . import EPSILON, END_OF_INPUT, DOT, logger

class LR0(Grammar):
    states : List[State]
    state_transition : List
    
    def __init__(self, productions: List[Production]):
        productions, self.start_symbol = self.augment_grammar(productions)
        
        super().__init__(productions)

        self.init_states()
        
        logger.info('Done initializing LR0')
        
        
        logger.debug('Checking for conflicts')
        _, conflicts = self.dump_table()
        if conflicts:
            for k, v in conflicts.items():
                logger.error(f'Conflict in state {k[0]} on symbol "{k[1]}" between {v}')
        logger.debug('Done checking for conflicts')

    def calc_closure(self, state: State):
        added = True
        while added:
            added = False
            for item in state.states:
                next_symbol = item.next_symbol()
                if next_symbol is not None and next_symbol in self._non_terminals:
                    for prod in self.productions:
                        if prod.head == next_symbol:
                            new_item = Item(prod, 0)
                            if new_item not in state.states:
                                state.states.append(new_item)
                                added = True
        return state
    
    def goto(self, state: State, symbol: Symbol):
        kernel = []
        for item in state.states:
            next_symbol = item.next_symbol()
            if next_symbol == symbol:
                kernel.append(item.advance())
        if kernel == []:
            return None
        return State(kernel)
    
    def init_states(self):
        self.states = []
        self.state_transition = []
        start_item = Item(self.productions[0], 0)
        start_state = self.calc_closure(State([start_item]))
        self.states.append(start_state)
        for state in self.states:
            for sym in self._non_terminals + self._terminals:
                new_state = self.goto(state, sym)
                if new_state:
                    self.state_transition.append((state, sym, new_state))
                    if new_state not in self.states:
                        new_state = self.calc_closure(new_state)
                        self.states.append(new_state)

        return self.states
    
    def check_conflict(self):
        conflicts = []
        for state in self.states:
            reduce = False
            shift = False
            for item in state.states:
                if item.is_reduce():
                    if reduce:
                        conflicts.append(f'{state} reduce-reduce conflict')
                        break
                    if shift:
                        conflicts.append(f'{state} shift-reduce conflict')
                        break
                    reduce = True
                else:
                    if reduce:
                        conflicts.append(f'{state} shift-reduce conflict')
                        break
                    shift = True
                    
        return conflicts
    
    def dump_table(self) -> tuple[dict, dict]:
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
                    if item.head != self.start_symbol:
                        for sym in self._terminals:
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
    
    def dump_state_names(self):
        state_name = {}
        for index, state in enumerate(self.states):
            state_name[state] = f'{index}'
        return state_name

    def __str__(self):
        info = [f'{super().__str__()}']
        state_name = {}
        for index, state in enumerate(self.states):
            info.append(f'State {index}: {state}')
            state_name[state] = f'State {index}'
        for state_from, by_sym, state_to in self.state_transition:
            info.append(f'{state_name[state_from]} -- {by_sym} -- {state_name[state_to]}')
        return '\n'.join(info)

    def __repr__(self):
        return '\n'.join([str(x) for x in self.states])

    def __eq__(self, other):
        return self.states == other.states

    def __hash__(self):
        return hash(str(self.states))
