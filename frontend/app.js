let scene, camera, renderer, controls;
let cubies = [];
let moves = [];
let moveIndex = 0;

const colorMap = {
    white: 0xffffff,
    yellow: 0xffff00,
    red: 0xff0000,
    orange: 0xff8000,
    blue: 0x0000ff,
    green: 0x00ff00
};

let cubeFaces = {};

// ---------------------------------------------------
// Load solver moves
// ---------------------------------------------------
fetch("solution_steps.txt")
    .then(res => res.text())
    .then(text => {
        let rawMoves = text.trim().split(/\s+/);

        // reverse + invert moves
        moves = rawMoves.reverse().map(m => {
            if (m.includes("2")) return m;        // F2, L2 stay same
            if (m.includes("'")) return m[0];     // R' -> R
            return m + "'";                       // R -> R'
        });

        document.getElementById("totalMoves").innerText = moves.length;
    });

// ---------------------------------------------------
// Load scanned cube colors
// ---------------------------------------------------
fetch("cube_faces.json")
    .then(res => res.json())
    .then(data => {
        cubeFaces = data;
        init();
    });

// ---------------------------------------------------

function init() {
    scene = new THREE.Scene();

    camera = new THREE.PerspectiveCamera(45, 1, 0.1, 1000);
    camera.position.set(5, 6, 8);

    renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(500, 500);
    document.getElementById("cubeContainer").appendChild(renderer.domElement);

    controls = new THREE.OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;

    scene.add(new THREE.AmbientLight(0xffffff, 1.3));

    buildCubies();
    // FIX: align cube orientation with solver
setTimeout(() => {
    rotateLayer("y", 1, true, () => {
        rotateLayer("y", 0, true, () => {
            rotateLayer("y", -1, true, () => {});
        });
    });
}, 500);

    animate();
}

// ---------------------------------------------------
// Build 27 cubies
// ---------------------------------------------------

function buildCubies() {
    const size = 0.9;
    const pos = [-1, 0, 1];

    pos.forEach(x => {
        pos.forEach(y => {
            pos.forEach(z => {
                const geometry = new THREE.BoxGeometry(size, size, size);
                const materials = createCubieMaterials(x, y, z);

                const cubie = new THREE.Mesh(geometry, materials);
                cubie.position.set(x, y, z);

                cubies.push(cubie);
                scene.add(cubie);
            });
        });
    });
}

// ---------------------------------------------------
// Apply scanned colors
// ---------------------------------------------------

function createCubieMaterials(x, y, z) {
    const black = new THREE.MeshBasicMaterial({ color: 0x000000 });

    const materials = [
        black, black, black, black, black, black
    ];

    // R face
    if (x === 1) {
        const idx = (1 - y) * 3 + (z + 1);
        materials[0] = new THREE.MeshBasicMaterial({
            color: colorMap[cubeFaces.R[idx]]
        });
    }

    // L face
    if (x === -1) {
        const idx = (1 - y) * 3 + (1 - z);
        materials[1] = new THREE.MeshBasicMaterial({
            color: colorMap[cubeFaces.L[idx]]
        });
    }

    // U face
    if (y === 1) {
        const idx = (1 - z) * 3 + (x + 1);
        materials[2] = new THREE.MeshBasicMaterial({
            color: colorMap[cubeFaces.U[idx]]
        });
    }

    // D face
    if (y === -1) {
        const idx = (z + 1) * 3 + (x + 1);
        materials[3] = new THREE.MeshBasicMaterial({
            color: colorMap[cubeFaces.D[idx]]
        });
    }

    // F face
    if (z === 1) {
        const idx = (1 - y) * 3 + (x + 1);
        materials[4] = new THREE.MeshBasicMaterial({
            color: colorMap[cubeFaces.F[idx]]
        });
    }

    // B face
    if (z === -1) {
        const idx = (1 - y) * 3 + (1 - x);
        materials[5] = new THREE.MeshBasicMaterial({
            color: colorMap[cubeFaces.B[idx]]
        });
    }

    return materials;
}

// ---------------------------------------------------
// SNAP FUNCTION (REMOVES GAPS)
// ---------------------------------------------------

function snapCubie(c) {
    c.position.x = Math.round(c.position.x);
    c.position.y = Math.round(c.position.y);
    c.position.z = Math.round(c.position.z);

    c.rotation.x = Math.round(c.rotation.x / (Math.PI / 2)) * (Math.PI / 2);
    c.rotation.y = Math.round(c.rotation.y / (Math.PI / 2)) * (Math.PI / 2);
    c.rotation.z = Math.round(c.rotation.z / (Math.PI / 2)) * (Math.PI / 2);
}

// ---------------------------------------------------
// ROTATE LAYER (STABLE & GAP-FREE)
// ---------------------------------------------------

function rotateLayer(axis, value, clockwise, callback) {
    const group = new THREE.Group();

    cubies.forEach(c => {
        if (Math.abs(c.position[axis] - value) < 0.1) {
            group.add(c);
        }
    });

    scene.add(group);

    let progress = 0;
    const speed = 0.1;
    const angle = clockwise ? -Math.PI / 2 : Math.PI / 2;

    function animateRotation() {
        if (progress < 1) {
            group.rotation[axis] = angle * progress;
            progress += speed;
            requestAnimationFrame(animateRotation);
        } else {
            group.rotation[axis] = angle;
            group.updateMatrixWorld();

            [...group.children].forEach(cubie => {
                cubie.applyMatrix4(group.matrixWorld);
                snapCubie(cubie);
                scene.add(cubie);
            });

            scene.remove(group);
            callback && callback();
        }
    }

    animateRotation();
}

// ---------------------------------------------------
// APPLY MOVE (R, R', R2 handled correctly)
// ---------------------------------------------------

function applyMove(move) {
    const prime = move.includes("'");
    const double = move.includes("2");
    const face = move[0];

    const times = double ? 2 : 1;
    let count = 0;

    function doRotate() {
        const cw = !prime;

        const done = () => {
            count++;
            if (count < times) doRotate();
            else {
                moveIndex++;
                document.getElementById("moveCounter").innerText = moveIndex;
                document.getElementById("currentMove").innerText = "Current Move: " + move;
            }
        };

        if (face === "R") rotateLayer("x", 1, cw, done);
        if (face === "L") rotateLayer("x", -1, cw, done);
        if (face === "U") rotateLayer("y", 1, cw, done);
        if (face === "D") rotateLayer("y", -1, cw, done);
        if (face === "F") rotateLayer("z", 1, cw, done);
        if (face === "B") rotateLayer("z", -1, cw, done);
    }

    doRotate();
}

// ---------------------------------------------------
// BUTTONS
// ---------------------------------------------------

document.getElementById("nextBtn").onclick = () => {
    if (moveIndex < moves.length) applyMove(moves[moveIndex]);
};

document.getElementById("autoBtn").onclick = () => {
    const auto = setInterval(() => {
        if (moveIndex >= moves.length) return clearInterval(auto);
        applyMove(moves[moveIndex]);
    }, 700);
};

document.getElementById("resetBtn").onclick = () => location.reload();

// ---------------------------------------------------

function animate() {
    requestAnimationFrame(animate);
    controls.update();
    renderer.render(scene, camera);
}
