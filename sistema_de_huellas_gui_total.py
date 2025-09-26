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
import os
from dotenv import load_dotenv

# --- Configuración Negentrópica ---
TRACE_ROOT_DIR = "traces"
# Se asume la configuración inicial de .env para GITHUB_TOKEN y REPO_URL
load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO_URL = os.getenv("REPO_URL")

# --- Generador de nombre de subdirectorio limpio y único ---
def limpiar_titulo(titulo_completo):
    """
    Genera una ruta de subdirectorio limpia y única a partir del título del artículo.
    Ignora el subtítulo (texto después de ':').
    """
    # 1. Extraer solo la parte principal (antes del primer ':')
    titulo_principal = titulo_completo.split(':')[0].strip()
    
    # 2. Obtener fecha
    fecha = datetime.now().strftime('%Y-%m-%d')
    
    # 3. Crear slug limpio
    base = titulo_principal.lower().strip()
    # Reemplazar caracteres no alfanuméricos (ni espacios, ni guiones bajos)
    slug = re.sub(r'[^\w\s-]', '', base).strip().lower()
    # Reemplazar espacios y guiones con un único guion bajo
    slug = re.sub(r'[-\s]+', '_', slug)
    
    # 4. Combinar fecha y slug
    nombre_directorio = f"{fecha}_{slug}"
    
    # 5. Construir la ruta completa dentro del directorio raíz de trazas
    ruta_subdirectorio = pathlib.Path(TRACE_ROOT_DIR) / nombre_directorio
    
    return ruta_subdirectorio, titulo_principal

# --- Convertidor estructural a MD (Guarda en el subdirectorio) ---
def convertir_a_md(texto, titulo_principal, subdirectorio_path):
    """Convierte el texto en formato Markdown y lo guarda en el subdirectorio."""
    # El archivo MD toma el nombre del subdirectorio para consistencia
    nombre_archivo = f"{subdirectorio_path.stem}.md"
    archivo_path = subdirectorio_path / nombre_archivo
    
    md_lines = [f"# {titulo_principal}", f"*Publicado: {datetime.now(timezone.utc).isoformat()}*", "---"]
    
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
    
    with archivo_path.open("w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))
        
    return archivo_path

# --- Medidor de negentropía semántica ---
def calcular_negentropia(texto):
    """Calcula la entropía semántica y el índice de negentropía."""
    palabras = [p.lower() for p in re.findall(r'\b\w+\b', texto) if len(p) > 2]
    total_palabras = len(palabras)
    if total_palabras == 0:
        return {
            "entropia_semantica": 0,
            "conceptos_clave": [],
            "indice_negentropia": 0
        }

    frecuencia = Counter(palabras)
    # Cálculo de la entropía de Shannon (base 2)
    entropia = -sum((f/total_palabras) * math.log2(f/total_palabras) for f in frecuencia.values())
    
    # Los "conceptos clave" (palabras repetidas) reducen el caos e incrementan el orden temático
    conceptos_clave = [p for p in frecuencia if frecuencia[p] > 1]
    indice_negentropia = round(len(conceptos_clave) / (entropia + 1), 3)

    return {
        "entropia_semantica": round(entropia, 3),
        "conceptos_clave": conceptos_clave,
        "indice_negentropia": indice_negentropia
    }

# --- Detector semántico de Operador ---
def detectar_operador(texto):
    """Detecta si la conciencia es tratada como un operador estructural."""
    if "conciencia" in texto.lower() or "consciousness" in texto.lower():
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
    """Añade los archivos modificados, hace commit y push al repositorio."""
    if not GITHUB_TOKEN or not REPO_URL:
        messagebox.showerror("Error de credenciales", "Faltan las claves de GitHub en el archivo .env.")
        return False, "Faltan credenciales"

    try:
        # Usar el token para la autenticación en la URL
        repo_url_with_token = REPO_URL.replace("https://", f"https://oauth2:{GITHUB_TOKEN}@")

        # Añadir todos los archivos modificados (incluyendo la nueva carpeta 'traces')
        subprocess.run(["git", "add", "."], check=True, capture_output=True, text=True)
        # Hacer el commit
        subprocess.run(["git", "commit", "-m", commit_message], check=True, capture_output=True, text=True)
        # Sincronizar con el repositorio remoto
        subprocess.run(["git", "push", repo_url_with_token], check=True, capture_output=True, text=True)
        
        return True, "Registro en GitHub exitoso."
    except subprocess.CalledProcessError as e:
        return False, f"Error al ejecutar comandos de Git:\n{e.stdout}\n{e.stderr}"
    except Exception as e:
        return False, f"Ocurrió un error inesperado: {e}"

# --- Guardar el reporte JSON dentro del subdirectorio ---
def registrar_reporte_json(subdirectorio_path, titulo, neg_data, sem_data, texto):
    """Guarda el reporte detallado para el artículo DENTRO de su subdirectorio."""
    reporte_data = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "titulo_principal": titulo,
        "hash_articulo": hashlib.sha256(texto.encode("utf-8")).hexdigest(),
        "idea_sobrepasada": sem_data["idea_sobrepasada"],
        "operador_emergente": sem_data["operador_emergente"],
        "indice_negentropia": neg_data["indice_negentropia"],
        "entropia_semantica": neg_data["entropia_semantica"],
        "conceptos_clave": neg_data["conceptos_clave"],
    }
    
    archivo_json_path = subdirectorio_path / "huella_report.json"
    
    with archivo_json_path.open("w", encoding="utf-8") as f:
        json.dump(reporte_data, f, indent=2, ensure_ascii=False)
        
    return reporte_data

