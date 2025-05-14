# ---------- Task 1: NFA (with epsilon transitions) to DFA Conversion ----------

# Define an example NFA
nfa = {
    'states': {'q0', 'q1', 'q2'},  # set of states
    'symbols': {'a', 'b'},         # input symbols
    'transitions': {               # transition table
        'q0': {'ε': {'q1', 'q2'}},  # epsilon transitions from q0 to q1 and q2
        'q1': {'a': {'q1'}},
        'q2': {'b': {'q2'}}
    },
    'start': 'q0',                # start state
    'finals': {'q1'}              # set of final (accepting) states
}

# Compute epsilon-closure of a single state
def epsilon_closure(state, transitions):
    stack = [state]
    closure = {state}
    while stack:
        s = stack.pop()
        for t in transitions.get(s, {}).get('ε', set()):
            if t not in closure:
                closure.add(t)
                stack.append(t)
    return closure

# Compute epsilon-closure for a set of states
def epsilon_closure_set(states, transitions):
    result = set()
    for state in states:
        result |= epsilon_closure(state, transitions)
    return result

# Move to next states via symbol from current states
def move(states, symbol, transitions):
    result = set()
    for state in states:
        result |= transitions.get(state, {}).get(symbol, set())
    return result

# Convert the NFA to a DFA using the subset construction method
def nfa_to_dfa(nfa):
    dfa_states = []            # List of DFA state sets
    dfa_transitions = {}       # DFA transition table
    state_map = {}             # Maps state sets to DFA state labels

    # Start with the epsilon-closure of the NFA start state
    start_closure = frozenset(epsilon_closure(nfa['start'], nfa['transitions']))
    state_map[start_closure] = 'A'
    dfa_states.append(start_closure)
    queue = [start_closure]    # BFS queue for unprocessed DFA states
    next_label = ord('B')      # Start labeling from 'B'

    while queue:
        current = queue.pop(0)
        label = state_map[current]
        dfa_transitions[label] = {}

        for symbol in nfa['symbols']:
            move_result = move(current, symbol, nfa['transitions'])
            closure = epsilon_closure_set(move_result, nfa['transitions'])
            if not closure:
                continue
            closure_frozen = frozenset(closure)
            if closure_frozen not in state_map:
                state_map[closure_frozen] = chr(next_label)
                next_label += 1
                queue.append(closure_frozen)
            dfa_transitions[label][symbol] = state_map[closure_frozen]

    # Determine final DFA states (those that include any NFA final state)
    final_states = {state_map[s] for s in state_map if nfa['finals'] & s}

    return {
        'states': list(state_map.values()),
        'start': 'A',
        'finals': list(final_states),
        'transitions': dfa_transitions
    }

# Run the conversion and print the resulting DFA
dfa = nfa_to_dfa(nfa)
print("\n--- DFA Result ---")
print("States:", dfa['states'])
print("Start State:", dfa['start'])
print("Final States:", dfa['finals'])
print("Transitions:")
for state in dfa['transitions']:
    print(f"  {state}: {dfa['transitions'][state]}")