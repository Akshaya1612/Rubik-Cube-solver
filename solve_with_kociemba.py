from kociemba_solver import solve

# Read cube string that you generated earlier
with open("cube_string.txt", "r") as f:
    cube_string = f.read().strip()

print("\nCube String Loaded:")
print(cube_string)

# Call the solver (this returns a list of moves)
solution_moves = solve(cube_string)

print("\nSolution Moves:")
print(solution_moves)

# Save moves to file
with open("solution_steps.txt", "w") as f:
    for m in solution_moves:
        f.write(m + "\n")

print("\nSaved solution steps to solution_steps.txt")
