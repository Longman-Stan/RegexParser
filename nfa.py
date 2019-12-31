import regular_expression
import string
try:
    from graphviz import Digraph
except ImportError:
    pass
    
EMPTY_SET = 0
EMPTY_STRING = 1
SYMBOL = 2
STAR = 3
CONCATENATION = 4
ALTERNATION = 5
    
def rename_states(target, reference): #from the regex to nfa colab laboratory
    off = max(reference.states) + 1
    target.start_state += off
    target.states = set(map(lambda s: s + off, target.states))
    target.final_states = set(map(lambda s: s + off, target.final_states))
    new_delta = {}
    for (state, symbol), next_states in target.delta.items():
        new_next_states = set(map(lambda s: s + off, next_states))
        new_delta[(state + off, symbol)] = new_next_states

    target.delta = new_delta


def new_states(*nfas): 
    state = 0
    for nfa in nfas:
        m = max(nfa.states)
        if m >= state:
            state = m + 1
    return state, state + 1

def get_alf(re): #get the alphabet of a regex
  if re.type == EMPTY_SET:
    return ""
  if re.type == EMPTY_STRING:
    return ""
  if re.type == SYMBOL:
    return str(re.symbol)
  if re.type == STAR:
    return get_alf(re.lhs)
  stri=get_alf(re.lhs)+get_alf(re.rhs)
  return "".join(set(stri))

def re_to_nfa(re):
    """Convert a Regular Expression to a Nondeterminstic Finite Automaton"""
    # TODO Thompson's algorithm
    alf =get_alf(re)
    if re.type == EMPTY_SET:
      return NFA(alf,{0},0,set(),dict())
    
    if re.type == EMPTY_STRING:
        return NFA(alf,{0,1},0,{1},{ (0,""):{1}})
      
    if re.type == SYMBOL:
        return NFA(alf,{0,1},0,{1},{ (0,str(re.symbol)):{1}})
                   
    if re.type == STAR:
        nfa = re_to_nfa(re.lhs)
        nfaprinc = NFA( alf, {0,1},0,{1}, { (0,""):{1}});
        rename_states(nfa,nfaprinc)
        nfaprinc.delta[(0,"")].add(nfa.start_state)
        for i in nfa.final_states:
            if (i,"") in nfa.delta:
                nfa.delta[(i,"")].add(1);
            else:
                nfa.delta[(i,"")]={1}

            if (i,"") in nfa.delta:
                nfa.delta[(i,"")].add(nfa.start_state)
            else:
                nfa.delta[(i,"")]={nfa.start_state}
        return NFA(alf,nfaprinc.states.union(nfa.states),0,{1},{**nfa.delta,**nfaprinc.delta})
    
    if re.type == CONCATENATION:
        nfa1 = re_to_nfa(re.lhs)
        nfa2 = re_to_nfa(re.rhs)
        nfaprinc = NFA(alf,{0,1},0,{1},{})
        rename_states(nfa1,nfaprinc)
        nfaprinc.delta[(0,"")]={nfa1.start_state}
        nfaprinc = NFA(alf,nfaprinc.states.union(nfa1.states),0,{1},{**nfaprinc.delta,**nfa1.delta})
      
        rename_states(nfa2,nfaprinc)
        for i in nfa1.final_states:
            if (i,"") in nfa1.delta:
                nfa1.delta[(i,"")].add(nfa2.start_state)
            else:
                nfa1.delta[(i,"")]={nfa2.start_state}
        nfaprinc = NFA(alf,nfaprinc.states.union(nfa1.states),0,{1},{**nfaprinc.delta,**nfa1.delta})
      
       
        for i in nfa2.final_states:
            if (i,"") in nfa2.delta:
                nfa2.delta[(i,"")].add(1)
            else:
                nfa2.delta[(i,"")]={1}

        return NFA(alf,nfaprinc.states.union(nfa2.states.union(nfa1.states)),0,{1},{**nfaprinc.delta,**nfa2.delta})
    
    if re.type == ALTERNATION:
        nfa1 = re_to_nfa(re.lhs)
        nfa2 = re_to_nfa(re.rhs)
        nfaprinc = NFA(alf,{0,1},0,{1},{})
        rename_states(nfa1,nfaprinc)
        nfaprinc.delta[(0,"")]={nfa1.start_state}
        for i in nfa1.final_states:
            if (i,"") in nfa1.delta:
                nfa1.delta[(i,"")].add(1);
            else:
                nfa1.delta[(i,"")]={1}
        nfaprinc = NFA(alf,nfaprinc.states.union(nfa1.states),0,{1},{**nfaprinc.delta,**nfa1.delta})
      
        rename_states(nfa2,nfaprinc)
        nfaprinc.delta[(0,"")].add(nfa2.start_state)
        for i in nfa2.final_states:
            if (i,"") in nfa2.delta:
                nfa2.delta[(i,"")].add(1);
            else:
                nfa2.delta[(i,"")]={1}
        return NFA(alf,nfaprinc.states.union(nfa2.states),0,{1},{**nfaprinc.delta,**nfa2.delta})

