# Description: This script deletes stored GitHub credentials from the Windows Credential Manager.
# Usage: Run this script in PowerShell to remove GitHub credentials.
# Requirements: PowerShell with the CredentialManager module installed.

# Instalar y cargar el módulo CredentialManager
try {
    Install-Module -Name CredentialManager -Force -Scope CurrentUser -ErrorAction Stop
    Import-Module -Name CredentialManager -ErrorAction Stop
    Write-Host "El modulo CredentialManager se ha instalado e importado correctamente."
} catch {
    Write-Host "Error al instalar o importar el modulo CredentialManager:" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    exit 1
}

# Intentar eliminar las credenciales de GitHub
try {
    $cred = Get-StoredCredential -Target "git:https://github.com" -ErrorAction Stop
    if ($cred) {
        Remove-StoredCredential -Target "git:https://github.com" -Type Generic -ErrorAction Stop
        Write-Host "Las credenciales de GitHub se han eliminado correctamente del Administrador de Credenciales de Windows." -ForegroundColor Green
    } else {
        Write-Host "No se encontraron credenciales de GitHub para eliminar." -ForegroundColor Yellow
    }
} catch {
    Write-Host "Ocurrio un error al intentar eliminar las credenciales de GitHub:" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
}

# Listar todas las credenciales almacenadas
try {
    cmd /c cmdkey /list
} catch {
    Write-Host "No fue posible listar las credenciales almacenadas." -ForegroundColor Red
}

# Pausar la ejecución para revisión
cmd /c pause

# Note: Ensure you have the necessary permissions to delete credentials from the Credential Manager.
# This script is intended to be run in a PowerShell environment with administrative privileges.
# End of script
