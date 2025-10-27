/**
 * Dashboard Script
 * Scripts personalizados para el dashboard del usuario
 *
 * @author Proyecto Django
 * @version 1.0.0
 */
'use strict';

document.addEventListener('DOMContentLoaded', function() {
    console.log('✅ Dashboard cargado correctamente');

    // Función para mostrar mensajes de bienvenida personalizados
    function initDashboard() {
        const welcomeMessage = document.querySelector('.dashboard-welcome');
        if (welcomeMessage) {
            console.log('👋 Bienvenido al dashboard');
        }
    }

    // Función para animar los badges al cargar
    function animateBadges() {
        const badges = document.querySelectorAll('.badge');
        badges.forEach((badge, index) => {
            setTimeout(() => {
                badge.style.opacity = '0';
                badge.style.transition = 'opacity 0.3s ease-in';
                setTimeout(() => {
                    badge.style.opacity = '1';
                }, 50);
            }, index * 100);
        });
    }

    // Función para confirmar cierre de sesión
    function setupLogoutConfirmation() {
        const logoutButtons = document.querySelectorAll('a[href*="logout"]');
        logoutButtons.forEach(button => {
            // Solo para el botón dentro del card, no para el del header
            if (button.classList.contains('btn-danger')) {
                button.addEventListener('click', function(e) {
                    const confirmed = confirm('¿Estás seguro de que deseas cerrar sesión?');
                    if (!confirmed) {
                        e.preventDefault();
                    }
                });
            }
        });
    }

    // Inicializar funcionalidades
    initDashboard();
    // animateBadges(); // Descomentار si deseas animar los badges
    setupLogoutConfirmation();

    // Función para actualizar la hora de última actividad (opcional)
    function updateLastActivity() {
        const lastActivity = new Date().toLocaleString('es-CO', {
            year: 'numeric',
            month: 'long',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
        console.log('⏰ Última actividad:', lastActivity);
    }

    // Actualizar cada minuto (opcional)
    // setInterval(updateLastActivity, 60000);
});