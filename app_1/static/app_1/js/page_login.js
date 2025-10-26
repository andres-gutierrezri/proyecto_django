/**
 * Script para la página de login
 *
 * Este script maneja:
 * - Configuración de tema desde localStorage
 * - Validación del formulario de login
 */

'use strict';

/**
 * Configuración de tema y preferencias
 * Este script se ejecuta inmediatamente para cargar el tema antes del render
 */
(function initializeThemeSettings() {
    let classHolder = document.getElementsByTagName("BODY")[0];

    /**
     * Cargar desde localStorage
     */
    let themeSettings = (localStorage.getItem('themeSettings')) ? JSON.parse(localStorage.getItem('themeSettings')) : {};
    let themeURL = themeSettings.themeURL || '';
    let themeOptions = themeSettings.themeOptions || '';

    /**
     * Cargar opciones de tema
     */
    if (themeSettings.themeOptions) {
        classHolder.className = themeSettings.themeOptions;
        console.log("%c✔ Theme settings loaded", "color: #148f32");
    } else {
        console.log("%c✔ Heads up! Theme settings is empty or does not exist, loading default settings...", "color: #ed1c24");
    }

    if (themeSettings.themeURL && !document.getElementById('mytheme')) {
        let cssfile = document.createElement('link');
        cssfile.id = 'mytheme';
        cssfile.rel = 'stylesheet';
        cssfile.href = themeURL;
        document.getElementsByTagName('head')[0].appendChild(cssfile);
    } else if (themeSettings.themeURL && document.getElementById('mytheme')) {
        document.getElementById('mytheme').href = themeSettings.themeURL;
    }

    /**
     * Guardar configuración en localStorage
     */
    window.saveSettings = function() {
        themeSettings.themeOptions = String(classHolder.className).split(/[^\w-]+/).filter(function(item) {
            return /^(nav|header|footer|mod|display)-/i.test(item);
        }).join(' ');

        if (document.getElementById('mytheme')) {
            themeSettings.themeURL = document.getElementById('mytheme').getAttribute("href");
        }

        localStorage.setItem('themeSettings', JSON.stringify(themeSettings));
    };

    /**
     * Resetear configuración
     */
    window.resetSettings = function() {
        localStorage.setItem("themeSettings", "");
    };
})();

/**
 * Validación del formulario de login
 * Se ejecuta cuando el DOM está completamente cargado
 */
document.addEventListener('DOMContentLoaded', function() {
    const loginBtn = document.getElementById("js-login-btn");

    if (loginBtn) {
        loginBtn.addEventListener("click", function(event) {
            // Obtener el formulario para aplicar validación de Bootstrap
            let form = document.getElementById("js-login");

            if (form && form.checkValidity() === false) {
                event.preventDefault();
                event.stopPropagation();
            }

            if (form) {
                form.classList.add('was-validated');
            }

            // Aquí se puede realizar el submit AJAX...
        });
    }
});
