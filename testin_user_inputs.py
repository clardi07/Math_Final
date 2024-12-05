#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Dec 1 20:18:17 2024

@author: p21clardi
"""

def viterbi_algorithm(observations, states, start_probs, trans_probs, emit_probs):
   
    # Starts the probability table and creates path tracker
    prob_table = [{}]
    path_tracker = {}

    # Initialization step
    for state in states:
        prob_table[0][state] = start_probs[state] * emit_probs[state][observations[0]]
        path_tracker[state] = [state]

    #Iterative step
    for t in range(1, len(observations)):
        prob_table.append({})
        new_tracker = {}

        for curr_state in states:
            max_prob, prev_state = max(
                (prob_table[t - 1][prev_state] * trans_probs[prev_state][curr_state] 
                 * emit_probs[curr_state][observations[t]], prev_state)
                for prev_state in states)
            
            prob_table[t][curr_state] = max_prob
            new_tracker[curr_state] = path_tracker[prev_state] + [curr_state]

        path_tracker = new_tracker

    #Finds the most probable final state and its path
    final_prob, final_state = max((prob_table[-1][state], state) for state in states)
    return final_prob, path_tracker[final_state]

#Prompt user for inputs needed for Viterbi
states = tuple(input("Enter the states separated by commas: ").split(','))

observations = tuple(input("Enter the observations separated by commas: ").split(','))

#Start probabilities
start_probabilities = {}
for state in states:
    start_probabilities[state] = float(input(f"Enter the starting probability for state '{state}': "))

#Transition mprobabilites for matrix
transition_probabilities = {}
for state in states:
    transition_probabilities[state] = {}
    for next_state in states:
        transition_probabilities[state][next_state] = float(input(f"Enter the probability of transitioning from '{state}' to '{next_state}': "))

#Emission probabilites for matrix
emission_probabilities = {}
unique_observations = set(observations)
for state in states:
    emission_probabilities[state] = {}
    for observation in unique_observations:
        emission_probabilities[state][observation] = float(input(f"Enter the probability of observing '{observation}' in state '{state}': "))

#Run the Viterbi function
result = viterbi_algorithm(observations, states, start_probabilities, 
                           transition_probabilities, emission_probabilities)

#Output 
print("\nMost probable sequence probability:", result[0])
print("Most probable sequence of states:", " → ".join(result[1]))
