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

# Comprobar si pipreqs está instalado
if (-not (pip show pipreqs -ErrorAction SilentlyContinue)) {
    Write-Output "Instalando pipreqs..."
    pip install pipreqs
} else {
    Write-Output "pipreqs ya está instalado."
}

# Generar el archivo requirements.txt
Write-Output "Generando requirements.txt con pipreqs..."
pipreqs .

# Instalar las dependencias desde requirements.txt
Write-Output "Instalando dependencias desde requirements.txt..."
pip install -r requirements.txt

Write-Output "El script ha finalizado."
