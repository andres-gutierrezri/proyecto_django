/**
 * Close All Sessions Modal Script
 * Maneja la funcionalidad del modal para cerrar todas las sesiones
 * excepto la sesión actual del usuario
 *
 * @author Proyecto Django
 * @version 1.0.0
 */
'use strict';

document.addEventListener('DOMContentLoaded', function() {
    console.log('✅ Script de cierre de sesiones cargado');

    const confirmButton = document.getElementById('confirmCloseAllSessions');
    
    if (confirmButton) {
        confirmButton.addEventListener('click', function() {
            console.log('🔒 Cerrando todas las demás sesiones...');
            
            // Deshabilitar el botón para evitar múltiples clicks
            confirmButton.disabled = true;
            confirmButton.innerHTML = '<i class="fal fa-spinner fa-spin"></i> Cerrando sesiones...';
            
            // Obtener todas las sesiones que no son la actual
            const sessionForms = document.querySelectorAll('form[action*="terminate-session"]');
            let sessionsToClose = [];
            
            sessionForms.forEach(form => {
                const sessionKey = form.action.split('/terminate-session/')[1].replace('/', '');
                sessionsToClose.push(sessionKey);
            });
            
            if (sessionsToClose.length === 0) {
                console.log('⚠️ No hay sesiones adicionales para cerrar');
                $('#closeAllSessionsModal').modal('hide');
                return;
            }
            
            console.log(`📋 Cerrando ${sessionsToClose.length} sesión(es)...`);
            
            // Función para cerrar una sesión
            function closeSession(sessionKey, index) {
                return fetch(`/terminate-session/${sessionKey}/`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': getCsrfToken(),
                        'Content-Type': 'application/x-www-form-urlencoded',
                    },
                    credentials: 'same-origin'
                })
                .then(response => {
                    if (response.ok) {
                        console.log(`✅ Sesión ${index + 1}/${sessionsToClose.length} cerrada`);
                        return true;
                    } else {
                        console.error(`❌ Error al cerrar sesión ${index + 1}`);
                        return false;
                    }
                })
                .catch(error => {
                    console.error(`❌ Error de red al cerrar sesión ${index + 1}:`, error);
                    return false;
                });
            }
            
            // Cerrar todas las sesiones secuencialmente
            let promises = sessionsToClose.map((sessionKey, index) => closeSession(sessionKey, index));
            
            Promise.all(promises)
                .then(results => {
                    const successCount = results.filter(r => r === true).length;
                    console.log(`✅ ${successCount} de ${sessionsToClose.length} sesiones cerradas exitosamente`);
                    
                    // Cerrar el modal de confirmación
                    $('#closeAllSessionsModal').modal('hide');
                    
                    // Mostrar modal de éxito
                    setTimeout(() => {
                        showSuccessModal(successCount);
                    }, 300);
                })
                .catch(error => {
                    console.error('❌ Error al cerrar sesiones:', error);
                    
                    // Cerrar modal de confirmación
                    $('#closeAllSessionsModal').modal('hide');
                    
                    // Mostrar modal de error
                    setTimeout(() => {
                        showErrorModal();
                    }, 300);
                    
                    // Re-habilitar el botón
                    confirmButton.disabled = false;
                    confirmButton.innerHTML = '<i class="fal fa-sign-out-alt"></i> Sí, cerrar todas las demás sesiones';
                });
        });
    }
    
    // Función para mostrar modal de éxito
    function showSuccessModal(count) {
        // Actualizar el contador
        document.getElementById('closedSessionsCount').textContent = count;
        
        // Mostrar el modal
        $('#sessionsClosedSuccessModal').modal('show');
        
        // Iniciar countdown
        let seconds = 3;
        const countdownElement = document.getElementById('reloadCountdown');
        
        const countdownInterval = setInterval(() => {
            seconds--;
            countdownElement.textContent = seconds;
            
            if (seconds <= 0) {
                clearInterval(countdownInterval);
                location.reload();
            }
        }, 1000);
        
        // Botón de recargar ahora
        document.getElementById('reloadNowBtn').addEventListener('click', function() {
            clearInterval(countdownInterval);
            location.reload();
        });
    }
    
    // Función para mostrar modal de error
    function showErrorModal() {
        // Crear modal de error dinámicamente
        const errorModalHTML = `
            <div class="modal fade" id="sessionsErrorModal" tabindex="-1" role="dialog" data-backdrop="static">
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
                                No se pudieron cerrar algunas sesiones. Por favor, intenta de nuevo o cierra las sesiones individualmente.
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
        
        // Agregar modal al DOM si no existe
        if (!document.getElementById('sessionsErrorModal')) {
            document.body.insertAdjacentHTML('beforeend', errorModalHTML);
        }
        
        // Mostrar modal
        $('#sessionsErrorModal').modal('show');
        
        // Eliminar modal del DOM cuando se cierre
        $('#sessionsErrorModal').on('hidden.bs.modal', function () {
            this.remove();
        });
    }
    
    // Función auxiliar para obtener el token CSRF
    function getCsrfToken() {
        const cookieValue = document.cookie
            .split('; ')
            .find(row => row.startsWith('csrftoken='))
            ?.split('=')[1];
        
        if (!cookieValue) {
            // Intentar obtener del input hidden en los formularios
            const csrfInput = document.querySelector('input[name="csrfmiddlewaretoken"]');
            return csrfInput ? csrfInput.value : '';
        }
        
        return cookieValue;
    }
    
    // Limpiar el estado del botón cuando se cierra el modal
    $('#closeAllSessionsModal').on('hidden.bs.modal', function () {
        if (confirmButton) {
            confirmButton.disabled = false;
            confirmButton.innerHTML = '<i class="fal fa-sign-out-alt"></i> Sí, cerrar todas las demás sesiones';
        }
    });
    
    // Log cuando se abre el modal
    $('#closeAllSessionsModal').on('shown.bs.modal', function () {
        console.log('📋 Modal de cierre de sesiones abierto');
    });
});
