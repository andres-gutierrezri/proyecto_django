document.addEventListener('DOMContentLoaded', function() {
    // Obtener referencia a la imagen del logo
    const logo = document.getElementById('logo');
    
    // Variables para el control de la rotación
    let rotation = 0;
    let rotationInterval;
    
    // Función para rotar la imagen
    function rotateLogo() {
        rotation += 2; // Velocidad de rotación
        logo.style.transform = `rotate(${rotation}deg)`;
    }
    
    // Evento cuando el mouse está sobre la imagen
    logo.addEventListener('mouseenter', function() {
        // Iniciar rotación continua
        rotationInterval = setInterval(rotateLogo, 20);
        
        // Añadir una transición suave
        logo.style.transition = 'transform 0.1s linear';
    });
    
    // Evento cuando el mouse sale de la imagen
    logo.addEventListener('mouseleave', function() {
        // Detener la rotación
        clearInterval(rotationInterval);
        
        // Restablecer la rotación a 0 grados con una transición suave
        rotation = 0;
        logo.style.transform = `rotate(${rotation}deg)`;
        logo.style.transition = 'transform 0.5s ease-out';
    });
});