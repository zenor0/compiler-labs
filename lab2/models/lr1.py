from typing import List
from utils.hash import get_hash_digest
from . import Grammar, Production, Symbol, Item, State, Behavior, Action
from . import EPSILON, END_OF_INPUT, DOT

class LR1(Grammar):
    states : List[State]
    state_transition : List
    
    def __init__(self, productions: List[Production]):
        productions, self.start_symbol = self.augment_grammar(productions)
        
        super().__init__(productions)

        self.init_states()
        
        conflicts = self.check_conflict()
        if conflicts:
            print('Conflicts:')
            for conflict in conflicts:
                print(conflict)
        else:
            print('No conflicts')
       
    def init_states(self):
        self.states = []
        self.state_transition = []
        start_item = Item(self.productions[0], 0, [Symbol(END_OF_INPUT)])
        start_state = self.calc_closure(State([start_item]))
        self.states.append(start_state)
        for state in self.states:
            for sym in self._non_terminals + self._terminals:
                new_state = self.goto(state, sym)
                if new_state:
                    self.state_transition.append((state.__hash__(), sym, new_state.__hash__()))
                    if new_state not in self.states:
                        new_state = self.calc_closure(new_state)
                        self.states.append(new_state)
                        
    def calc_closure(self, state: State):
        added = True
        while added:
            added = False
            for item in state.states:
                next_symbol = item.next_symbol()
                if next_symbol is not None and next_symbol in self._non_terminals:
                    calc_first_term = item.body[item.dot_index+1:] + item.lookahead
                    next_first = self.first(calc_first_term)
                    for prod in self.productions:
                        if prod.head == next_symbol:
                            for lookahead in next_first:
                                new_item = Item(prod, 0, [lookahead])
                                if new_item not in state.states:
                                    state.states.append(new_item)
                                    added = False
        return state
    def goto(self, state: State, symbol: Symbol):
        kernel = []
        for item in state.states:
            next_symbol = item.next_symbol()
            if next_symbol == symbol:
                new_item = item.advance()
                new_item.lookahead = item.lookahead
                kernel.append(new_item)
        if kernel == []:
            return None
        return State(kernel)
    

            
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
    
    def dump_table(self):
        state_table = {}
        for state in self.states:
            state_table[get_hash_digest(state)] = {}
            for item in state.states:
                if item.is_reduce():
                    if item.head != self.start_symbol:
                        state_table[get_hash_digest(state)][item.lookahead[0]] = Behavior(Action.REDUCE, self.productions.index(item.get_production()))
                    else:
                        state_table[get_hash_digest(state)][Symbol(END_OF_INPUT)] = Behavior(Action.ACCEPT, 0)
                else:
                    next_sym = item.next_symbol()
                    if next_sym in self._terminals:
                        new_state = self.goto(state, next_sym)
                        state_table[get_hash_digest(state)][next_sym] = Behavior(Action.SHIFT, get_hash_digest(new_state))
                    elif next_sym in self._non_terminals:
                        new_state = self.goto(state, next_sym)
                        state_table[get_hash_digest(state)][next_sym] = Behavior(Action.GOTO, get_hash_digest(new_state))
        return state_table


    def __str__(self):
        info = [f'{super().__str__()}']
        state_name = {}
        for index, state in enumerate(self.states):
            info.append(f'State {index}: {state}')
            state_name[state.__hash__()] = f'State {index}'
        for state_from, by_sym, state_to in self.state_transition:
            info.append(f'{state_name[state_from]} -- {by_sym} -- {state_name[state_to]}')
        return '\n'.join(info)

    def __repr__(self):
        return '\n'.join([str(x) for x in self.states])

    def __eq__(self, other):
        return self.states == other.states

    def __hash__(self):
        return hash(str(self.states))
