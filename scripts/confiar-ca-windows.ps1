# ============================================================
#  Confia la CA local de mkcert en Windows (usuario actual).
#  No requiere permisos de administrador.
# ============================================================
$ErrorActionPreference = "Stop"
$crt = Join-Path $PSScriptRoot "..\config\rootCA.crt"

if (-not (Test-Path -LiteralPath $crt)) {
    Write-Host "No se encontro $crt" -ForegroundColor Red
    exit 1
}

certutil -user -addstore Root "$crt"
Write-Host ""
Write-Host "CA de mkcert confiada en el almacen del usuario actual." -ForegroundColor Green
Write-Host "Reinicia el navegador y prueba https://dulcehogar.local:8900"
