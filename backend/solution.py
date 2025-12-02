# backend/solution.py
import json
import os

# Load solutions from solutions.json
SOLUTIONS_PATH = os.path.join(os.path.dirname(__file__), "solutions.json")

with open(SOLUTIONS_PATH, "r") as f:
    SOLUTIONS = json.load(f)

def get_solution(disease_name: str) -> str:
    """
    Return solution text for a disease from solutions.json
    """
    return SOLUTIONS.get(disease_name, "No solution available for this disease yet.")
