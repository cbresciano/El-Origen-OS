import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timezone
import pathlib
import math
from collections import Counter
import subprocess
import json
import re
import hashlib
import base64
import os
from dotenv import load_dotenv

# --- Cargar credenciales desde .env ---
load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO_URL = os.getenv("REPO_URL")

# --- Generador de nombre de archivo desde título ---
def generar_nombre_archivo(titulo):
    base = "_".join(titulo.lower().split()[:8])
    limpio = "".join(c for c in base if c.isalnum() or c == "_")
    return limpio + ".md"

# --- Convertidor estructural con nombre dinámico y mejor formateo ---
def convertir_a_md(texto, titulo="Artículo sin título"):
    nombre_archivo = generar_nombre_archivo(titulo)
    md_lines = [f"# {titulo}", f"*Publicado: {datetime.now(timezone.utc).isoformat()}*", "---"]
    
    lineas = texto.strip().split("\n")
    for linea in lineas:
        linea = linea.strip()
        if not linea:
            continue
            
        if re.match(r"^\s*#+\s", linea):
            md_lines.append(f"\n{linea}")
        elif re.match(r"^\s*[-*]\s", linea):
            md_lines.append(f"\n{linea}")
        elif re.match(r"^\s*>", linea):
            md_lines.append(f"\n{linea}")
        elif linea.isupper() and len(linea) < 60:
            md_lines.append(f"\n## {linea.title()}")
        else:
            md_lines.append(f"\n{linea}")
            
    md_lines.append("\n---")
    
    archivo = pathlib.Path(nombre_archivo)
    with archivo.open("w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))
        
    return archivo.absolute()

# --- Medidor de negentropía semántica ---
def calcular_negentropia(texto):
    palabras = [p.lower() for p in re.findall(r'\b\w+\b', texto) if len(p) > 2]
    total_palabras = len(palabras)
    if total_palabras == 0:
        return {
            "entropia_semantica": 0,
            "conceptos_clave": [],
            "indice_negentropia": 0
        }

    frecuencia = Counter(palabras)
    entropia = -sum((f/total_palabras) * math.log2(f/total_palabras) for f in frecuencia.values())
    conceptos_clave = [p for p in frecuencia if frecuencia[p] > 1]
    indice_negentropia = round(len(conceptos_clave) / (entropia + 1), 3)

    return {
        "entropia_semantica": round(entropia, 3),
        "conceptos_clave": conceptos_clave,
        "indice_negentropia": indice_negentropia
    }

# --- Detector semántico ---
def detectar_operador(texto):
    if "conciencia" in texto.lower():
        return {
            "idea_sobrepasada": "Conciencia como epifenómeno",
            "operador_emergente": "Conciencia como operador estructural"
        }
    return {
        "idea_sobrepasada": "No se detectó un operador emergente",
        "operador_emergente": "No se detectó un operador emergente"
    }

# --- Anclaje en GitHub ---
def anclar_en_github(commit_message):
    if not GITHUB_TOKEN or not REPO_URL:
        messagebox.showerror("Error de credenciales", "Faltan las claves de GitHub en el archivo .env.")
        return False, "Faltan credenciales"

    try:
        # Configurar la URL del repositorio con el token para la autenticación
        repo_url_with_token = REPO_URL.replace("https://", f"https://{GITHUB_TOKEN}@")

        # Añadir todos los archivos modificados
        subprocess.run(["git", "add", "."], check=True)
        # Hacer el commit
        subprocess.run(["git", "commit", "-m", commit_message], check=True)
        # Sincronizar con el repositorio remoto
        subprocess.run(["git", "push", repo_url_with_token], check=True)
        
        return True, "Registro en GitHub exitoso."
    except subprocess.CalledProcessError as e:
        return False, f"Error al ejecutar comandos de Git: {e.stderr.decode('utf-8') if e.stderr else e}"
    except Exception as e:
        return False, f"Ocurrió un error inesperado: {e}"

# --- Registro de huella con verificación de unicidad ---
def registrar_huella(titulo, texto, ruta_md, neg_data, sem_data, commit_msg):
    huella_data = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "titulo": titulo,
        "idea_sobrepasada": sem_data["idea_sobrepasada"],
        "operador_emergente": sem_data["operador_emergente"],
        "indice_negentropia": neg_data["indice_negentropia"],
        "entropia_semantica": neg_data["entropia_semantica"],
        "conceptos_clave": neg_data["conceptos_clave"],
        "archivo_md": str(ruta_md),
        "github_commit": commit_msg or "No anclado"
    }

    archivo = pathlib.Path("huellas_registradas.json")
    if archivo.exists():
        with archivo.open("r", encoding="utf-8") as f:
            data = json.load(f)
            hash_articulo = hashlib.sha256(texto.encode("utf-8")).hexdigest()
            for entrada in data:
                if entrada.get("hash_articulo") == hash_articulo:
                    messagebox.showwarning("Acto Duplicado", "Este artículo ya fue registrado. Tu doctrina no permite la redundancia.")
                    return None
    else:
        data = []
    
    huella_data["hash_articulo"] = hashlib.sha256(texto.encode("utf-8")).hexdigest()
    data.append(huella_data)
    
    with archivo.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        
    return huella_data

