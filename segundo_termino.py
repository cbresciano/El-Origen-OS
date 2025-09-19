#!/usr/bin/env python3
"""
Segundo Término SDK v1.0
Vacío cuántico → bifurcación → negentropía semántica → anclaje en GitHub.
No explica el vacío. Lo *usa*.
"""
import hashlib
import datetime
import pathlib
import json
import subprocess
import os
from dotenv import load_dotenv

# ---------- CONFIG ----------
VACIO_LOG = "vacuo.log"
VACIO_CERT = "vacuo.cert"

# --- Cargar credenciales desde .env ---
load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO_URL = os.getenv("REPO_URL")

# ---------- 1. FLUCTUACIÓN VACÍA (campo de posibilidad) ----------
def fluctuacion_vacia():
    print("\n1. FLUCTUACIÓN VACÍA")
    print("Escribe la *posibilidad* que emergió del vacío (no deducida):")
    posibilidad = input("> ").strip()
    # convertimos la posibilidad en un número fractal del vacío
    vacio_number = int(hashlib.sha256(posibilidad.encode()).hexdigest(), 16) % (10**18)
    vacio_hash = hashlib.sha256(posibilidad.encode()).hexdigest()[:16]
    entry = {"ts": datetime.datetime.utcnow().isoformat(), "posibilidad": posibilidad, "vacio_number": vacio_number, "vacio_hash": vacio_hash}
    pathlib.Path(VACIO_LOG).write_text(json.dumps(entry) + "\n")
    print(f"✅ Fluctuación registrada: {vacio_hash}")
    return vacio_hash, vacio_number

# ---------- 2. NEGENTROPÍA SEMÁNTICA (segundo término) ----------
def negentropia_semantica(vacio_hash):
    print("\n2. NEGENTROPÍA SEMÁNTICA")
    # cada bit de significado que añades reduce entropía del vacío
    try:
        significado = pathlib.Path(VACIO_LOG).read_text()
        bits_added = len(significado.encode()) * 8
        # Constante de entropía del vacío y umbral de rebelión, definidos en el código original.
        REBEL_UMBRAL = 1e-27
        delta_S = -bits_added * 1e-27
        if abs(delta_S) >= REBEL_UMBRAL:
            print(f"✅ Segundo término activado: ΔS = {delta_S:.2e} J/K")
            return delta_S, hashlib.sha256(significado.encode()).hexdigest()[:16]
        else:
            print("❯ Vacío sin bifurcar → poesía.")
            return 0, None
    except FileNotFoundError:
        print("❌ Archivo de log del vacío no encontrado.")
        return 0, None

# ---------- 3. ANCLAJE EN GITHUB (huella del origen) ----------
def anclar_en_github(commit_message):
    if not GITHUB_TOKEN or not REPO_URL:
        print("❌ Faltan credenciales de GitHub en el archivo .env.")
        return False, "Faltan credenciales"

    try:
        # Añadir el archivo de log para el commit
        subprocess.run(["git", "add", VACIO_LOG], check=True, capture_output=True, text=True)
        # Hacer el commit con el mensaje del certificado
        subprocess.run(["git", "commit", "-m", commit_message], check=True, capture_output=True, text=True)
        # Sincronizar con el repositorio remoto usando el token
        repo_url_with_token = REPO_URL.replace("https://", f"https://{GITHUB_TOKEN}@")
        subprocess.run(["git", "push", repo_url_with_token], check=True, capture_output=True, text=True)
        
        return True, None
    except subprocess.CalledProcessError as e:
        print(f"❌ Error al ejecutar comandos de Git: {e.stderr}")
        return False, e.stderr
    except Exception as e:
        print(f"❌ Ocurrió un error inesperado: {e}")
        return False, str(e)

# ---------- 4. CERTIFICADO DEL SEGUNDO TÉRMINO ----------
def certificado(delta_S, vacio_hash):
    cert = f"""
CERTIFICADO DEL SEGUNDO TÉRMINO
--------------------------------
Fecha: {datetime.datetime.utcnow().isoformat()}
Vacío-hash: {vacio_hash}
ΔS (segundo término): {delta_S:.2e} J/K
--------------------------------
El vacío fluctuó, bifurcó y dejó huella.
El universo puede olvidar, pero no deshacer.
--------------------------------
"""
    print(cert)
    return cert

# ---------- 5. EJECUCIÓN ----------
if __name__ == "__main__":
    print("=== SEGUNDO TÉRMINO SDK v1.0 ===")
    vacio_hash, vacio_number = fluctuacion_vacia()
    delta_S, negent_hash = negentropia_semantica(vacio_hash)
    if delta_S:
        commit_message = certificado(delta_S, vacio_hash)
        success, error_msg = anclar_en_github(commit_message)
        if success:
            print(f"✅ Acto de Origen registrado en GitHub. El certificado se encuentra en el historial del commit.")
        else:
            print(f"❌ El anclaje en GitHub falló. Error: {error_msg}")
    
    # El archivo de log sigue estando disponible localmente si lo necesitas.
    # El certificado ahora es el mensaje del commit, no se guarda como archivo separado.