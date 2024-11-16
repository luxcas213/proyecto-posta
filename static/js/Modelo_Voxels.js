let isMouseDown = false;
cargarprefabSTL();
document.body.onmousedown = function () {
    isMouseDown = true;
};

document.body.onmouseup = function () {
    isMouseDown = false;
};


function crearMatrices() {
    const size = parseInt(document.getElementById("size").value);
    if(size>30){
        alert("tamaño muy grande")
        return;
        }
    if (isNaN(size) || size <= 0) {
        alert("Por favor, ingresa un tamaño válido para la matriz.");
        return;
    }
    generarMatriz('matriz1', size);
    generarMatriz('matriz2', size);
    generarMatriz('matriz3', size);
    verificarTamaños(); // Llama a la función para verificar tamaños
}

function verificarTamaños() {
    const contenedorMatrices = document.querySelector('.contenedor-matrices');
    const matriz1 = document.getElementById('matriz1');
    const matriz2 = document.getElementById('matriz2');
    const matriz3 = document.getElementById('matriz3');

    // Verificar las alturas de las matrices
    const alturas = [
        matriz1.offsetHeight,
        matriz2.offsetHeight,
        matriz3.offsetHeight,
    ];

    // Cambiar el estilo según la altura
    if (alturas.some(altura => altura > 230)) {
        contenedorMatrices.style.flexDirection = 'column';
    } else {
        contenedorMatrices.style.flexDirection = 'row'; // Vuelve al estilo original si es necesario
    }
}
function descargarSTL() {
    fetch('/static/output.stl')
        .then(response => {
            if (!response.ok) throw new Error("Error al descargar el STL");
            return response.blob();
        })
        .then(blob => {
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'output.stl';
            document.body.appendChild(a);
            a.click();
            a.remove();
            URL.revokeObjectURL(url);
        })
        .catch(error => console.error('Error al descargar el STL:', error));
}

function generarMatriz(matrizId, size) {
    
    
    const matrizDiv = document.getElementById(matrizId);
    matrizDiv.innerHTML = '';

    for (let i = 0; i < size; i++) {
        const fila = document.createElement('div');
        fila.classList.add('fila');

        for (let j = 0; j < size; j++) {
            const cuadro = document.createElement('div');
            cuadro.classList.add('cuadro');
            cuadro.dataset.checked = 'true';

            cuadro.addEventListener('mousedown', function () {
                toggleCuadro(cuadro);
            });

            cuadro.addEventListener('mouseover', function () {
                if (isMouseDown) {
                    toggleCuadro(cuadro);
                }
            });

            fila.appendChild(cuadro);
        }
        matrizDiv.appendChild(fila);
    }
}

function toggleCuadro(cuadro) {
    if (cuadro.dataset.checked === 'true') {
        cuadro.dataset.checked = 'false';
        cuadro.classList.add('checked');
    } else {
        cuadro.dataset.checked = 'true';
        cuadro.classList.remove('checked');
    }
}

function enviarDatos() {
    const size = document.getElementById("size").value;
    const matriz1 = obtenerMatriz('matriz1', size);
    const matriz2 = obtenerMatriz('matriz2', size);
    const matriz3 = obtenerMatriz('matriz3', size);

    fetch('/procesar', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            size: size,
            matriz1: matriz1,
            matriz2: matriz2,
            matriz3: matriz3
        })
    })
    .then(response => response.json())
    .then(data => {
        cargarSTL();
    })
    .catch(error => console.error('Error:', error));
}

function obtenerMatriz(matrizId, size) {
    const matriz = [];
    const filas = document.querySelectorAll(`#${matrizId} .fila`);
    filas.forEach(fila => {
        const filaMatriz = [];
        fila.querySelectorAll('.cuadro').forEach(cuadro => {
            filaMatriz.push(cuadro.dataset.checked === 'true');
        });
        matriz.push(filaMatriz);
    });
    return matriz;
}

function cargarSTL() {
    const viewer = document.getElementById('viewer');
    viewer.innerHTML = '';

    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, viewer.clientWidth / viewer.clientHeight, 0.1, 1000);
    camera.position.set(10,10,10);
    const renderer = new THREE.WebGLRenderer();
    renderer.setSize(viewer.clientWidth, viewer.clientHeight);
    viewer.appendChild(renderer.domElement);

    const light = new THREE.DirectionalLight(0xffffff, 1);
    light.position.set(1, 1, 1).normalize();
    scene.add(light);

    const loader = new THREE.STLLoader();
    loader.load('/static/output.stl', function (geometry) {
        const material = new THREE.MeshNormalMaterial();
        const mesh = new THREE.Mesh(geometry, material);
        scene.add(mesh);
        const controls = new THREE.OrbitControls(camera, renderer.domElement);
        controls.enableZoom = true;

        function animate() {
            requestAnimationFrame(animate);
            renderer.render(scene, camera);
        }
        animate();
    });
}
function cargarprefabSTL() {
    const viewer = document.getElementById('viewer');
    viewer.innerHTML = '';

    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, viewer.clientWidth / viewer.clientHeight, 0.1, 1000);
    camera.position.set(10,10,10)
    const renderer = new THREE.WebGLRenderer();
    renderer.setSize(viewer.clientWidth, viewer.clientHeight);
    viewer.appendChild(renderer.domElement);

    const light = new THREE.DirectionalLight(0xffffff, 1);
    light.position.set(1, 1, 1).normalize();
    scene.add(light);

    const loader = new THREE.STLLoader();
    loader.load('/static/prefab.stl', function (geometry) {
        const material = new THREE.MeshNormalMaterial();
        const mesh = new THREE.Mesh(geometry, material);
        scene.add(mesh);


        const controls = new THREE.OrbitControls(camera, renderer.domElement);
        controls.enableZoom = true;

        function animate() {
            requestAnimationFrame(animate);
            renderer.render(scene, camera);
        }
        animate();
    });
}