# --- Actualizar el índice general de huellas (Se queda en la raíz) ---
def actualizar_indice_general(huella_data, texto):
    """Actualiza el índice maestro huellas_registradas.json en la raíz."""
    archivo_indice = pathlib.Path("huellas_registradas.json")
    
    if archivo_indice.exists():
        with archivo_indice.open("r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = [] # Si el archivo está corrupto, inicia de nuevo
            
        hash_articulo = hashlib.sha256(texto.encode("utf-8")).hexdigest()
        for entrada in data:
            if entrada.get("hash_articulo") == hash_articulo:
                messagebox.showwarning("Acto Duplicado", "Este artículo ya fue registrado. Tu doctrina no permite la redundancia.")
                return None
    else:
        data = []
        
    # Crear un resumen limpio para el índice general
    indice_resumen = {
        "timestamp": huella_data["timestamp"],
        "titulo_principal": huella_data["titulo_principal"],
        "hash_articulo": huella_data["hash_articulo"],
        # Guardamos la ruta relativa al subdirectorio creado
        "directorio_relativo": str(pathlib.Path(TRACE_ROOT_DIR) / huella_data["subdirectorio_slug"]),
        "indice_negentropia": huella_data["indice_negentropia"],
        "entropia_semantica": huella_data["entropia_semantica"],
    }
    
    data.append(indice_resumen)
    
    with archivo_indice.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        
    return indice_resumen

# --- GUI principal (El orquestador negentrópico) ---
def procesar_texto():
    try:
        titulo_completo = campo_titulo.get().strip() or "Artículo sin título"
        texto = campo_texto.get("1.0", tk.END).strip()
        
        if not texto:
            messagebox.showwarning("Falta texto", "Pega el artículo antes de procesar.")
            return

        # 1. Generar la ruta negentrópica y el título principal
        subdirectorio_path, titulo_principal = limpiar_titulo(titulo_completo)
        
        # 2. Ejecutar el Acto Negentrópico: crear el directorio (genera orden estructural)
        os.makedirs(subdirectorio_path, exist_ok=True)
        
        # 3. Calcular métricas
        neg_data = calcular_negentropia(texto)
        sem_data = detectar_operador(texto)
        
        # 4. Convertir y guardar el archivo MD dentro del subdirectorio
        ruta_md = convertir_a_md(texto, titulo_principal, subdirectorio_path)
        
        # 5. Guardar el reporte JSON detallado DENTRO del subdirectorio
        huella_reporte_local = registrar_reporte_json(subdirectorio_path, titulo_principal, neg_data, sem_data, texto)
        
        # 6. Preparar datos para el índice general
        # Añadir temporalmente el slug para pasarlo al índice
        huella_reporte_local['subdirectorio_slug'] = subdirectorio_path.name
        
        # 7. Preparar commit
        commit_msg = f"Acto Negentrópico: Registro de '{titulo_principal}'"
        
        # 8. Anclar a GitHub (Añade el nuevo directorio)
        success, error_msg = anclar_en_github(commit_msg)

        if success:
            # 9. Registrar en el índice general (huellas_registradas.json)
            huella_registrada = actualizar_indice_general(huella_reporte_local, texto)
            
            if huella_registrada:
                # Mostrar resultado
                resultado = f"""
✅ Huella registrada (Negentropía estructural)
📁 Directorio de la Huella: {huella_registrada['directorio_relativo']}
📄 Título Principal: {huella_registrada['titulo_principal']}
📉 Entropía semántica: {huella_registrada['entropia_semantica']}
📈 Índice de negentropía (ΔS): {huella_reporte_local['indice_negentropia']}
🧠 Operador emergente: {sem_data['operador_emergente']}
🧨 Idea sobrepasada: {sem_data['idea_sobrepasada']}
🔗 Commit de GitHub: {commit_msg}
"""
                campo_resultado.config(state="normal")
                campo_resultado.delete("1.0", tk.END)
                campo_resultado.insert(tk.END, resultado)
                campo_resultado.config(state="disabled")
                messagebox.showinfo("Proceso Completo", "La huella estructural ha sido registrada con orden negentrópico. ¡El caos ha sido reducido!")
            # Si huella_registrada es None, es porque era un duplicado y ya se mostró la advertencia
        else:
            messagebox.showerror("Error al registrar", f"No se pudo registrar en GitHub (la huella no se completó).\n{error_msg}")
            
    except Exception as e:
        messagebox.showerror("Error General", f"Ocurrió un error inesperado: {e}")
        # print(f"ERROR DETECTADO: {e}") # Usar para depuración

# --- GUI setup ---
ventana = tk.Tk()
ventana.title("🧬 Sistema de Huellas — GUI Negentrópica")

tk.Label(ventana, text="Título del artículo: (Solo el principal se usa para el directorio)").pack()
campo_titulo = tk.Entry(ventana, width=60)
campo_titulo.pack()

tk.Label(ventana, text="Pega el texto del artículo:").pack()
campo_texto = tk.Text(ventana, height=20, width=80)
campo_texto.pack()

tk.Button(ventana, text="Metabolizar y registrar huella (Acto Negentrópico)", command=procesar_texto).pack(pady=10)

tk.Label(ventana, text="Resultado de la huella:").pack()
campo_resultado = tk.Text(ventana, height=15, width=80, state="disabled")
campo_resultado.pack()

ventana.mainloop()
