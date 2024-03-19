# -*- coding: utf-8 -*-
"""
Created on Thu Feb 15 13:34:57 2024

@author: LMOakes
"""

import random as rand
from tabulate import tabulate as tab

#Given Queue class
class Queue:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []
    
    def enqueue(self, item):
        self.items.insert(0,item)

    #change to dequeue method to return item popped from queue
    def dequeue(self):
        self.out = self.items.pop()
        return self.out

    def size(self):
        return len(self.items)
    
#Class customer takes in rate_per_item to calculate total time for checkout
class Customer:
    def __init__(self, rate_per_item ):
        self.items = rand.randint(6, 20)
        self.rate_per_item = rate_per_item
        self.time_for_just_items = self.items*self.rate_per_item
        self.time_to_checkout = self.time_for_just_items + 45
    
    #Track simulation seconds for total and item time
    #until item time gets below 0 then stop subtracting
    def subtract_second_from_checkout_time(self):
        self.time_to_checkout -= 1
        if self.time_for_just_items > -1:
            self.time_for_just_items -= 1
    
    #Following are get methods to access Customer object data for each instance
    def get_items(self):
        return self.items
    
    def get_time_to_checkout(self):
        return self.time_to_checkout
        
    #Special get method that checks and returns boolean if a Customer has less than 10 items 
    def get_less_than_10(self):
        if self.items < 10:
            return True
        else:
            return False
    
    def get_time_for_items(self):
        return self.time_for_just_items

#Class register takes in a name and a boolean value to represent express of not
class Register:
    def __init__(self, is_express_lane, reg_name):
        self.is_express_lane = is_express_lane
        self.reg_name = reg_name
        self.queue_of_customer = Queue()
        self.total_time_customers_waiting = 0
        self.total_num_customers_served = 0
        self.total_idle_time = 0
        self.current_customer = None
        self.total_items = 0
        self.avg_wait_time = 0
     
    #Adds a customer to Register by either updating current customer
    #or adding customer to Register queue is there is a current customer
    def add_customer_to_queue(self, Customer):
        if self.current_customer == None:
            self.current_customer = Customer
        else:
            self.queue_of_customer.enqueue(Customer)
    
    #Removes a customer from the Register by either removing current customer
    #or removing a customer from the queue using deque method
    #using the dequeue method will alos update the current customer 
    #either case will add to total number of customers served
    def remove_customer_from_queue(self):
        if self.queue_of_customer.size() == 0:
            self.current_customer = None
        else:
            self.current_customer = self.queue_of_customer.dequeue()
        self.total_num_customers_served += 1
    
    #Check if Register is empty, including current customer and queue of customers
    #returns boolean value
    #also adds to simulated idle time if empty to reduce the need for redundant if statements 
    def check_if_empty(self):
        if self.current_customer == None and self.queue_of_customer.size() == 0:
            self.total_idle_time += 1
            return True
        else:
            return False
    
    #Following methods add simulated time oritems to respective variables
    def total_time_customers_waiting_plus_one(self):
        self.total_time_customers_waiting += 1

    def total_items_plus_one(self):
        self.total_items += 1
        
    #Special get method that calculates and returns average wait time 
    def get_avg_wait_time(self):
        self.avg_wait_time = self.total_time_customers_waiting / self.total_num_customers_served
        return self.avg_wait_time
    
    #Following are get methods to access Register object data for each instance
    def get_current_customer(self):
        return self.current_customer
    
    def get_size_customer_queue(self):
        return self.queue_of_customer.size()
    
    def get_customer_queue(self):
        return self.queue_of_customer.items
    
    def get_express(self):
        return self.is_express_lane
    
    def get_reg_name(self):
        return self.reg_name
    
    def get_items(self):
        return self.total_items
    
    def get_customers_served(self):
        return self.total_num_customers_served
    
    def get_idle_time(self):
        return self.total_idle_time
    
    def get_time_customers_waiting(self):
        return self.total_time_customers_waiting

