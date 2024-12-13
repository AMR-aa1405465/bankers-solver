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

        while True:
            found = False
            for i in range(len(self.needed)):
                if not finish[i] and all(self.needed[i] <= work):
                    work += self.allocation[i]
                    safe_sequence.append(i)
                    finish[i] = True
                    found = True

            if not found:
                break

        if all(finish):
            return True, safe_sequence
        else:
            return False, []

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
            return True, f"System is in a safe state. Safe sequence: {sequence}"
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
