import pathlib
import json
import subprocess
import os
from dotenv import load_dotenv

load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO_URL = os.getenv("REPO_URL")

def anclar_en_github(commit_message):
    if not GITHUB_TOKEN or not REPO_URL:
        print("❌ Faltan credenciales de GitHub en el archivo .env.")
        return False, "Faltan credenciales"

    try:
        repo_url_with_token = REPO_URL.replace("https://", f"https://{GITHUB_TOKEN}@")
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", commit_message], check=True)
        subprocess.run(["git", "push", repo_url_with_token], check=True)
        return True, "Registro en GitHub exitoso."
    except subprocess.CalledProcessError as e:
        return False, f"Error al ejecutar comandos de Git: {e.stderr.decode('utf-8') if e.stderr else e}"
    except Exception as e:
        return False, f"Ocurrió un error inesperado: {e}"

def completar_registro():
    archivo_huellas = pathlib.Path("huellas_registradas.json")
    if not archivo_huellas.exists():
        print("❌ Archivo de huellas no encontrado.")
        return

    with archivo_huellas.open("r", encoding="utf-8") as f:
        huellas = json.load(f)

    huella_a_completar = next((h for h in reversed(huellas) if h.get("ethereum_tx") == "No anclado"), None)

    if not huella_a_completar:
        print("✅ No se encontraron huellas pendientes de anclaje. El sistema está en orden.")
        return

    commit_message = f"Acto de Origen: Se completa el registro de '{huella_a_completar['titulo']}'"
    print(f"Buscando huella pendiente. Procediendo a registrar en GitHub.")

    success, error_msg = anclar_en_github(commit_message)

    if success:
        huella_a_completar["estado_ipfs"] = "Distribuido"
        huella_a_completar["github_commit"] = commit_message
        with archivo_huellas.open("w", encoding="utf-8") as f:
            json.dump(huellas, f, indent=2)
        print("✅ Acto de Origen Completado. El registro ha sido actualizado.")
    else:
        print(f"❌ El anclaje en GitHub falló: {error_msg}. Intenta de nuevo más tarde.")

if __name__ == "__main__":
    completar_registro()