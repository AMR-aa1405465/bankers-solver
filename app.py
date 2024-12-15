from typing import List
import numpy as np
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

class BankersAlgorithm:
    def __init__(self, all_res: List[int], needed: List[List[int]], allocation: List[List[int]], request: List[int], process_requesting: int):
        self.needed = np.array(needed)
        self.all_res = np.array(all_res)
        self.allocation = np.array(allocation)
        self.request = np.array(request)
        self.process_requesting = process_requesting
        self.available = self.calculate_available()

    def calculate_available(self):
        return self.all_res - self.allocation.sum(axis=0)

    def is_request_valid(self):
        if any(self.request > self.needed[self.process_requesting]):
            return False, "Test 1 Failed: Request > needed resources."
        if any(self.request > self.available):
            return False, "Test 2 Failed: Request > available resources."
        return True, "Request is valid."

    def check_safety(self):
        work = self.available.copy()
        finish = [False] * len(self.needed)
        safe_sequence = []
        execution_states = []  # To store the state after each execution

        while True:
            found = False
            for i in range(len(self.needed)):
                if not finish[i] and all(self.needed[i] <= work):
                    work += self.allocation[i]
                    safe_sequence.append(i)
                    execution_states.append(work.copy())  # Store the new available resources
                    finish[i] = True
                    found = True

            if not found:
                break

        if all(finish):
            # Create a message showing the available resources after each process
            execution_message = "Process execution sequence:<br>"
            for idx, process in enumerate(safe_sequence):
                execution_message += f"After executing P{process}: Available = {execution_states[idx]}<br>"
            return True, execution_message
        else:
            return False, "No safe sequence found"

    def process_request(self):
        valid, message = self.is_request_valid()
        if not valid:
            return False, message

        # Temporarily allocate resources to test safety
        self.available -= self.request
        self.allocation[self.process_requesting] += self.request
        self.needed[self.process_requesting] -= self.request

        safe, sequence = self.check_safety()

        if safe:
            return True, sequence  # Now returns the detailed execution message
        else:
            # Rollback allocation
            self.available += self.request
            self.allocation[self.process_requesting] -= self.request
            self.needed[self.process_requesting] += self.request
            return False, "System is not in a safe state after the request."

# Example usage function for integration
def solve_bankers(all_res: List[int], needed: List[List[int]], allocation: List[List[int]], request: List[int], process_requesting: int):
    banker = BankersAlgorithm(all_res, needed, allocation, request, process_requesting)
    result, message = banker.process_request()
    return {"result": result, "message": message}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/solve', methods=['POST'])
def solve():
    try:
        data = request.json
        all_res = data['all_res']
        needed = data['needed']
        allocation = data['allocation']
        request_resources = data['request']
        process_requesting = data['process_requesting']

        response = solve_bankers(all_res, needed, allocation, request_resources, process_requesting)
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
