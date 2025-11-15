# Script PowerShell para ver qué procesos están usando los puertos de Laragon

Write-Host "=" -NoNewline
Write-Host ("=" * 69)
Write-Host "PROCESOS USANDO PUERTOS DE LARAGON"
Write-Host "=" -NoNewline
Write-Host ("=" * 69)
Write-Host ""

$puertos = @(3306, 80, 443, 8000)

foreach ($puerto in $puertos) {
    Write-Host "Puerto $puerto :" -ForegroundColor Yellow
    Write-Host ("-" * 70)
    
    try {
        $conexiones = netstat -ano | Select-String ":$puerto " | Select-String "LISTENING"
        
        if ($conexiones) {
            foreach ($linea in $conexiones) {
                $partes = $linea -split '\s+'
                $pid = $partes[-1]
                
                if ($pid -match '^\d+$') {
                    try {
                        $proceso = Get-Process -Id $pid -ErrorAction SilentlyContinue
                        if ($proceso) {
                            Write-Host "  PID: $pid - Proceso: $($proceso.ProcessName) - Ruta: $($proceso.Path)" -ForegroundColor Green
                        } else {
                            Write-Host "  PID: $pid - Proceso no encontrado (puede haber terminado)" -ForegroundColor Red
                        }
                    } catch {
                        Write-Host "  PID: $pid - No se pudo obtener información del proceso" -ForegroundColor Red
                    }
                }
            }
        } else {
            Write-Host "  No hay procesos escuchando en este puerto" -ForegroundColor Gray
        }
    } catch {
        Write-Host "  Error al verificar el puerto: $_" -ForegroundColor Red
    }
    
    Write-Host ""
}

Write-Host "=" -NoNewline
Write-Host ("=" * 69)
Write-Host "SOLUCIONES:"
Write-Host "=" -NoNewline
Write-Host ("=" * 69)
Write-Host ""
Write-Host "1. Si MySQL (3306) está ocupado:"
Write-Host "   - Detené el servicio MySQL de Windows:"
Write-Host "     services.msc -> MySQL -> Detener"
Write-Host ""
Write-Host "2. Si Apache (80/443) está ocupado:"
Write-Host "   - Detené IIS si está corriendo:"
Write-Host "     services.msc -> World Wide Web Publishing Service -> Detener"
Write-Host "   - O cambiá el puerto en Laragon"
Write-Host ""
Write-Host "3. Si Django (8000) está ocupado:"
Write-Host "   - Detené el servidor Django (Ctrl+C en la terminal)"
Write-Host ""
Write-Host "4. Para detener un proceso específico:"
Write-Host "   taskkill /PID <numero_pid> /F"
Write-Host ""

