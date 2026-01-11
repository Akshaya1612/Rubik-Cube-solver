import pycuber as pc
from pycuber.solver import CFOPSolver
import random

# Create a cube
cube = pc.Cube()

# Generate a random scramble manually
moves = ["U", "U'", "R", "R'", "L", "L'", "D", "D'", "F", "F'", "B", "B'"]
scramble = [random.choice(moves) for _ in range(20)]

print("Scramble moves:")
print(" ".join(scramble))

# Apply scramble
for move in scramble:
    cube(move)

print("\nScrambled Cube:")
print(cube)

# Solve using CFOP
solver = CFOPSolver(cube)
solution = solver.solve()

print("\nSolution Moves:")
print(solution)
