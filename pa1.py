# -*- coding: utf-8 -*-
"""
Created on Thu Jan 25 13:13:50 2024

@author: LMOakes
"""
import random as ran, time
from tabulate import tabulate as tab

#function generates requested data in a table format 
#table may be adjusted by changing the starting number of steps or number of runs
def main():
    start_step = 20
    num_runs = 6
    
    #generates table data
    data_prob, data_time  = gen_prob_lists(start_step, num_runs)
    
    print(data_prob)
    
    #creates and prints tables 
    headers_prob = ["Num Steps", "1D", "2D", "3D"]
    prob_table = tab(data_prob, headers_prob, tablefmt="grid")
    
    headers_time = ["Num Steps", "Time for 3D"]
    time_table = tab(data_time, headers_time, tablefmt="grid")
    
    print()
    print("Table for probability of each dimension for number of steps")
    print(prob_table)
    print()
    print("Table for time to run steps of 3D instances")
    print(time_table)
    
    
#function generates each line of table data using nested for loops 
#runs more functions to generate probabilities and random movemements 
def gen_prob_lists(start_step, num_runs):

    lists_of_prob_lists = []
    list_of_times = []
    
    for n in range(num_runs):
        prob_list = [0, 0, 0, 0]
        time_list = [0, 0]
        num_steps = start_step*(10**n)
        prob_list[0] = num_steps
        time_list[0] = num_steps
        
        for d in range(3):
            if d == 2: 
                start_time=time.time()
                
            prob_list[d+1] = run_occurences(num_steps, d)

            if d == 2:
                time_list[d-1] = (time.time() - start_time)
            
        lists_of_prob_lists.append(prob_list)
        list_of_times.append(time_list)
        
    return lists_of_prob_lists, list_of_times
    

#function generates random movement forwards or backwards in random direction
def random_gen(current_value, num_axis):
    while True:
        move = ran.randint(-1, 1)
        
        if move == -1 or move == 1:
            break
        
    direction = ran.randint(0, num_axis)
    current_value[direction] += move

    return current_value
    

#function runs random gen function for the desired number of steps 
#will break and return 1 if origin is reached
def single_occurence(num_steps, num_axis):
    start = [0, 0, 0]
    
    for step in range(num_steps):
        start = random_gen(start, num_axis)
    
        if start == [0, 0, 0]:
            return(1)
            break
        
    return(0)
        

#function runs the above process for a set number of occurences 
#will count and determine probability of particle returning to starting point
def run_occurences(num_steps, num_axis):
    count = 0
    occurences = 1000
    
    for i in range(occurences):
        count += single_occurence(num_steps, num_axis)
        
    probability_origin = (count/occurences) * 100
    
    return probability_origin
        

#runs program
main()


        
