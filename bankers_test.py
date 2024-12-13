import numpy as np
import pandas as pd

class BankersAlgorithm:
    def __init__(self,all, needed, allocation, request, process_requesting):
        self.needed = needed
        self.all_res = all
        self.allocation = allocation
        # self.max = max
        self.request = request
        self.process_requesting = process_requesting
        self.available = self.calculate_available()
        self.print_resource_info()
        print("*"*100)
    
    def print_resource_info(self):
        print("allocation:\n",self.allocation,"\n")
        print("all_res:\n",self.all_res,"\n")
        print("needed:\n",self.needed,"\n")
        print("available:\n",self.available,"\n")
    def calculate_available(self):
        return self.all_res - self.allocation.sum()
         
    def is_safe(self):
        test_1 = self.solve_test_1()
        if not test_1:
            return "Invalid request... request > needed"
        test_2 = self.solve_test_2()

        if not test_2:
            return "Invalid request... request > available"
        
        test_3, execution_sequence = self.solve_test_3()
        if not test_3:
            return "no execution sequence"
        print("safe sequence: ", execution_sequence)
        # return True 
    
    def solve_test_1(self):
        print("test1 in progress")
        needed_for_process = self.needed.loc[self.process_requesting]
        print(f"is {self.request} <= {needed_for_process.values}?")
        if (needed_for_process.values >= self.request).all():
            print("test1 passed")
            print("👍")
            return True
        else:
            print("test1 failed: Terminate process")
            print("👎")
            return False
        
    def solve_test_2(self):
        print("test2 in progress")
        print(f"is {self.request} <= {self.available.values}?")
        if (self.request <= self.available.values).all():
            print("test2 passed")
            return True
        else:
            print("test2 failed: process must wait")
            return False
    
    def solve_test_3(self):
        currently_finished_processes = []
        max_number_of_processes = len(self.needed.index)
        print(f"1. Updating the allocation of {self.process_requesting}")
        self.allocation.loc[self.process_requesting] += self.request
        print(f"2. Updating the needed of {self.process_requesting}")
        self.needed.loc[self.process_requesting] -= self.request
        print(f"3. Updating the available vector")
        self.available -= self.request
        print("New Tables:")
        self.print_resource_info()
        max_trials_without_success = 10
        trials = 0
        counter = 0
        success=False
        while True:
            for process in self.needed.index:
                if process not in currently_finished_processes:
                    if (self.needed.loc[process] <= self.available.values).all():
                        currently_finished_processes.append(process)
                        self.available += self.allocation.loc[process]
                        counter+=1
                        print(f"process {process} finished")
                        if counter == max_number_of_processes:
                            success = True
                            break
            trials+=1
            if trials == max_trials_without_success:
                return False,[]
            if success:
                return True,currently_finished_processes
       
if __name__ == "__main__":
    # Using Pandas DataFrames for even better readability
    all = [7,6,4,8]
    needed = pd.DataFrame({
        'A': [0,0,2,0,2],
        'B': [2,1,4,1,0],
        'C': [1,0,0,2,2],
        'D': [2,1,2,0,2]
    }, index=['p0', 'p1', 'p2', 'p3', 'p4'])
    
    allocation = pd.DataFrame({
        'A': [2,0,1,1,1],
        'B': [0,1,0,2,0],
        'C': [1,2,0,1,0],
        'D': [1,1,1,0,1]
    }, index=['p0', 'p1', 'p2', 'p3', 'p4'])
   
    request = [0,1,0,1]
    process_requesting = "p0"
    bankers = BankersAlgorithm(all,needed, allocation, request, process_requesting)
    bankers.is_safe()
