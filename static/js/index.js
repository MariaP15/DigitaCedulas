const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const captureButton1 = document.getElementById('captureButton1');
const captureButton2 = document.getElementById('captureButton2');
const clearButton = document.getElementById('clearButton');
const csrf = document.getElementById('csrf');
const card0 = document.getElementById('card0')
const card1 = document.getElementById('card1');

const cedulaCard = document.getElementById('cedulaCard')

// Solicitar acceso a la cámara
navigator.mediaDevices.getUserMedia({ video: true })
    .then(function (stream) {
        video.srcObject = stream;
    })
    .catch(function (error) {
        console.error("Error al acceder a la cámara:", error);
    });


    captureButton1.addEventListener('click', function () {
        // Configuración del canvas y captura de imagen
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        const context = canvas.getContext('2d', { willReadFrequently: true });
    
        // Captura la imagen completa del video
        context.drawImage(video, 0, 0, canvas.width, canvas.height);
    
        const imageData = context.getImageData(0, 0, canvas.width, canvas.height);
        const data = imageData.data;
    
        // Aplicar el kernel de sharpen
        const sharpenKernel = [
            0, -1,  0,
           -1,  5, -1,
            0, -1,  0
        ];
        applyConvolution(imageData, sharpenKernel, canvas.width, canvas.height);
    
        // Reasignar los datos de la imagen
        context.putImageData(imageData, 0, 0);
    
        // Convertir la imagen a datos base64 para el OCR
        const imageBase64 = canvas.toDataURL('image/jpeg');
    
        // Us Tesseract.js para digitalizar la imagen y extraer el texto
        Tesseract.recognize(imageBase64, 'eng', {
            logger: info => console.log(info) // Mostrar el progreso
        }).then(({ data: { text } }) => {
            console.log('Texto extraído:', text);
    
            // Filtrar solo números usando expresión regular
            const numberOnlyRegex = /\d+/g; // Solo números
            const numberMatch = text.match(numberOnlyRegex);
            
            document.getElementById('msj').style.display='block';
            if (numberMatch) {
                // Unir todos los números encontrados
                const numberSeries = numberMatch.join(''); // Todos los números válidos unidos
                console.log("Número detectado:", numberSeries);
                document.getElementById('cedulaText').textContent = numberSeries; // Mostrar el número de cédula
    
                canvas.toBlob(function (blob) {
                    const formData = new FormData();
                    formData.append('cedula', numberSeries); 
    
                    fetch("/tribunal/", {
                        method: 'POST',
                        headers: {
                            'X-CSRFToken': csrf.value
                        },
                        body: formData
                    })
                    .then(response => {
                        if (!response.ok) {
                            throw new Error('Error en la respuesta del servidor: ' + response.statusText);
                        }
                      

                        return response.json(); 

                        
                    })
                    .then(data => {
                        console.log('Datos procesados:', data);
                        document.getElementById('msj').style.display='flex';

    
                        // Asignar los datos recibidos del backend a los respectivos elementos HTML
                        document.getElementById('cedulaText').textContent = data.Cedula;
                        document.getElementById('nombreText').textContent = data.Nombre;
                        document.getElementById('apellido1Text').textContent = data.Apellido1;
                        document.getElementById('apellido2Text').textContent = data.Apellido2;
                        document.getElementById('fechaVencimientoText').textContent = data.Vencimiento;
                        document.getElementById('cantonText').textContent = data.Canton;
    
                        // Mostrar el card con los datos de la cédula
                        document.getElementById('msj').style.display='none';
                        document.getElementById('cedulaCard').style.display = 'block';
                    })
                    .catch(error => {
                        console.error('Error al procesar la imagen:', error);
                        document.getElementById('msj-error').style.display='flex';
                        document.getElementById('msj').style.display='none';
                    });
                }, 'image/jpeg');
                
            } else {
                document.getElementById('cedulaText').textContent = 'No se encontró un número válido.';
                document.getElementById('cedulaText').style.display = 'block';
                card0.style.display = "block"; // Mostrar el card0
                cedulaCard.style.display = 'block';
            }
    
            // Ocultar la cámara y los botones
            captureButton1.style.display = 'none';
            captureButton2.style.display = 'none';
            card1.style.display = 'none'; // Si deseas ocultar otros cards
            document.querySelector('.camera-box').style.display = 'none'; // Ocultar el contenedor de la cámara
            video.style.display = 'none'; // Ocultar el video
            clearButton.style.display = 'block'; // Mostrar el botón de limpiar
        }).catch(error => {
            console.error('Error al procesar la imagen con OCR:', error);
        });
    });
    
    
    
    
    




    // Boton de escaneo y digitalizacion de datos en la parte trasera

  captureButton2.addEventListener('click', function () {
    // Configuración del canvas y captura de imagen
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    const context = canvas.getContext('2d', { willReadFrequently: true });

    context.drawImage(video, 0, 0, canvas.width, canvas.height);

    // Convertir la imagen a escala de grises utilizando un método perceptual
    const imageData = context.getImageData(0, 0, canvas.width, canvas.height);
    const data = imageData.data;

    // Aplicar escala de grises utilizando luminancia
    for (let i = 0; i < data.length; i += 4) {
        const avg = 0.2126 * data[i] + 0.7152 * data[i + 1] + 0.0722 * data[i + 2]; // Luminancia
        data[i] = avg;     // Rojo
        data[i + 1] = avg; // Verde
        data[i + 2] = avg; // Azul
    }

    // Aplicar el kernel de sharpen
    const sharpenKernel = [
        0, -1,  0,
       -1,  5, -1,
        0, -1,  0
    ];
    applyConvolution(imageData, sharpenKernel, canvas.width, canvas.height);

    // Aplicar un desenfoque suave (opcional)
    applyGaussianBlur(imageData, canvas.width, canvas.height);

    // Reasignar los datos de la imagen
    context.putImageData(imageData, 0, 0);

    // Convertir a datos base64 y procesar con OCR
    canvas.toBlob(function (blob) {
        const formData = new FormData();
        formData.append('image', blob);
        formData.append('type', 'back');

        // Enviar la imagen al servidor
        fetch("/upload_images/", {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrf.value
            },
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Error en la respuesta del servidor: ' + response.statusText);
            }
            return response.json();
        })
        .then(data => {
            // Validar y procesar datos
            if (data.datos) {
                const datos = data.datos;
                const setTextContent = (elementId, value) => {
                    const element = document.getElementById(elementId);
                    if (value) {
                        element.innerText = value;
                    }
                };
                
                // Eliminar caracteres especiales
                cedula = removeSpecialCharacters(datos.cedula);
                year = removeSpecialCharacters(datos.fecha_nacimiento);
                place = removeSpecialCharacters(datos.lugar_nacimiento);
                vote = removeSpecialCharacters(datos.domicilio_electoral);
                dad = removeSpecialCharacters(datos.nombre_padre);
                mom = removeSpecialCharacters(datos.nombre_madre);
                vencimiento = removeSpecialCharacters(datos.vencimiento);
                setTextContent('cedularesult', cedula);
                setTextContent('yearResult', year);
                setTextContent('placeResult', place);
                setTextContent('voteResult', vote);
                setTextContent('dadResult', dad);
                setTextContent('momResult', mom);
                setTextContent('vencimientoResult', vencimiento);

                // Mostrar el card con los datos y ocultar la cámara y el botón de captura
                cedulaCard.style.display = 'block';
                captureButton1.style.display = 'none';
                captureButton2.style.display = 'none';
               
                card1.style.display = "block";
                card0.style.display = "none";
                document.querySelector('.camera-box').style.display = 'none';
                clearButton.style.display = 'block';
                video.style.display = 'none';
            } else {
                console.error('Datos no disponibles');
            }
        })
        .catch(error => {
            console.error('Error al procesar la imagen:', error);
        });
    }, 'image/jpeg');
});

