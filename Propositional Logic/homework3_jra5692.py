
############################################################
# Imports
############################################################



############################################################
# Section 1: Propositional Logic
############################################################

class Expr(object):
    def __hash__(self):
        return hash((type(self).__name__, self.hashable))

class Atom(Expr):
    def __init__(self, name):
        self.name = name
        self.hashable = name
    def __hash__(self):
        return super().__hash__()
    def __eq__(self, other):
        if isinstance(other, Atom) and self.name == other.name:
            return True
        else:
            return False
    def __repr__(self):
        return f"Atom({self.name})"
    def atom_names(self):
        return {self.name}
    def evaluate(self, assignment):
        return assignment[self.name]
    def to_cnf(self):
        return self

class Not(Expr):
    def __init__(self, arg):
        self.arg = arg
        self.hashable = arg
    def __hash__(self):
        return super().__hash__()
    def __eq__(self, other):
        if isinstance(other, Not) and self.arg == other.arg:
            return True
        else:
            return False
    def __repr__(self):
        return f"Not({repr(self.arg)})"
    def atom_names(self):
        return self.arg.atom_names()
    def evaluate(self, assignment):
        return not self.arg.evaluate(assignment)
    def to_cnf(self):
        if isinstance(self.arg, Atom):
            return Not(self.arg)
        elif isinstance(self.arg, Not):
            return self.arg.arg.to_cnf()
        elif isinstance(self.arg, And):
            return Or(*(Not(c).to_cnf() for c in self.arg.conjuncts)).to_cnf()
        elif isinstance(self.arg, Or):
            return And(*(Not(d).to_cnf() for d in self.arg.disjuncts)).to_cnf()
        else:
            return Not(self.arg.to_cnf())
        
class And(Expr):
    def __init__(self, *conjuncts):
        helperSet = set()
        for conjunct in conjuncts:
            if isinstance(conjunct, And):
                helperSet.update(conjunct.conjuncts)
            else:
                helperSet.add(conjunct)
        self.conjuncts = frozenset(helperSet)
        self.hashable = self.conjuncts
    def __hash__(self):
        return super().__hash__()
    def __eq__(self, other):
        return isinstance(other, And) and self.conjuncts == other.conjuncts
    def __repr__(self):
        returnStr = ', '.join(repr(r) for r in self.conjuncts)
        return f"And({returnStr})"
    def atom_names(self):
        newSet = set()
        for i in self.conjuncts:
            newSet.update(i.atom_names())
        return newSet
    def evaluate(self, assignment):
        for i in self.conjuncts:
            if not i.evaluate(assignment):
                return False
        return True
    def to_cnf(self):
        helperLst = []
        itemCnf = [c.to_cnf() for c in self.conjuncts]

        for conjunct in itemCnf:
            if isinstance(conjunct, And):
                helperLst.extend(conjunct.conjuncts)
            else:
                helperLst.append(conjunct)

        return And(*helperLst)

class Or(Expr):
    def __init__(self, *disjuncts):
        helperSet = set()
        for disjunct in disjuncts:
            if isinstance(disjunct, Or):
                helperSet.update(disjunct.disjuncts)
            else:
                helperSet.add(disjunct)
        self.disjuncts = frozenset(helperSet)
        self.hashable = self.disjuncts
    def __hash__(self):
        return super().__hash__()
    def __eq__(self, other):
        if isinstance(other, Or) and self.disjuncts == other.disjuncts:
            return True
        else:
            return False
    def __repr__(self):
        returnStr = ', '.join(repr(r) for r in self.disjuncts)
        return f"Or({returnStr})"
    def atom_names(self):
        newSet = set()
        for i in self.disjuncts:
            newSet.update(i.atom_names())
        return newSet
    def evaluate(self, assignment):
        for i in self.disjuncts:
            if i.evaluate(assignment):
                return True
        return False
            
    def to_cnf(self):
        helperLst = []
        helperLst2 = []
        helperLst3 = []
        helperLst4 = []
        disjuncts = [disJ.to_cnf() for disJ in self.disjuncts]
        
        if any(isinstance(disJ, And) for disJ in disjuncts):
            for disjunct in disjuncts:
                if isinstance(disjunct, And):
                    helperLst.append(disjunct)
                else:
                    helperLst2.append(disjunct)
            
            for conjunct in helperLst[0].conjuncts:
                helperLst3.append(Or(conjunct, *helperLst2).to_cnf())
            
            for andStatement in helperLst[1:]:
                helperLst4 = []
                for item1 in andStatement.conjuncts:
                    for item2 in helperLst3:
                        if isinstance(item2, And):
                            helperLst4.append(Or(item1, *item2.conjuncts).to_cnf())
                        else:
                            helperLst4.append(Or(item1, item2).to_cnf())
                helperLst3 = helperLst4

            return And(*helperLst3).to_cnf()
        
        return Or(*disjuncts)

