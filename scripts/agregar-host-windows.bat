@echo off
REM ============================================================
REM  Agrega dulcehogar.local al archivo hosts de Windows.
REM  EJECUTAR COMO ADMINISTRADOR (clic derecho -> Ejecutar como admin)
REM ============================================================
set "HOSTS=%SystemRoot%\System32\drivers\etc\hosts"

findstr /C:"dulcehogar.local" "%HOSTS%" >nul 2>&1
if %errorlevel%==0 (
    echo La entrada "dulcehogar.local" ya existe en el archivo hosts.
) else (
    echo 127.0.0.1 dulcehogar.local>> "%HOSTS%"
    echo Entrada agregada: 127.0.0.1 dulcehogar.local
)

echo.
echo Ahora puedes abrir: https://dulcehogar.local:8900/api/saludo?nombre=Equipo
pause