// Función para aplicar el kernel de convolución
function applyConvolution(imageData, kernel, width, height) {
    const outputData = new Uint8ClampedArray(imageData.data.length);
    const side = Math.round(Math.sqrt(kernel.length));
    const halfSide = Math.floor(side / 2);

    // Copiar la imagen original para preservar los bordes
    for (let i = 0; i < imageData.data.length; i++) {
        outputData[i] = imageData.data[i];
    }

    // Aplicar la convolución
    for (let y = halfSide; y < height - halfSide; y++) {
        for (let x = halfSide; x < width - halfSide; x++) {
            let r = 0, g = 0, b = 0;

            // Aplicar el kernel en el vecindario de píxeles
            for (let ky = -halfSide; ky <= halfSide; ky++) {
                for (let kx = -halfSide; kx <= halfSide; kx++) {
                    const pixelIndex = ((y + ky) * width + (x + kx)) * 4;
                    const kernelValue = kernel[(ky + halfSide) * side + (kx + halfSide)];

                    r += imageData.data[pixelIndex] * kernelValue;
                    g += imageData.data[pixelIndex + 1] * kernelValue;
                    b += imageData.data[pixelIndex + 2] * kernelValue;
                }
            }

            // Set new RGB values after convolution
            const i = (y * width + x) * 4;
            outputData[i] = Math.min(Math.max(r, 0), 255);
            outputData[i + 1] = Math.min(Math.max(g, 0), 255);
            outputData[i + 2] = Math.min(Math.max(b, 0), 255);
            outputData[i + 3] = imageData.data[i + 3]; // Alpha channel
        }
    }

    // Reasignar los datos procesados a la imagen original
    for (let i = 0; i < outputData.length; i++) {
        imageData.data[i] = outputData[i];
    }
}

