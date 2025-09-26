#!/usr/bin/env python3
"""
Relación-Macro SDK v1.1
GUI completa + anclaje en GitHub + modelo probabilístico del "wedge"
Registra (edad_hombre, edad_mujer) → verifica si cae dentro del wedge → ancla en GitHub.
"""
import hashlib, datetime, pathlib, json, os, subprocess, requests
import tkinter as tk
from tkinter import messagebox, Text
import base64
from dotenv import load_dotenv

# Carga las variables de entorno desde el archivo .env
load_dotenv()

# ---------- CONFIGURACIÓN ----------
WEDGE_CERT = "relacion.cert"

def get_credentials():
    """Obtiene las credenciales de GitHub desde variables de entorno."""
    github_token = os.getenv("GITHUB_TOKEN")
    repo_url = os.getenv("REPO_URL")
    
    if not github_token:
        messagebox.showerror(
            "Variable de Entorno Faltante",
            "Por favor, configura la variable de entorno GITHUB_TOKEN en tu archivo .env."
        )
        return None, None, None
        
    if not repo_url:
        messagebox.showerror(
            "Variable de Entorno Faltante",
            "Por favor, configura la variable de entorno REPO_URL en tu archivo .env."
        )
        return None, None, None

    try:
        parts = repo_url.split('/')
        github_user = parts[-2]
        github_repo = parts[-1].replace('.git', '')
        return github_token, github_user, github_repo
    except IndexError:
        messagebox.showerror(
            "Formato de URL Inválido",
            "La URL del repositorio (REPO_URL) no tiene un formato válido. Debe ser como 'https://github.com/usuario/repositorio.git'."
        )
        return None, None, None

# ---------- GITHUB ----------
def subir_a_github(content, github_token, github_user, github_repo):
    """Sube el contenido a GitHub como un nuevo archivo."""
    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    timestamp = datetime.datetime.utcnow().isoformat().replace(":", "-").replace(".", "-")
    file_path = f"registros/{timestamp}.json"
    
    data = {
        "message": f"Registro de pareja en el wedge: {timestamp}",
        "content": base64.b64encode(content.encode('utf-8')).decode('utf-8')
    }
    
    api_url = f"https://api.github.com/repos/{github_user}/{github_repo}/contents/{file_path}"
    
    try:
        response = requests.put(api_url, headers=headers, data=json.dumps(data))
        response.raise_for_status()
        return response.json()['content']['html_url'], None
    except requests.exceptions.HTTPError as e:
        return None, f"Error de GitHub: {e.response.status_code} - {e.response.text}"
    except Exception as e:
        return None, str(e)

# ---------- MODELO DEL WEDGE ----------
def modelo_wedge(age_man, age_woman):
    # Cresta del wedge: y = x/2 + 7
    cresta = age_man / 2 + 7
    # Probabilidad cae dentro del wedge (± 2 años de la cresta)
    prob = max(0, 100 - abs(age_woman - cresta) * 10)
    return cresta, prob

# ---------- REGISTRO DE PAREJA ----------
def registrar_pareja():
    try:
        edad_h = int(campo_hombre.get())
        edad_m = int(campo_mujer.get())
    except ValueError:
        messagebox.showwarning("Entrada inválida", "Por favor, ingresa edades válidas (números enteros).")
        return

    if edad_h < 18 or edad_m < 18:
        messagebox.showwarning("Edad inválida", "Ambos deben ser ≥ 18 años.")
        return

    cresta, prob = modelo_wedge(edad_h, edad_m)
    dentro = prob >= 80

    huella = hashlib.sha256(f"{edad_h}{edad_m}{datetime.datetime.utcnow().isoformat()}".encode()).hexdigest()[:16]
    entry = {
        "ts": datetime.datetime.utcnow().isoformat(),
        "edad_hombre": edad_h,
        "edad_mujer": edad_m,
        "cresta_wedge": cresta,
        "probabilidad": prob,
        "dentro_wedge": dentro,
        "huella": huella
    }

    # Lógica de anclaje en GitHub
    github_token, github_user, github_repo = get_credentials()
    if not github_token:
        return

    github_url, github_error = subir_a_github(json.dumps(entry, indent=2), github_token, github_user, github_repo)

    # Certificado
    cert = f"""
CERTIFICADO DE PAREJA EN EL WEDGE
---------------------------------
Fecha: {datetime.datetime.utcnow().isoformat()}
Edad hombre: {edad_h}
Edad mujer: {edad_m}
Cresta del wedge (y = x/2 + 7): {cresta:.1f}
Probabilidad de caer dentro: {prob:.1f}%
¿Dentro del wedge?: {"SÍ" if dentro else "NO"}
Huella irreversible: {huella}
URL de GitHub: {github_url or github_error}
---------------------------------
Esta pareja ha sido registrada en el modelo probabilístico del mercado de relaciones.
---------------------------------
"""
    pathlib.Path(WEDGE_CERT).write_text(cert)

    # Mostrar resultado
    resultado = f"""
✅ Pareja registrada
Edad H: {edad_h} | Edad M: {edad_m}
Cresta: {cresta:.1f} | Prob: {prob:.1f}%
¿Dentro del wedge?: {"SÍ" if dentro else "NO"}
URL de GitHub: {github_url or github_error}
Certificado: {WEDGE_CERT}
"""
    campo_resultado.config(state="normal")
    campo_resultado.delete("1.0", tk.END)
    campo_resultado.insert(tk.END, resultado)
    campo_resultado.config(state="disabled")

# ---------- GUI ----------
def crear_gui():
    global campo_hombre, campo_mujer, campo_resultado
    ventana = tk.Tk()
    ventana.title("💑 Relación-Macro SDK — GUI con GitHub")
    ventana.geometry("800x600")

    tk.Label(ventana, text="Edad del hombre:").pack(pady=5)
    campo_hombre = tk.Entry(ventana, width=10)
    campo_hombre.pack(pady=5)

    tk.Label(ventana, text="Edad de la mujer:").pack(pady=5)
    campo_mujer = tk.Entry(ventana, width=10)
    campo_mujer.pack(pady=5)

    tk.Button(ventana, text="Registrar pareja en el wedge", command=registrar_pareja).pack(pady=10)

    tk.Label(ventana, text="Resultado del registro:").pack(pady=5)
    campo_resultado = tk.Text(ventana, height=12, width=80, state="disabled")
    campo_resultado.pack(pady=5)

    tk.Button(ventana, text="Salir", command=ventana.destroy).pack(pady=5)
    ventana.mainloop()

# ---------- MAIN ----------
if __name__ == "__main__":
    crear_gui()
