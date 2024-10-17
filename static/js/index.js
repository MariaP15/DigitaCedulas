//Se obtienen todos los valores que se necesitan 
const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const captureButton = document.getElementById('captureButton');
const clearButton = document.getElementById('clearButton');
const cedulaCard = document.getElementById('cedulaCard');
const csrf = document.getElementById('csrf')
// Solicitar acceso a la cámara
navigator.mediaDevices.getUserMedia({ video: true })
    .then(function (stream) {
        video.srcObject = stream;
    })
    .catch(function (error) {
        console.error("Error al acceder a la cámara:", error);
    });

// Capturar la imagen cuando se hace clic en el botón "Capturar Imagen"
captureButton.addEventListener('click', function () {
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    const context = canvas.getContext('2d');
    context.drawImage(video, 0, 0, canvas.width, canvas.height);

    // Convertir la imagen a datos base64
    canvas.toBlob(function (blob) {
        const formData = new FormData();
        formData.append('image', blob);

        // Enviar la imagen al servidor
        fetch("/upload_images/", {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrf.value
            },
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            const datos = data.datos;
        // Si la solicitud es existosa me devuelve los datos obtenidos 
            const setTextContent = (elementId, value) => {
                const element = document.getElementById(elementId);
                if (value) {
                    element.innerText = value;
                }
            };
            //Se eliminan todos los caracteres especiales
            cedula =  removeSpecialCharacters(datos.cedula)
            nombre =  removeSpecialCharacters(datos.nombre)
            apelli1 =  removeSpecialCharacters(datos.apellido1)
            apelli2 =  removeSpecialCharacters(datos.apellido2)
            year =  removeSpecialCharacters(datos.fecha_nacimiento)
            place =  removeSpecialCharacters(datos.lugar_nacimiento)
            vote =  removeSpecialCharacters(datos.domicilio_electoral)
            dad =  removeSpecialCharacters(datos.nombre_padre)
            mom =  removeSpecialCharacters(datos.nombre_madre)
            vencimiento =  removeSpecialCharacters(datos.vencimiento)
            setTextContent('cedularesult', cedula);
            setTextContent('nameResult', nombre);
            setTextContent('lastnameResult', apelli1);
            setTextContent('lastname2Result', apelli2);
            setTextContent('yearResult', year);
            setTextContent('placeResult', place);
            setTextContent('voteResult', vote);
            setTextContent('dadResult', dad);
            setTextContent('momResult', mom);
            setTextContent('vencimientoResult', vencimiento);

            // Mostrar el card con los datos y ocultar la cámara y el botón de captura
            cedulaCard.style.display = 'block';
            captureButton.style.display = 'none';
            document.querySelector('.camera-box').style.display = 'none'; // Ocultar el contenedor de la cámara
            clearButton.style.display = 'block';
            video.style.display='none';
        })
        .catch(error => {
            console.error('Error al capturar la imagen:', error); // Mensaje de error en caso de que la imagen no se logre capturar correctamente
        });
    }, 'image/jpeg');
});

// Al hacer clic en el botón de limpiar, se recarga la página
clearButton.addEventListener('click', function () {
    location.reload();
});

function removeSpecialCharacters(input) {
return input.replace(/[^a-zA-Z0-9\s]/g, ''); // Elimina caracteres especiales, pero mantiene letras, números y espacios
}

