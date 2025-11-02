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

    // Verificar que los elementos existen
    if (!confirmCheckbox || !confirmButton || !deleteAccountForm) {
        console.warn('Elementos del modal de eliminación de cuenta no encontrados');
        return;
    }

    /**
     * Habilitar/deshabilitar botón de eliminación basado en checkbox
     */
    confirmCheckbox.addEventListener('change', function() {
        confirmButton.disabled = !this.checked;
    });

    /**
     * Limpiar el formulario al cerrar el modal
     * Esto asegura que el usuario deba confirmar nuevamente si vuelve a abrir el modal
     */
    if (deleteAccountModal.length) {
        deleteAccountModal.on('hidden.bs.modal', function () {
            deleteAccountForm.reset();
            confirmButton.disabled = true;
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