class NFA(object):
    """Model a Nondeterministic Finite Automaton

    The automaton contains the following:

        - "alphabet": a set of symbols
        - "states": set of non-negative integers
        - "start_state": a member of "states"
        - "final_states": a subset of "states"
        - "delta": a dictionary from configurations to a set of states
                {(state, word): next_states}
            where a "configuration" is a tuple consisting of a member of
            "states" and a list of 0 or more symbols from "alphabet" and
            "next_states" is a subset of "states"

    """
    def __init__(self, alphabet, states, start_state, final_states, delta):
        """See class docstring"""
        assert start_state in states
        assert final_states.issubset(states)
        for symbol in "()*|":
            assert symbol not in alphabet

        self.alphabet = alphabet
        self.states = states
        self.start_state = start_state
        self.final_states = final_states
        self.delta = delta

    def to_graphviz(self):
        def get_edges(delta):
            edges = {}
            for (prev_state, word), next_states in delta.items():
                for next_state in next_states:
                    edge = (prev_state, next_state)
                    if edge not in edges:
                        edges[edge] = set()

                    edges[edge].add(word)

            return edges

        def collate_symbols(edge_words):
            collated = []
            i = 0
            edge_words = sorted(edge_words)
            if len(edge_words[0]) == 0:  # contains empty string
                collated.insert(0, "ε")
                edge_words = edge_words[1:]

            while i < len(edge_words) and len(edge_words[i]) == 1:
                range_start = i
                while i + 1 < len(edge_words) and \
                      len(edge_words[i + 1]) == 1 and \
                      ord(edge_words[i + 1]) == ord(edge_words[i]) + 1:
                    i += 1

                dist = i - range_start
                if dist >= 2:
                    label = "{}-{}".format(edge_words[range_start],
                                           edge_words[i])
                    collated.append(label)
                else:
                    collated.append(str(edge_words[range_start]))
                    if dist == 1:
                        collated.append(str(edge_words[range_start + 1]))
                        i += 1

                i += 1

            collated += [word for word in edge_words if len(word) > 1]
            return ",".join(collated)

        dot = Digraph()
        dot.graph_attr["rankdir"] = "LR"
        

        # This is here to nicely mark the starting state.
        dot.node("_", shape="point")
        dot.edge("_", str(self.start_state))

        for state in self.states:
            shape = "doublecircle" if state in self.final_states else "circle"
            dot.node(str(state), shape=shape)

        edges = get_edges(self.delta)

        edges = {k: collate_symbols(v) for k, v in edges.items()}
        for (prev_state, next_state), label in edges.items():
            dot.edge(str(prev_state), str(next_state), label=label)

        return dot
