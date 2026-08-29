/**
 * Script para el modal de eliminación de cuenta
 * Maneja la validación y confirmación para eliminar la cuenta del usuario
 */

document.addEventListener('DOMContentLoaded', function() {
    // Elementos del DOM
    const confirmCheckbox = document.getElementById('confirmDelete');
    const confirmButton = document.getElementById('confirmDeleteBtn');
    const deleteAccountForm = document.getElementById('deleteAccountForm');
    const deleteAccountModal = $('#deleteAccountModal');
    const passwordInput = document.getElementById('deletePassword');
    const errorAlert = document.getElementById('deleteAccountError');
    const errorMessage = document.getElementById('deleteAccountErrorMessage');

    // Verificar que los elementos existen
    if (!confirmCheckbox || !confirmButton || !deleteAccountForm) {
        console.warn('Elementos del modal de eliminación de cuenta no encontrados');
        return;
    }

    /**
     * Detectar si hay un mensaje de error de contraseña incorrecta al cargar la página
     * y reabrir el modal automáticamente
     */
    const checkPasswordError = function() {
        // Buscar mensajes de error en la página
        const alertMessages = document.querySelectorAll('.alert-danger, .alert-error');
        let hasPasswordError = false;

        alertMessages.forEach(function(alert) {
            if (alert.textContent.includes('Contraseña incorrecta') ||
                alert.textContent.includes('contraseña') && alert.textContent.includes('eliminar')) {
                hasPasswordError = true;

                // Copiar el mensaje al modal
                if (errorMessage && errorAlert) {
                    errorMessage.textContent = 'La contraseña ingresada es incorrecta. Por favor, verifica e intenta nuevamente.';
                    errorAlert.classList.remove('d-none');
                }

                // Marcar el input como inválido
                if (passwordInput) {
                    passwordInput.classList.add('is-invalid');
                }
            }
        });

        // Si hay error de contraseña, abrir el modal automáticamente
        if (hasPasswordError && deleteAccountModal.length) {
            setTimeout(function() {
                deleteAccountModal.modal('show');
                // Enfocar el campo de contraseña
                if (passwordInput) {
                    passwordInput.focus();
                    passwordInput.select();
                }
            }, 500);
        }
    };

    // Ejecutar al cargar la página
    checkPasswordError();

    /**
     * Habilitar/deshabilitar botón de eliminación basado en checkbox
     */
    confirmCheckbox.addEventListener('change', function() {
        confirmButton.disabled = !this.checked;
    });

    /**
     * Ocultar mensaje de error cuando el usuario empieza a escribir
     */
    if (passwordInput && errorAlert) {
        passwordInput.addEventListener('input', function() {
            errorAlert.classList.add('d-none');
            passwordInput.classList.remove('is-invalid');
        });
    }

    /**
     * Limpiar el formulario al cerrar el modal
     * Esto asegura que el usuario deba confirmar nuevamente si vuelve a abrir el modal
     */
    if (deleteAccountModal.length) {
        deleteAccountModal.on('hidden.bs.modal', function () {
            deleteAccountForm.reset();
            confirmButton.disabled = true;
            // Ocultar mensajes de error
            if (errorAlert) {
                errorAlert.classList.add('d-none');
            }
            if (passwordInput) {
                passwordInput.classList.remove('is-invalid');
            }
        });
    }

    /**
     * Validación adicional antes de enviar el formulario
     */
    deleteAccountForm.addEventListener('submit', function(event) {
        // Prevenir el envío por defecto
        event.preventDefault();

        const passwordInput = document.getElementById('deletePassword');

        // Validar que se haya ingresado una contraseña
        if (!passwordInput.value.trim()) {
            alert('Por favor, ingresa tu contraseña para confirmar la eliminación.');
            passwordInput.focus();
            return false;
        }

        // Validar que el checkbox esté marcado
        if (!confirmCheckbox.checked) {
            alert('Debes confirmar que entiendes que esta acción es irreversible.');
            confirmCheckbox.focus();
            return false;
        }

        // Cerrar el modal actual y abrir el modal de última advertencia
        deleteAccountModal.modal('hide');

        setTimeout(function() {
            $('#finalWarningModal').modal('show');
        }, 300);

        return false;
    });

    /**
     * Manejo del modal de última advertencia
     */
    const finalWarningModal = $('#finalWarningModal');
    const cancelFinalWarning = document.getElementById('cancelFinalWarning');
    const confirmFinalDeletion = document.getElementById('confirmFinalDeletion');

    // Botón "No, mantener mi cuenta" - volver al modal anterior
    if (cancelFinalWarning) {
        cancelFinalWarning.addEventListener('click', function() {
            finalWarningModal.modal('hide');
            setTimeout(function() {
                deleteAccountModal.modal('show');
            }, 300);
        });
    }

    // Botón "Sí, eliminar permanentemente" - enviar el formulario
    if (confirmFinalDeletion) {
        confirmFinalDeletion.addEventListener('click', function() {
            // Limpiar espacios en blanco de la contraseña antes de enviar
            const passwordInput = document.getElementById('deletePassword');
            if (passwordInput && passwordInput.value) {
                passwordInput.value = passwordInput.value.trim();
            }

            // Deshabilitar el botón para evitar clics duplicados
            this.disabled = true;
            this.innerHTML = '<i class="fal fa-spinner fa-spin"></i> Eliminando cuenta...';

            // Cambiar también el botón del modal original
            confirmButton.disabled = true;
            confirmButton.innerHTML = '<i class="fal fa-spinner fa-spin"></i> Eliminando...';

            // Enviar el formulario
            deleteAccountForm.submit();
        });
    }
});