#Total simulation test 
def simulation(num_registers_stand, items_for_express,
               rate_per_item, total_sec_for_simulation):
    
    #Tracks all registers made for simulation 
    list_of_registers = []

    #Create non express registers
    count = 0
    for reg in range(num_registers_stand):
        count += 1
        reg_name = "Register " + str(count)
        temp_name = Register(False, reg_name)
        list_of_registers.append(temp_name)
    
    #Create express register
    exp_reg = Register(True, "Express")
    list_of_registers.append(exp_reg)      
        
    #Loop through every second simulating simulation 
    for second in range(total_sec_for_simulation):
    
        #check if time to make new customer
        if ((second + 1) % 30) == 0:
            new_customer(list_of_registers, rate_per_item)
            
        #Check if time to print mini output
        if ((second + 1) % 50) == 0:
            sec50_output(list_of_registers, second)
        
        #Loop through each register we created 
        #to check if we need to add or remove customers
        #or add any simulated time or counts in the object methods
        for reg in list_of_registers:
            reg.check_if_empty()
            
            current_customer = reg.get_current_customer()
            
            if current_customer != None:
                if current_customer.get_time_for_items() % rate_per_item == 0:
                    reg.total_items_plus_one()
                    
                current_customer.subtract_second_from_checkout_time()
                
                if current_customer.get_time_to_checkout() == 0:
                    reg.remove_customer_from_queue()
                    
            if reg.get_size_customer_queue() != 0:
                queue_customers = reg.get_customer_queue()
                
                for customer in queue_customers:
                    reg.total_time_customers_waiting_plus_one()
    
    #After total simulation time is complete, calculate averages
    for reg in list_of_registers:
        reg.get_avg_wait_time()
        
    return list_of_registers

#Creates new customer and updates register chsoen with new customer
def new_customer(list_of_registers, rate_per_item):
    new_cust = Customer(rate_per_item)
    new_cust_reg = []
    
    #Chose express if empty and have less than 10 items
    #or choose register with least people
    #or choose random with least people
    if new_cust.get_less_than_10() == True:
        for reg in list_of_registers:
            if reg.get_express() == True and reg.check_if_empty() == True:
                reg.add_customer_to_queue(new_cust)
                return list_of_registers
        if not new_cust_reg:
            new_cust_reg = [reg for reg in list_of_registers if reg.get_current_customer() == None]
        if not new_cust_reg:
            smallest_queue = min(reg.get_size_customer_queue() for reg in list_of_registers)
            new_cust_reg = [reg for reg in list_of_registers if reg.get_size_customer_queue() <= smallest_queue]

    #Chose register with least people or choose random with least people
    else:
        standard_reg = [reg for reg in list_of_registers if reg.get_express() == False]
        new_cust_reg = [reg for reg in standard_reg if reg.get_current_customer() == None]
        if not new_cust_reg:
            smallest_queue = min(reg.get_size_customer_queue() for reg in standard_reg)
            new_cust_reg = [reg for reg in standard_reg if reg.get_size_customer_queue() <= smallest_queue]
   
    new_reg = rand.choice(new_cust_reg)
    
    for reg in list_of_registers:
        if new_reg == reg:
            reg.add_customer_to_queue(new_cust)

#Create mini output for every 50 seconds
def sec50_output(list_of_registers, second):
    print()
    print()
    print(str(second + 1) + " Second Update")
    print("------------------------")
    for reg in list_of_registers:
        prnt = ""
        prnt = prnt + reg.get_reg_name()
        if reg.get_reg_name() == "Express":
            prnt = prnt + "   "

        if reg.get_current_customer() != None:
            prnt = prnt + ":  " + str(reg.get_current_customer().get_items())
            if reg.get_current_customer().get_items() < 10:
                prnt = prnt + " "
        else:
            prnt = prnt + ":    "
            
        prnt = prnt + " | "
        
        if reg.get_size_customer_queue() > 0:
            for customer in reg.get_customer_queue():
                prnt = prnt + str(customer.get_items()) + "  "
                if customer.get_items() < 10:
                    prnt = prnt + " "
        
        print(prnt)

#Create final table output
def final_output(list_of_registers):
   data_2 = []
   for reg in list_of_registers:
       data = []
       a = reg.get_reg_name()
       data.append(a)
       z = reg.get_customers_served()
       data.append(z)
       y = reg.get_items()
       data.append(y)
       b = reg.get_idle_time()
       data.append(b)
       x = reg.get_avg_wait_time()
       data.append(x)
       data_2.append(data)
      
   headers = ['Register', 'total customers', 'total items',
              'total idle time (min)', 'average wait time (sec)']
  
   table = tab(data_2, headers, tablefmt="grid")
   
   print()
   print()
   print()
   print("FINAL VALUES")
   print()
   print(table)

#Control overall program
def main():
    items_for_express = 10
    rate_per_item = 4
    total_sec_for_simulation = 7200
    num_registers_stand = 4
    
    list_of_registers = simulation(num_registers_stand, items_for_express, 
                                   rate_per_item, total_sec_for_simulation)
    
    final_output(list_of_registers)
    
main()

