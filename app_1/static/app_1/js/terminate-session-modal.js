/**
 * Terminate Session Modal Script
 * Maneja la confirmación mediante modal para cerrar sesiones individuales
 *
 * @author Proyecto Django
 * @version 1.0.0
 */
'use strict';

document.addEventListener('DOMContentLoaded', function() {
    console.log('✅ Script de terminación de sesión individual cargado');

    // Variables del modal
    let currentSessionKey = null;
    let currentForm = null;

    // Botones de terminar sesión
    const terminateButtons = document.querySelectorAll('.btn-terminate-session');
    
    // Modal elements
    const modalDeviceInfo = document.getElementById('modalDeviceInfo');
    const modalIpAddress = document.getElementById('modalIpAddress');
    const modalLastActivity = document.getElementById('modalLastActivity');
    const confirmButton = document.getElementById('confirmTerminateSession');
    
    if (terminateButtons.length > 0 && confirmButton) {
        // Agregar evento click a cada botón
        terminateButtons.forEach(button => {
            button.addEventListener('click', function(e) {
                e.preventDefault();
                
                // Obtener datos de la sesión
                currentSessionKey = this.getAttribute('data-session-key');
                const deviceInfo = this.getAttribute('data-device-info');
                const ipAddress = this.getAttribute('data-ip');
                const lastActivity = this.getAttribute('data-last-activity');
                
                // Guardar referencia al formulario
                currentForm = this.closest('form');
                
                // Actualizar información en el modal
                if (modalDeviceInfo) modalDeviceInfo.textContent = deviceInfo;
                if (modalIpAddress) modalIpAddress.textContent = ipAddress;
                if (modalLastActivity) modalLastActivity.textContent = lastActivity;
                
                console.log('🔒 Abriendo modal para cerrar sesión:', {
                    sessionKey: currentSessionKey,
                    device: deviceInfo,
                    ip: ipAddress
                });
                
                // Mostrar el modal
                $('#terminateSessionModal').modal('show');
            });
        });
        
        // Evento del botón de confirmación
        confirmButton.addEventListener('click', function() {
            console.log('✅ Usuario confirmó el cierre de sesión:', currentSessionKey);
            
            if (!currentForm) {
                console.error('❌ No se encontró el formulario');
                return;
            }
            
            // Deshabilitar el botón mientras se procesa
            this.disabled = true;
            this.innerHTML = '<i class="fal fa-spinner fa-spin"></i> Cerrando...';
            
            // Enviar el formulario usando fetch
            const formData = new FormData(currentForm);
            const actionUrl = currentForm.action;
            
            fetch(actionUrl, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                },
                credentials: 'same-origin'
            })
            .then(response => {
                if (response.ok) {
                    console.log('✅ Sesión cerrada exitosamente');
                    
                    // Cerrar el modal
                    $('#terminateSessionModal').modal('hide');
                    
                    // Mostrar mensaje de éxito y recargar
                    setTimeout(() => {
                        showSuccessMessage();
                    }, 300);
                } else {
                    console.error('❌ Error al cerrar la sesión');
                    throw new Error('Error al cerrar la sesión');
                }
            })
            .catch(error => {
                console.error('❌ Error:', error);
                
                // Cerrar el modal
                $('#terminateSessionModal').modal('hide');
                
                // Mostrar mensaje de error
                setTimeout(() => {
                    showErrorMessage();
                }, 300);
                
                // Re-habilitar el botón
                this.disabled = false;
                this.innerHTML = '<i class="fal fa-times-circle"></i> Sí, cerrar sesión';
            });
        });
    }
    
    // Función para mostrar mensaje de éxito
    function showSuccessMessage() {
        // Crear modal de éxito simple
        const successModalHTML = `
            <div class="modal fade" id="sessionClosedSuccessModal" tabindex="-1" role="dialog" data-backdrop="static">
                <div class="modal-dialog modal-dialog-centered" role="document">
                    <div class="modal-content">
                        <div class="modal-header bg-success text-white">
                            <h5 class="modal-title">
                                <i class="fal fa-check-circle"></i> Sesión Cerrada
                            </h5>
                        </div>
                        <div class="modal-body text-center">
                            <div class="mb-4">
                                <i class="fal fa-check-circle text-success" style="font-size: 5rem;"></i>
                            </div>
                            <h4 class="mb-3">¡Sesión cerrada exitosamente!</h4>
                            <p class="text-muted mb-0">
                                La página se recargará automáticamente en <strong id="reloadCountdownSingle">2</strong> segundos...
                            </p>
                        </div>
                        <div class="modal-footer justify-content-center">
                            <button type="button" class="btn btn-success" onclick="location.reload()">
                                <i class="fal fa-sync"></i> Recargar ahora
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        // Agregar modal al DOM
        if (!document.getElementById('sessionClosedSuccessModal')) {
            document.body.insertAdjacentHTML('beforeend', successModalHTML);
        }
        
        // Mostrar modal
        $('#sessionClosedSuccessModal').modal('show');
        
        // Countdown
        let seconds = 2;
        const countdownElement = document.getElementById('reloadCountdownSingle');
        
        const countdownInterval = setInterval(() => {
            seconds--;
            if (countdownElement) {
                countdownElement.textContent = seconds;
            }
            
            if (seconds <= 0) {
                clearInterval(countdownInterval);
                location.reload();
            }
        }, 1000);
        
        // Eliminar modal del DOM cuando se cierre
        $('#sessionClosedSuccessModal').on('hidden.bs.modal', function () {
            this.remove();
        });
    }
    
    // Función para mostrar mensaje de error
    function showErrorMessage() {
        const errorModalHTML = `
            <div class="modal fade" id="sessionErrorModal" tabindex="-1" role="dialog" data-backdrop="static">
                <div class="modal-dialog modal-dialog-centered" role="document">
                    <div class="modal-content">
                        <div class="modal-header bg-danger text-white">
                            <h5 class="modal-title">
                                <i class="fal fa-exclamation-circle"></i> Error
                            </h5>
                        </div>
                        <div class="modal-body text-center">
                            <div class="mb-4">
                                <i class="fal fa-exclamation-triangle text-danger" style="font-size: 5rem;"></i>
                            </div>
                            <h4 class="mb-3">Hubo un problema</h4>
                            <p class="mb-0">
                                No se pudo cerrar la sesión. Por favor, intenta de nuevo o recarga la página.
                            </p>
                        </div>
                        <div class="modal-footer justify-content-center">
                            <button type="button" class="btn btn-secondary" data-dismiss="modal">
                                <i class="fal fa-times"></i> Cerrar
                            </button>
                            <button type="button" class="btn btn-danger" onclick="location.reload()">
                                <i class="fal fa-sync"></i> Recargar página
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        // Agregar modal al DOM
        if (!document.getElementById('sessionErrorModal')) {
            document.body.insertAdjacentHTML('beforeend', errorModalHTML);
        }
        
        // Mostrar modal
        $('#sessionErrorModal').modal('show');
        
        // Eliminar modal del DOM cuando se cierre
        $('#sessionErrorModal').on('hidden.bs.modal', function () {
            this.remove();
        });
    }
    
    // Limpiar estado cuando se cierra el modal
    $('#terminateSessionModal').on('hidden.bs.modal', function () {
        currentSessionKey = null;
        currentForm = null;
        
        // Restaurar el botón de confirmación
        const confirmBtn = document.getElementById('confirmTerminateSession');
        if (confirmBtn) {
            confirmBtn.disabled = false;
            confirmBtn.innerHTML = '<i class="fal fa-times-circle"></i> Sí, cerrar sesión';
        }
    });
    
    // Log cuando se abre el modal
    $('#terminateSessionModal').on('shown.bs.modal', function () {
        console.log('📋 Modal de terminación de sesión abierto');
    });
});
