/**
 * Theme Loader Script
 *
 * Este script debe colocarse justo después del body tag para una ejecución rápida.
 * Carga la configuración de tema desde localStorage y la aplica al documento.
 *
 * Nota: El script está escrito en JavaScript puro y no depende de librerías de terceros.
 *
 * @author Proyecto Django
 * @version 1.0.1
 */
'use strict';

(function() {
    const classHolder = document.getElementsByTagName("BODY")[0];

    /**
     * Cargar desde localstorage
     **/
    let themeSettings = (localStorage.getItem('themeSettings')) ? JSON.parse(localStorage.getItem('themeSettings')) : {};
    const themeURL = themeSettings.themeURL || '';

    /**
     * Cargar opciones de tema
     **/
    if (themeSettings.themeOptions) {
        classHolder.className = themeSettings.themeOptions;
        console.log("%c✔ Configuración de tema cargada", "color: #148f32");
    } else {
        console.log("%c✔ Atención: La configuración de tema está vacía o no existe, cargando configuración por defecto...", "color: #ed1c24");
    }

    if (themeSettings.themeURL && !document.getElementById('mytheme')) {
        const cssfile = document.createElement('link');
        cssfile.id = 'mytheme';
        cssfile.rel = 'stylesheet';
        cssfile.href = themeURL;
        document.getElementsByTagName('head')[0].appendChild(cssfile);
    } else if (themeSettings.themeURL && document.getElementById('mytheme')) {
        document.getElementById('mytheme').href = themeSettings.themeURL;
    }

    /**
     * Guardar en localstorage
     **/
    window.saveSettings = function() {
        themeSettings.themeOptions = String(classHolder.className).split(/[^\w-]+/).filter(function(item) {
            return /^(nav|header|footer|mod|display)-/i.test(item);
        }).join(' ');
        if (document.getElementById('mytheme')) {
            themeSettings.themeURL = document.getElementById('mytheme').getAttribute("href");
        }
        localStorage.setItem('themeSettings', JSON.stringify(themeSettings));
    }

    /**
     * Resetear configuración
     **/
    window.resetSettings = function() {
        localStorage.setItem("themeSettings", "");
    }
})();
