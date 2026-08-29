/**
 * Session Timeout Handler
 * Manejo de tiempo de espera de sesión con advertencia al usuario
 *
 * Características:
 * - Detecta inactividad del usuario después de un tiempo configurado
 * - Muestra modal de advertencia antes de cerrar sesión
 * - Permite al usuario extender la sesión
 * - Cierra sesión automáticamente si no hay respuesta
 *
 * @author Proyecto Django
 * @version 1.0.0
 */
'use strict';

(function() {
    // Configuración de tiempos (en milisegundos)
    const config = {
        // Tiempo de inactividad antes de mostrar advertencia (28 minutos)
        warningTime: 28 * 60 * 1000,  // 28 minutos

        // Tiempo de la advertencia antes de cerrar sesión (2 minutos)
        logoutTime: 2 * 60 * 1000,     // 2 minutos

        // Total: 30 minutos de inactividad

        // URL de logout
        logoutUrl: '/logout/',

        // URL para mantener sesión viva
        keepAliveUrl: '/dashboard/',   // Cualquier URL autenticada
    };

    let warningTimer;
    let logoutTimer;
    let countdownInterval;
    let modal;
    let countdownElement;

    /**
     * Inicializa el sistema de timeout de sesión
     */
    function init() {
        console.log('🔒 Sistema de timeout de sesión inicializado');
        console.log('⏱️ Advertencia en:', config.warningTime / 60000, 'minutos');
        console.log('⏱️ Cierre de sesión en:', (config.warningTime + config.logoutTime) / 60000, 'minutos');

        createModal();
        resetTimer();
        setupEventListeners();
    }

    /**
     * Crea el modal de advertencia
     */
    function createModal() {
        const modalHTML = `
            <div class="modal fade" id="sessionTimeoutModal" tabindex="-1" role="dialog" aria-labelledby="sessionTimeoutModalLabel" aria-hidden="true" data-backdrop="static" data-keyboard="false">
                <div class="modal-dialog modal-dialog-centered" role="document">
                    <div class="modal-content">
                        <div class="modal-header bg-warning text-white">
                            <h5 class="modal-title" id="sessionTimeoutModalLabel">
                                <i class="fal fa-exclamation-triangle mr-2"></i>
                                Sesión por Expirar
                            </h5>
                        </div>
                        <div class="modal-body text-center">
                            <div class="mb-3">
                                <i class="fal fa-clock fs-xxxl text-warning"></i>
                            </div>
                            <p class="mb-3">
                                Tu sesión está a punto de expirar por inactividad.
                            </p>
                            <p class="mb-3">
                                <strong>Tiempo restante:</strong>
                                <span id="sessionCountdown" class="badge badge-warning fs-lg">2:00</span>
                            </p>
                            <p class="text-muted mb-0">
                                ¿Deseas continuar con la sesión activa?
                            </p>
                        </div>
                        <div class="modal-footer justify-content-center">
                            <button type="button" class="btn btn-success" id="extendSessionBtn">
                                <i class="fal fa-check mr-1"></i> Sí, continuar
                            </button>
                            <button type="button" class="btn btn-danger" id="logoutNowBtn">
                                <i class="fal fa-sign-out mr-1"></i> No, cerrar sesión
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        `;

        // Agregar modal al body si no existe
        if (!document.getElementById('sessionTimeoutModal')) {
            document.body.insertAdjacentHTML('beforeend', modalHTML);
            modal = $('#sessionTimeoutModal');
            countdownElement = document.getElementById('sessionCountdown');

            // Event listeners para los botones del modal
            document.getElementById('extendSessionBtn').addEventListener('click', extendSession);
            document.getElementById('logoutNowBtn').addEventListener('click', logoutNow);
        }
    }

    /**
     * Reinicia los timers de sesión
     */
    function resetTimer() {
        // Limpiar timers existentes
        clearTimeout(warningTimer);
        clearTimeout(logoutTimer);
        clearInterval(countdownInterval);

        // Cerrar modal si está abierto
        if (modal && modal.hasClass('show')) {
            modal.modal('hide');
        }

        // Configurar nuevo timer de advertencia
        warningTimer = setTimeout(showWarning, config.warningTime);

        console.log('⏱️ Timers reiniciados');
    }

    /**
     * Muestra la advertencia de timeout
     */
    function showWarning() {
        console.log('⚠️ Mostrando advertencia de sesión');

        // Mostrar modal
        modal.modal('show');

        // Iniciar contador regresivo
        startCountdown();

        // Configurar timer de logout automático
        logoutTimer = setTimeout(logoutNow, config.logoutTime);
    }

    /**
     * Inicia el contador regresivo en el modal
     */
    function startCountdown() {
        let timeLeft = config.logoutTime / 1000; // Convertir a segundos

        updateCountdownDisplay(timeLeft);

        countdownInterval = setInterval(() => {
            timeLeft--;
            updateCountdownDisplay(timeLeft);

            if (timeLeft <= 0) {
                clearInterval(countdownInterval);
            }
        }, 1000);
    }

    /**
     * Actualiza el display del contador regresivo
     */
    function updateCountdownDisplay(seconds) {
        const minutes = Math.floor(seconds / 60);
        const secs = seconds % 60;
        const display = `${minutes}:${secs < 10 ? '0' : ''}${secs}`;

        if (countdownElement) {
            countdownElement.textContent = display;

            // Cambiar color según el tiempo restante
            if (seconds <= 30) {
                countdownElement.className = 'badge badge-danger fs-lg';
            } else if (seconds <= 60) {
                countdownElement.className = 'badge badge-warning fs-lg';
            }
        }
    }

    /**
     * Extiende la sesión del usuario
     */
    function extendSession() {
        console.log('✅ Sesión extendida por el usuario');

        // Hacer una petición al servidor para mantener la sesión viva
        fetch(config.keepAliveUrl, {
            method: 'GET',
            credentials: 'same-origin',
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        }).then(response => {
            if (response.ok) {
                console.log('✅ Sesión renovada en el servidor');
                resetTimer();
            } else {
                console.error('❌ Error al renovar sesión');
                // Continuar de todas formas en el cliente
                resetTimer();
            }
        }).catch(error => {
            console.error('❌ Error de red:', error);
            // Continuar de todas formas en el cliente
            resetTimer();
        });
    }

    /**
     * Cierra la sesión del usuario
     */
    function logoutNow() {
        console.log('🚪 Cerrando sesión...');

        // Limpiar timers
        clearTimeout(warningTimer);
        clearTimeout(logoutTimer);
        clearInterval(countdownInterval);

        // Redirigir a logout
        window.location.href = config.logoutUrl;
    }

    /**
     * Configura los event listeners para detectar actividad del usuario
     */
    function setupEventListeners() {
        // Eventos que indican actividad del usuario
        const events = [
            'mousedown',
            'mousemove',
            'keypress',
            'scroll',
            'touchstart',
            'click'
        ];

        // Agregar listeners para cada evento
        events.forEach(event => {
            document.addEventListener(event, handleUserActivity, true);
        });

        console.log('👂 Event listeners configurados para detectar actividad');
    }

    /**
     * Maneja la actividad del usuario
     */
    function handleUserActivity() {
        // Solo resetear si el modal NO está visible
        // (para evitar resetear mientras se muestra la advertencia)
        if (!modal || !modal.hasClass('show')) {
            resetTimer();
        }
    }

    /**
     * Limpia todos los timers y event listeners
     */
    function cleanup() {
        clearTimeout(warningTimer);
        clearTimeout(logoutTimer);
        clearInterval(countdownInterval);
        console.log('🧹 Cleanup completado');
    }

    // Inicializar cuando el DOM esté listo
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

    // Cleanup al descargar la página
    window.addEventListener('beforeunload', cleanup);

    // Exponer funciones para debugging (solo en desarrollo)
    if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
        window.sessionTimeout = {
            reset: resetTimer,
            showWarning: showWarning,
            extendSession: extendSession,
            logout: logoutNow,
            config: config
        };
        console.log('🔧 Funciones de debugging disponibles en window.sessionTimeout');
    }

})();