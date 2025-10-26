/**
 * Theme Toggle Script
 *
 * Script para cambiar entre modo por defecto, claro y oscuro en las páginas de autenticación.
 * Proporciona un botón interactivo que cicla entre los tres temas y guarda la preferencia del usuario.
 *
 * Modos disponibles:
 * - Default: Sin clases de tema (usa los estilos por defecto de SmartAdmin)
 * - Light: Clase 'mod-skin-light' aplicada
 * - Dark: Clase 'mod-skin-dark' aplicada
 *
 * Requisitos:
 * - Elemento con id "theme-toggle" para el botón de cambio
 * - Elemento con id "theme-icon" para el icono del botón
 * - theme-loader.js debe estar cargado para la función saveSettings
 *
 * @author Proyecto Django
 * @version 1.1.0
 */
'use strict';

document.addEventListener('DOMContentLoaded', function() {
    const themeToggle = document.getElementById('theme-toggle');
    const themeIcon = document.getElementById('theme-icon');
    const body = document.getElementsByTagName('BODY')[0];

    // Verificar que los elementos existan
    if (!themeToggle || !themeIcon) {
        console.warn('⚠️ Elementos de cambio de tema no encontrados. Asegúrate de que existan elementos con id "theme-toggle" y "theme-icon".');
        return;
    }

    /**
     * Obtiene el tema actual
     * @returns {string} 'default', 'light' o 'dark'
     */
    function getCurrentTheme() {
        if (body.classList.contains('mod-skin-dark')) {
            return 'dark';
        } else if (body.classList.contains('mod-skin-light')) {
            return 'light';
        } else {
            return 'default';
        }
    }

    /**
     * Actualiza el icono según el tema actual
     */
    function updateThemeIcon() {
        const currentTheme = getCurrentTheme();

        switch(currentTheme) {
            case 'dark':
                themeIcon.className = 'fal fa-adjust';
                themeToggle.title = 'Cambiar a modo por defecto';
                console.log('%c🌙 Modo oscuro activo', 'color: #a8c7fa');
                break;
            case 'light':
                themeIcon.className = 'fal fa-moon';
                themeToggle.title = 'Cambiar a modo oscuro';
                console.log('%c☀️ Modo claro activo', 'color: #0d6efd');
                break;
            case 'default':
            default:
                themeIcon.className = 'fal fa-sun';
                themeToggle.title = 'Cambiar a modo claro';
                console.log('%c🎨 Modo por defecto activo', 'color: #39a900');
                break;
        }
    }

    /**
     * Cicla entre los tres modos de tema: default → light → dark → default
     */
    function toggleTheme() {
        const currentTheme = getCurrentTheme();

        // Remover todas las clases de tema
        body.classList.remove('mod-skin-dark', 'mod-skin-light');

        // Aplicar el siguiente tema en el ciclo
        switch(currentTheme) {
            case 'default':
                // Default → Light
                body.classList.add('mod-skin-light');
                break;
            case 'light':
                // Light → Dark
                body.classList.add('mod-skin-dark');
                break;
            case 'dark':
                // Dark → Default (sin clases)
                break;
        }

        // Actualizar icono
        updateThemeIcon();

        // Guardar configuración si la función existe
        if (typeof window.saveSettings === 'function') {
            window.saveSettings();
            console.log('%c✔ Preferencia de tema guardada', 'color: #198754');
        } else {
            console.warn('⚠️ Función saveSettings no disponible. La preferencia no se guardará.');
        }
    }

    // Inicializar icono según el tema actual
    updateThemeIcon();

    // Evento click para cambiar tema
    themeToggle.addEventListener('click', function(e) {
        e.preventDefault();
        toggleTheme();
    });

    // Atajo de teclado opcional (Ctrl/Cmd + K)
    document.addEventListener('keydown', function(e) {
        if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
            e.preventDefault();
            toggleTheme();
        }
    });

    console.log('%c🎨 Sistema de cambio de tema inicializado correctamente', 'color: #0dcaf0; font-weight: bold');
    console.log('%cAtajo de teclado: Ctrl/Cmd + K para cambiar tema', 'color: #6c757d; font-style: italic');
});
