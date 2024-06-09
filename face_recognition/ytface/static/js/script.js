const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const context = canvas.getContext('2d');

navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => {
        video.srcObject = stream;
    })
    .catch(error => {
        console.error("Error accessing the camera: ", error);
    });

function capture() {
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    const dataUrl = canvas.toDataURL('image/jpeg');
    return dataUrl;
}

function register() {
    const name = document.getElementById('name').value;
    const photo = capture();

    fetch('/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            name: name,
            photo: photo
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.message === "Registro exitoso") {
            alert('Registro exitoso');
        } else {
            alert('Error en el registro');
        }
    })
    .catch(error => {
        console.error("Error:", error);
    });
}

function login() {
    const photo = capture();

    fetch('/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            photo: photo
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            window.location.href = `/success?user_name=${data.name}`;
        } else {
            alert('No se encontró ninguna coincidencia');
        }
    })
    .catch(error => {
        console.error("Error:", error);
    });
}