# --- GUI principal ---
def procesar_texto():
    try:
        titulo = campo_titulo.get().strip() or "Artículo sin título"
        texto = campo_texto.get("1.0", tk.END).strip()
        
        if not texto:
            messagebox.showwarning("Falta texto", "Pega el artículo antes de procesar.")
            return

        ruta_md = convertir_a_md(texto, titulo)
        neg_data = calcular_negentropia(texto)
        sem_data = detectar_operador(texto)
        
        commit_msg = f"Acto de Origen: Registro de '{titulo}'"
        success, error_msg = anclar_en_github(commit_msg)

        if success:
            huella_registrada = registrar_huella(titulo, texto, ruta_md, neg_data, sem_data, commit_msg)
            if huella_registrada:
                resultado = f"""
✅ Huella registrada
📄 Título: {huella_registrada['titulo']}
📉 Entropía semántica: {huella_registrada['entropia_semantica']}
📈 Índice de negentropía (ΔS): {huella_registrada['indice_negentropia']}
🧠 Operador emergente: {huella_registrada['operador_emergente']}
🧨 Idea sobrepasada: {huella_registrada['idea_sobrepasada']}
🔗 Commit de GitHub: {huella_registrada['github_commit']}
"""
                campo_resultado.config(state="normal")
                campo_resultado.delete("1.0", tk.END)
                campo_resultado.insert(tk.END, resultado)
                campo_resultado.config(state="disabled")
                messagebox.showinfo("Proceso Completo", "La huella estructural ha sido registrada exitosamente en GitHub.")
        else:
            messagebox.showerror("Error al registrar", f"No se pudo registrar en GitHub.\n{error_msg}")
            
    except Exception as e:
        messagebox.showerror("Error General", f"Ocurrió un error inesperado: {e}")

# --- GUI setup ---
ventana = tk.Tk()
ventana.title("🧬 Sistema de Huellas — GUI Total")

tk.Label(ventana, text="Título del artículo:").pack()
campo_titulo = tk.Entry(ventana, width=60)
campo_titulo.pack()

tk.Label(ventana, text="Pega el texto del artículo:").pack()
campo_texto = tk.Text(ventana, height=20, width=80)
campo_texto.pack()

tk.Button(ventana, text="Metabolizar y registrar huella", command=procesar_texto).pack(pady=10)

tk.Label(ventana, text="Resultado de la huella:").pack()
campo_resultado = tk.Text(ventana, height=15, width=80, state="disabled")
campo_resultado.pack()

ventana.mainloop()