# test read in from string

# test first set parse
# test follow set parse

from model import Symbol, Production, Grammar, Item

def test_symbol():
    s1 = Symbol('a')
    s2 = Symbol('a')
    s3 = Symbol('b')
    epsilon = Symbol(Symbol.EPSILON)
    assert s1 == s2
    assert s1 != s3
    assert str(s1) == 'a'
    assert str(s3) == 'b'
    assert repr(s1) == 'a'
    assert repr(s3) == 'b'
    assert hash(s1) == hash(s2)
    assert hash(s1) != hash(s3)
    assert hash(epsilon) == hash(Symbol(Symbol.EPSILON))
    
def test_production():
    s1 = Symbol('S')
    s2 = Symbol('A')
    s3 = Symbol('B')
    p1 = Production(s1, [s2, s3])
    p2 = Production(s1, [s2, s3])
    p3 = Production(s1, [s3, s2])
    assert p1 == p2
    assert p1 != p3
    assert str(p1) == 'S -> A B'
    assert str(p3) == 'S -> B A'
    assert repr(p1) == 'S -> A B'
    assert repr(p3) == 'S -> B A'
    assert hash(p1) == hash(p2)
    assert hash(p1) != hash(p3)
    
def test_grammar():
    s = Symbol('S')
    a = Symbol('a')
    b = Symbol('b')
    c = Symbol('c')
    p1 = Production(s, [a, b, c])
    p2 = Production(s, [a, b, c])
    p3 = Production(s, [a, b])
    g = Grammar([p1, p3])
    assert p1 in g
    assert p2 in g
    assert p3 in g
    assert str(g) == 'S -> a b c\nS -> a b'
    assert repr(g) == 'S -> a b c\nS -> a b'
    assert hash(g) == hash(Grammar([p1, p3]))
    assert hash(g) != hash(Grammar([p1, p2]))
    assert hash(g) != hash(Grammar([p1]))
    assert hash(g) != hash(Grammar([p3]))
    
def test_item():
    s = Symbol('S')
    a = Symbol('a')
    b = Symbol('b')
    c = Symbol('c')
    p1 = Production(s, [a, b, c])
    i1 = Item(p1, 1)
    i2 = Item(p1, 1)
    i3 = Item(p1, 2)
    assert i1 == i2
    assert i1 != i3
    assert str(i1) == 'S -> a . b c'
    assert str(i3) == 'S -> a b . c'
    assert repr(i1) == 'S -> a . b c'
    assert repr(i3) == 'S -> a b . c'
    assert hash(i1) == hash(i2)
    assert hash(i1) != hash(i3)
    
    
def test_first_follow():
    """
    S -> A B 
    S -> b C
    A -> <epsilon>
    A -> b
    B -> <epsilon>
    B -> a D
    C -> A D
    C -> b
    D -> a S
    D -> c
    """
    grammar = Grammar([
        Production(Symbol('S'), [Symbol('A'), Symbol('B')]),
        Production(Symbol('S'), [Symbol('b'), Symbol('C')]),
        Production(Symbol('A'), [Symbol(Symbol.EPSILON)]),
        Production(Symbol('A'), [Symbol('b')]),
        Production(Symbol('B'), [Symbol(Symbol.EPSILON)]),
        Production(Symbol('B'), [Symbol('a'), Symbol('D')]),
        Production(Symbol('C'), [Symbol('A'), Symbol('D')]),
        Production(Symbol('C'), [Symbol('b')]),
        Production(Symbol('D'), [Symbol('a'), Symbol('S')]),
        Production(Symbol('D'), [Symbol('c')]),
    ])
    
    """ FIRST(S)={ ε,a,b } 
        FIRST(A)={ ε,b }   
        FIRST(B)={ ε,a }
        FIRST(C)={ a,b,c }  
        FIRST(D)={ a,c }
    """
    first = {
        Symbol('S'): {Symbol(Symbol.EPSILON), Symbol('a'), Symbol('b')},
        Symbol('A'): {Symbol(Symbol.EPSILON), Symbol('b')},
        Symbol('B'): {Symbol(Symbol.EPSILON), Symbol('a')},
        Symbol('C'): {Symbol('a'), Symbol('b'), Symbol('c')},
        Symbol('D'): {Symbol('a'), Symbol('c')},
    }
    
    follow = {
        Symbol('S'): {Symbol('$')},
        Symbol('A'): {Symbol('$'), Symbol('a'), Symbol('c')},
        Symbol('B'): {Symbol('$')},
        Symbol('C'): {Symbol('$')},
        Symbol('D'): {Symbol('$')},
    }
    
    for production in grammar:
        assert grammar.first(production.head) == first[production.head]
        assert grammar.follow(production.head) == follow[production.head]

def test_first_follow_case2():
    '''
    E -> T E'
    E' -> + T E'
    E' -> <epsilon>
    T -> F T'
    T' -> * F T'
    T' -> <epsilon>
    F -> ( E )
    F -> id
    '''
    
    
    grammar = Grammar([
        Production(Symbol('E'), [Symbol('T'), Symbol("E'")]),
        Production(Symbol("E'"), [Symbol('+'), Symbol('T'), Symbol("E'")]),
        Production(Symbol("E'"), [Symbol(Symbol.EPSILON)]),
        Production(Symbol('T'), [Symbol('F'), Symbol("T'")]),
        Production(Symbol("T'"), [Symbol('*'), Symbol('F'), Symbol("T'")]),
        Production(Symbol("T'"), [Symbol(Symbol.EPSILON)]),
        Production(Symbol('F'), [Symbol('('), Symbol('E'), Symbol(')')]),
        Production(Symbol('F'), [Symbol('id')]),
    ])
    
    first = {
        Symbol('E'): {Symbol('('), Symbol('id')},
        Symbol("E'"): {Symbol('+'), Symbol(Symbol.EPSILON)},
        Symbol('T'): {Symbol('('), Symbol('id')},
        Symbol("T'"): {Symbol('*'), Symbol(Symbol.EPSILON)},
        Symbol('F'): {Symbol('('), Symbol('id')},
    }
    
    follow = {
        Symbol('E'): {Symbol(Symbol.END), Symbol(')')},
        Symbol("E'"): {Symbol(Symbol.END), Symbol(')')},
        Symbol('T'): {Symbol('+'), Symbol(Symbol.END), Symbol(')')},
        Symbol("T'"): {Symbol('+'), Symbol(Symbol.END), Symbol(')')},
        Symbol('F'): {Symbol('*'), Symbol('+'), Symbol(Symbol.END), Symbol(')')},
    }
    
    for production in grammar:
        assert grammar.first(production.head) == first[production.head]
        assert grammar.follow(production.head) == follow[production.head]