// Función para aplicar un desenfoque gaussiano (opcional)
function applyGaussianBlur(imageData, width, height) {
    const outputData = new Uint8ClampedArray(imageData.data.length);
    const kernelSize = 5; // Tamaño del kernel
    const sigma = 1.0; // Desviación estándar
    const kernel = createGaussianKernel(kernelSize, sigma);
    const halfSize = Math.floor(kernelSize / 2);

    for (let y = halfSize; y < height - halfSize; y++) {
        for (let x = halfSize; x < width - halfSize; x++) {
            let r = 0, g = 0, b = 0;

            for (let ky = -halfSize; ky <= halfSize; ky++) {
                for (let kx = -halfSize; kx <= halfSize; kx++) {
                    const pixelIndex = ((y + ky) * width + (x + kx)) * 4;
                    const kernelValue = kernel[(ky + halfSize) * kernelSize + (kx + halfSize)];

                    r += imageData.data[pixelIndex] * kernelValue;
                    g += imageData.data[pixelIndex + 1] * kernelValue;
                    b += imageData.data[pixelIndex + 2] * kernelValue;
                }
            }

            const i = (y * width + x) * 4;
            outputData[i] = Math.min(Math.max(r, 0), 255);
            outputData[i + 1] = Math.min(Math.max(g, 0), 255);
            outputData[i + 2] = Math.min(Math.max(b, 0), 255);
            outputData[i + 3] = imageData.data[i + 3]; // Alpha channel
        }
    }

    for (let i = 0; i < outputData.length; i++) {
        imageData.data[i] = outputData[i];
    }
}

// Crear un kernel gaussiano
function createGaussianKernel(size, sigma) {
    const kernel = new Array(size * size);
    const center = Math.floor(size / 2);
    let sum = 0;

    for (let y = -center; y <= center; y++) {
        for (let x = -center; x <= center; x++) {
            const value = Math.exp(-(x * x + y * y) / (2 * sigma * sigma)) / (2 * Math.PI * sigma * sigma);
            kernel[(y + center) * size + (x + center)] = value;
            sum += value;
        }
    }

    // Normalizar el kernel
    for (let i = 0; i < kernel.length; i++) {
        kernel[i] /= sum;
    }

    return kernel;
}



//Lector del codigo de barras

// captureButton3.addEventListener('click', function () {
   

//     // Convertir a datos base64 y procesar con OCR
   
//         const formData = new FormData();
//         formData.append('type', 'end')

//         // Enviar la imagen al servidor
//         fetch("/upload_images/", {
//             method: 'POST',
//             headers: {
//                 'X-CSRFToken': csrf.value
//             },
//             body: formData
//         })
//         .then(response => {
//             if (!response.ok) {
//                 throw new Error('Error en la respuesta del servidor: ' + response.statusText);
//             }
//             return response.json();
//         })
//         .then(data => {
//             // Validar y procesar datos
//             if (data) {
//                 const datos = data;
//                         // Si la solicitud es existosa me devuelve los datos obtenidos 
//                 const setTextContent = (elementId, value) => {
//                     const element = document.getElementById(elementId);
//                     if (value) {
//                         element.innerText = value;
//                     }
//                 };
//                 console.log(datos); // Verificar datos esperados
//                 //Se eliminan todos los caracteres especiales
//                 cedula =  datos.datos.id
//                 apellido1 = datos.datos.apellido1
//                 apellido2 =  datos.datos.apellido2
//                 nombre = datos.datos.nombre
//                 sexo =  datos.datos.sexo
//                 date =  datos.datos.fecha_nacimiento
//                 vencimiento =  datos.datos.fecha_vencimiento
//                 setTextContent('cedularesult1',cedula);
//                 setTextContent('lastnameResult1',apellido1);
//                 setTextContent('lastname2Result1',apellido2);
//                 setTextContent('nameResult1',nombre);
//                 setTextContent('sexoResult1', sexo)
//                 setTextContent('vencimientoResult1',vencimiento); 

//                 // Mostrar el card con los datos y ocultar la cámara y el botón de captura
//                 cedulaCard.style.display = 'block';
//                 card2.style.display = "block";
//                 card1.style.display = "none"
//                 card0.style.display = "none"
//                 captureButton1.style.display = 'none';
//                 captureButton2.style.display = 'none';
//                 captureButton3.style.display = 'none';
//                 document.querySelector('.camera-box').style.display = 'none'; // Ocultar el contenedor de la cámara
//                 clearButton.style.display = 'block';
//                 video.style.display='none';
//             } else {
//                 console.error('Datos no disponibles');
//             }
//         })
//         .catch(error => {
//             console.error('Error al procesar la imagen:', error);
//         });
//     }, 'image/jpeg');





function removeSpecialCharacters(input) {
    return input.replace(/[^a-zA-Z0-9\s]/g, ''); // Elimina caracteres especiales, pero mantiene letras, números y espacios
}

// Al hacer clic en el botón de limpiar, se recarga la página
clearButton.addEventListener('click', function () {
    location.reload();
});
