// Función para establecer el tema basado en las preferencias del usuario
function setThemeBasedOnPreference() {
    const prefersDarkScheme = window.matchMedia("(prefers-color-scheme: dark)").matches;
    document.body.setAttribute('data-bs-theme', prefersDarkScheme ? 'dark' : 'light');
}

// Ejecutar la función al cargar la página
setThemeBasedOnPreference();

// Escuchar cambios en las preferencias del sistema operativo
window.matchMedia("(prefers-color-scheme: dark)").addEventListener('change', event => {
    setThemeBasedOnPreference();
});
