import json

# mapping colors → letters (solver format)
COLOR_TO_LETTER = {
    "white": "U",    # Up
    "yellow": "D",   # Down
    "red": "R",      # Right
    "orange": "L",   # Left
    "green": "F",    # Front
    "blue": "B"      # Back
}

# Order required by solver: U, R, F, D, L, B
FACE_ORDER = ["U", "R", "F", "D", "L", "B"]

with open("cube_faces.json", "r") as f:
    cube_faces = json.load(f)

cube_string = ""

for face in FACE_ORDER:
    colors = cube_faces[face]
    for c in colors:
        cube_string += COLOR_TO_LETTER[c]

print("\nFinal cube string for solver:")
print(cube_string)

# Save to file
with open("cube_string.txt", "w") as f:
    f.write(cube_string)

print("\nSaved as cube_string.txt")
