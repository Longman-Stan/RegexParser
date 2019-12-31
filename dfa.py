import nfa
try:
    from graphviz import Digraph
except ImportError:
    pass
    

def nfa_to_dfa(nfa):
    alf = nfa.alphabet
    eps_trans = {}
    for i in nfa.states: #determine the epsilon transitions from each state
        stack=[i]
        states_set={i}
        viz_set=set()
        while stack!=[]:
            crt = stack.pop()
            viz_set.add(crt)
            if (crt,"") in nfa.delta:
                for j in nfa.delta[(crt,"")]: 
                    if not j in viz_set:
                        stack.append(j)
                        states_set.add(j)
        eps_trans[i]=states_set
    next_state=1 #build the dfa
    state_dict={}
    state_dict[0]=eps_trans[nfa.start_state] #the new start state is the epsilon transition of the start state of the nfa
    new_start_state=0 
    new_delta={}
    state_stack=[new_start_state] #put the new start state in the stack, as it is the start point
    state_set={frozenset(state_dict[0])} #keep it in a special set to check for duplicates
    #print(state_set)
    while state_stack!=[]: #while there are states to be processed
        crt = state_stack.pop() #get the first one
        for a in alf: #build every transition there is to be built
            next_state_set = set() #add every reachable state by consuming char a to the new set
            for crt_states in state_dict[crt]:
                if (crt_states,a) in nfa.delta:
                    for next_step in nfa.delta[(crt_states,a)]:
                        #print(crt_states,a, next_step, eps_trans[next_step] )
                        next_state_set.update( eps_trans[next_step]) #add the states to the new set
            #print(next_state_set)
            #print(state_set)
            if next_state_set==set(): #if the resultin set was empty, ignore it
                #print("state goes nowhere")
                continue
            if not (next_state_set in state_set): #if it's not in the set of visited states
                #print("new state")
                state_dict[next_state]=next_state_set #build a new state
                new_delta[(crt,a)]=next_state
                state_stack.append(next_state)
                state_set.add(frozenset(next_state_set))
                next_state+=1
                
            else:
                for key,setu in state_dict.items(): #else find the associated state
                    if setu== next_state_set:    
                        cheia = key
                new_delta[(crt,a)]=cheia #and add a new transition
    new_states=set()
    for i in range(0,next_state): #build the dfa states set
        new_states.add(i)
    final_states=set()
    for i in new_states: #and the final states set
        for j in nfa.final_states:
            if j in state_dict[i]:
                final_states.add(i)
                break
   # print(alf)
    #print(new_states)
    #print(new_start_state)
    #print(final_states)
    #print(state_dict)
    #print(new_delta)
    return DFA(alf,new_states,new_start_state,final_states,new_delta) #and build the damn dfa
    

class DFA(object):
    """Model a Nondeterministic Finite Automaton

    The automaton contains the following:

        - "alphabet": a set of symbols
        - "states": set of non-negative integers
        - "start_state": a member of "states"
        - "final_states": a subset of "states"
        - "delta": a dictionary from configurations to states
                {(state, symbol): state}
                where "state" is a member of "states" and "symbol" is a member
                of "alphabet"

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
        self.sink_state = None
        
    def check(self,string):
        state=self.start_state
        i=0
        while i<len(string):
            if (state,string[i]) in self.delta:
                state=self.delta[(state,string[i])]
            else:
                return False
            i+=1
        if state in self.final_states:
            return True
        return False

    def to_graphviz(self):
        def get_edges(delta):
            edges = {}
            for (prev_state, symbol), next_state in delta.items():
                edge = (prev_state, next_state)
                if edge not in edges:
                    edges[edge] = set()

                edges[edge].add(symbol)

            return edges

        def collate_symbols(edge_symbols):
            collated = []
            i = 0
            edge_symbols = sorted(edge_symbols)
            while i < len(edge_symbols):
                range_start = i
                while i + 1 < len(edge_symbols) and \
                      ord(edge_symbols[i + 1]) == ord(edge_symbols[i]) + 1:
                    i += 1

                dist = i - range_start
                if dist >= 2:
                    label = "{}-{}".format(edge_symbols[range_start],
                                           edge_symbols[i])
                    collated.append(label)
                else:
                    collated.append(str(edge_symbols[range_start]))
                    if dist == 1:
                        collated.append(str(edge_symbols[range_start + 1]))
                        i += 1

                i += 1

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
