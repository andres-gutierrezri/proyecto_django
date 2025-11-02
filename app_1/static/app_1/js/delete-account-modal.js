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
        const passwordInput = document.getElementById('deletePassword');

        // Validar que se haya ingresado una contraseña
        if (!passwordInput.value.trim()) {
            event.preventDefault();
            alert('Por favor, ingresa tu contraseña para confirmar la eliminación.');
            passwordInput.focus();
            return false;
        }

        // Validar que el checkbox esté marcado
        if (!confirmCheckbox.checked) {
            event.preventDefault();
            alert('Debes confirmar que entiendes que esta acción es irreversible.');
            confirmCheckbox.focus();
            return false;
        }

        // Confirmación final
        const userConfirmed = confirm(
            '⚠️ ÚLTIMA ADVERTENCIA ⚠️\n\n' +
            'Esta acción es PERMANENTE e IRREVERSIBLE.\n\n' +
            'Se eliminarán:\n' +
            '• Todos tus datos personales\n' +
            '• Todas tus sesiones activas\n' +
            '• Tu acceso a todos los servicios\n\n' +
            '¿Estás absolutamente seguro de que deseas continuar?'
        );

        if (!userConfirmed) {
            event.preventDefault();
            return false;
        }

        // Si llegamos aquí, el usuario confirmó todo
        // Deshabilitar el botón para evitar envíos duplicados
        confirmButton.disabled = true;
        confirmButton.innerHTML = '<i class="fal fa-spinner fa-spin"></i> Eliminando...';
    });
});