class Implies(Expr):
    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.hashable = (left, right)
    def __hash__(self):
        return super().__hash__()
    def __eq__(self, other):
        return isinstance(other, Implies) and self.left == other.left and self.right == other.right
    def __repr__(self):
        return f"Implies({repr(self.left)}, {repr(self.right)})"
    def atom_names(self):
        return self.left.atom_names().union(self.right.atom_names())
    def evaluate(self, assignment):
        if self.left.evaluate(assignment) == False and self.right.evaluate(assignment) == True:
            return True
        elif self.left.evaluate(assignment) == True and self.right.evaluate(assignment) == True:
            return True
        elif self.left.evaluate(assignment) == False and self.right.evaluate(assignment) == False:
            return True
        return False
    def to_cnf(self):
        a = Not(self.left).to_cnf()
        b = self.right.to_cnf()
        return Or(a, b).to_cnf()

class Iff(Expr):
    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.hashable = (left, right)
    def __hash__(self):
        return super().__hash__()
    def __eq__(self, other):
        if isinstance(other, Iff) and (self.left == other.left and self.right == other.right):
            return True
        elif isinstance(other, Iff) and (self.left == other.right and self.right == other.left):
            return True
        else:
            return False
    def __repr__(self):
        return f"IFF({repr(self.left)}, {repr(self.right)})"
    def atom_names(self):
        return self.left.atom_names().union(self.right.atom_names())
    def evaluate(self, assignment):
        return self.left.evaluate(assignment) == self.right.evaluate(assignment)
    def to_cnf(self):
        a = Implies(self.left, self.right).to_cnf()
        b = Implies(self.right, self.left).to_cnf()
        return And(a, b).to_cnf()

def getPermutationsTF(length):
    returnLst = []
    if length == 0:
        return [[]]
    
    recursiveComb = getPermutationsTF(length - 1)

    for combo in recursiveComb:
        returnLst.append(combo + [True])
        returnLst.append(combo + [False])
    
    return returnLst

def satisfying_assignments(expr):
    atom_names = list(expr.atom_names())
    length = len(atom_names)
    permutations = getPermutationsTF(length)
    currDict = {}

    for perm in permutations:
        for j in range(length):
            currDict[atom_names[j]] = perm[j]
        if expr.evaluate(currDict):
            yield currDict.copy()


class KnowledgeBase(object):
    def __init__(self):
        self.facts = set()
    def get_facts(self):
        return self.facts
    def tell(self, expr):
        cnf_expr = expr.to_cnf()
        if isinstance(cnf_expr, And):
            for conjunct in cnf_expr.conjuncts:
                self.facts.add(conjunct)
        else:
            self.facts.add(cnf_expr)
    def ask(self, expr):
        atom_names = set()

        for fact in self.facts:
            atom_names.update(fact.atom_names())
        if not expr.atom_names().issubset(atom_names):
            return False
        
        expression = And(*self.facts)
        satisfying = list(satisfying_assignments(expression))


        for assignment in satisfying:
            if not expr.evaluate(assignment):
                return False
                
        return True



############################################################
# Section 2: Logic Puzzles
############################################################

# Puzzle 1

kb1 = KnowledgeBase()

mythical = Atom("mythical")
mammal = Atom("mammal")
horned = Atom("horned")
mortal = Atom("mortal")
magical = Atom("magical")

kb1.tell(Implies(mythical, Not(mortal)))
kb1.tell(Implies(Not(mythical), And(mortal, mammal)))
kb1.tell(Implies(Or(Not(mortal), mammal), horned))
kb1.tell(Implies(horned, magical))

mythical_query = kb1.ask(mythical)
magical_query = kb1.ask(magical)
horned_query = kb1.ask(horned)


is_mythical = False
is_magical = True
is_horned = True

# Puzzle 2
john = Atom("j")
mary = Atom("m")
ann = Atom("a")

party_constraints = And(Implies(Or(mary, ann), john), Implies(Not(mary), ann), Implies(ann, Not(john)))

valid_scenarios = list(satisfying_assignments(party_constraints))


puzzle_2_question = """
[{'m': True, 'a': False, 'j': True}]
"""

# Puzzle 3

kb3 = KnowledgeBase()
room_one_prize = Atom("p1")
room_one_empty = Atom("e1")
room_two_prize = Atom("p2")
room_two_empty = Atom("e2")
sign_one_true = Atom("s1")
sign_two_true = Atom("s2")
sign_one = Iff(sign_one_true, And(room_one_prize, room_two_empty))
sign_two = Iff(sign_two_true, And(Or(room_one_prize, room_two_prize), Or(room_two_empty, room_one_empty)))
if_sign_one = Iff(sign_one_true, Not(sign_two_true))
kb3.tell(sign_one)
kb3.tell(sign_two)
kb3.tell(if_sign_one)

# Puzzle 4

kb4 = KnowledgeBase()

adams_innocent = Atom("ia")
adams_knew = Atom("ka")
brown_innocent = Atom("ib")
brown_knew = Atom("kb")
clark_innocent = Atom("ic")
clark_knew = Atom("kc")
adams_statement = Implies(adams_innocent, And(Not(clark_knew), brown_knew))
browns_statement = Implies(brown_innocent, Not(brown_knew))
clarks_statement = Implies(clark_innocent, And(brown_knew, adams_knew, Or(Not(brown_innocent), Not(adams_innocent))))
kb4.tell(Or(And(Not(adams_innocent), brown_innocent, clark_innocent), And(adams_innocent, Not(brown_innocent), clark_innocent), And(adams_innocent, brown_innocent, Not(clark_innocent))))
kb4.tell(adams_statement)
kb4.tell(browns_statement)
kb4.tell(clarks_statement)


guilty_suspect = "Brown"