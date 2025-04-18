# Nombre del entorno virtual
$VENV_DIR = "venv"

# Crear el entorno virtual si no existe
if (-not (Test-Path $VENV_DIR)) {
    Write-Output "Creando entorno virtual..."
    python -m venv $VENV_DIR
} else {
    Write-Output "El entorno virtual ya existe."
}

# Activar el entorno virtual
& "$VENV_DIR\Scripts\Activate.ps1"

# Función para instalar o actualizar un paquete
function Install-Or-Update-Package {
    param (
        [string]$PackageName
    )
    
    try {
        # Verificar si el paquete está instalado y obtener su versión
        $installedPackages = pip list --format=json | ConvertFrom-Json
        $package = $installedPackages | Where-Object { $_.name -eq $PackageName }
        
        if ($null -eq $package) {
            Write-Output "Instalando $PackageName..."
            pip install $PackageName
            if ($LASTEXITCODE -ne 0) {
                Write-Error "Error al instalar $PackageName."
                return $false
            }
            Write-Output "$PackageName instalado correctamente."
        } else {
            Write-Output "$PackageName ya está instalado (versión $($package.version))."
            
            # Comprobar si hay una versión más nueva disponible
            Write-Output "Verificando actualizaciones para $PackageName..."
            pip list --outdated --format=json | ConvertFrom-Json | ForEach-Object {
                if ($_.name -eq $PackageName) {
                    Write-Output "Actualizando $PackageName de la versión $($package.version) a $($_.latest_version)..."
                    pip install --upgrade $PackageName
                    if ($LASTEXITCODE -ne 0) {
                        Write-Error "Error al actualizar $PackageName."
                        return $false
                    }
                    Write-Output "$PackageName actualizado correctamente a la versión $($_.latest_version)."
                }
            }
        }
        return $true
    }
    catch {
        Write-Error ("Error al procesar el paquete " + $PackageName + ": " + $_)
        return $false
    }
}

# Instalar o actualizar pipreqs
if (Install-Or-Update-Package -PackageName "pipreqs") {
    # Generar el archivo requirements.txt
    Write-Output "Generando requirements.txt con pipreqs..."
    pipreqs . --force

    # Instalar las dependencias desde requirements.txt
    Write-Output "Instalando dependencias desde requirements.txt..."
    pip install -r requirements.txt

    Write-Output "El script ha finalizado."
} else {
    Write-Error "No se pudo configurar pipreqs. El script no puede continuar."
    exit 1
}
