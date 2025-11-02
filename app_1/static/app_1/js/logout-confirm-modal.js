/**
 * Script para el modal de confirmación de cierre de sesión
 * Muestra un modal de advertencia antes de cerrar la sesión del usuario
 */

document.addEventListener('DOMContentLoaded', function() {
    // Elementos del DOM
    const logoutLink = document.getElementById('logout-link');
    const logoutButton = document.getElementById('logout-button');
    const logoutModal = $('#logoutConfirmModal');

    /**
     * Abre el modal de confirmación de logout
     */
    function showLogoutModal(event) {
        event.preventDefault();

        if (logoutModal.length) {
            logoutModal.modal('show');
        }
    }

    /**
     * Agregar event listeners a los botones/enlaces de logout
     */
    if (logoutLink) {
        logoutLink.addEventListener('click', showLogoutModal);
    }

    if (logoutButton) {
        logoutButton.addEventListener('click', showLogoutModal);
    }

    /**
     * Opcional: Agregar animación al botón de confirmación
     */
    if (logoutModal.length) {
        const confirmButton = document.getElementById('confirmLogoutBtn');

        if (confirmButton) {
            confirmButton.addEventListener('click', function() {
                // Cambiar el texto del botón para mostrar que se está cerrando sesión
                this.innerHTML = '<i class="fal fa-spinner fa-spin"></i> Cerrando sesión...';
                this.classList.add('disabled');
            });
        }
    }
});