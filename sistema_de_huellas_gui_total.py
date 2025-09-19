Aquí tienes el código completo y corregido. He implementado la solución que te di antes y he hecho algunas optimizaciones adicionales para mejorar el rendimiento y la legibilidad.

Python

import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timezone
import pathlib
import math
from collections import Counter
import subprocess
import requests
import json
import time
import networkx as nx
import matplotlib.pyplot as plt
from web3 import Web3
import os
from dotenv import load_dotenv
import re
import hashlib
import base64

# --- Cargar credenciales ---
load_dotenv()
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
PUBLIC_ADDRESS = os.getenv("PUBLIC_ADDRESS")
INFURA_URL = os.getenv("INFURA_URL")
INFURA_IPFS_PROJECT_ID = os.getenv("INFURA_IPFS_PROJECT_ID")
INFURA_IPFS_API_SECRET = os.getenv("INFURA_IPFS_API_SECRET")

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

# --- Medidor de negentropía semántica —
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

# --- Subida a IPFS a través de la API de Infura ---
def subir_a_ipfs(ruta_md):
    INFURA_IPFS_URL = "https://ipfs.infura.io:5001/api/v0/add"
    
    if not INFURA_IPFS_PROJECT_ID or not INFURA_IPFS_API_SECRET:
        messagebox.showerror("Error de credenciales", "Faltan las claves de la API de Infura en tu archivo .env.")
        return None

    try:
        auth_string = f"{INFURA_IPFS_PROJECT_ID}:{INFURA_IPFS_API_SECRET}"
        auth_bytes = auth_string.encode("utf-8")
        auth_base64 = base64.b64encode(auth_bytes).decode("utf-8")
        
        headers = {
            "Authorization": f"Basic {auth_base64}"
        }

        with open(ruta_md, 'rb') as f:
            files = {'file': f}
            response = requests.post(INFURA_IPFS_URL, headers=headers, files=files)
            response.raise_for_status()
            cid = response.json()['Hash']
            print(f"✅ Archivo subido a Infura con éxito. CID: {cid}")
            return cid
            
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error de conexión a Infura", f"No se pudo subir a Infura. Verifica tu conexión y tus claves API.\n{e}")
        return None
    except Exception as e:
        messagebox.showerror("Error de subida a Infura", f"Ocurrió un error inesperado al subir a Infura.\n{e}")
        return None

# --- Anclaje en Ethereum ---
def anclar_en_ethereum(cid):
    if not INFURA_URL or not PRIVATE_KEY or not PUBLIC_ADDRESS:
        messagebox.showwarning("Faltan credenciales", "No se puede anclar sin credenciales de Ethereum.")
        return None
    
    try:
        w3 = Web3(Web3.HTTPProvider(INFURA_URL))
        if not w3.is_connected():
            raise ConnectionError("No se pudo conectar a la red de Ethereum.")
        
        nonce = w3.eth.get_transaction_count(PUBLIC_ADDRESS)
        tx = {
            'nonce': nonce,
            'to': Web3.to_checksum_address(PUBLIC_ADDRESS),
            'value': 0,
            'gas': 200000,
            'gasPrice': w3.to_wei('30', 'gwei'),
            'data': Web3.to_hex(text=cid)  # LINEA CORREGIDA
        }
        signed_tx = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        return w3.to_hex(tx_hash)
    except Exception as e:
        messagebox.showerror("Error Ethereum", f"No se pudo anclar la huella.\n{e}")
        return None

# --- Registro de huella con verificación de unicidad ---
def registrar_huella(titulo, texto, ruta_md, neg_data, sem_data, cid, tx_hash):
    huella_data = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "titulo": titulo,
        "idea_sobrepasada": sem_data["idea_sobrepasada"],
        "operador_emergente": sem_data["operador_emergente"],
        "indice_negentropia": neg_data["indice_negentropia"],
        "entropia_semantica": neg_data["entropia_semantica"],
        "conceptos_clave": neg_data["conceptos_clave"],
        "archivo_md": str(ruta_md),
        "ipfs_cid": cid or "Error",
        "estado_ipfs": "Distribuido" if cid else "Pendiente",
        "ethereum_tx": tx_hash or "No anclado"
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

# --- Visualización como grafo con título abreviado ---
def visualizar_grafo():
    archivo = pathlib.Path("huellas_registradas.json")
    if not archivo.exists():
        messagebox.showinfo("Sin datos", "No hay huellas registradas aún.")
        return
    with archivo.open("r", encoding="utf-8") as f:
        data = json.load(f)
    G = nx.DiGraph()
    
    for h in data:
        titulo = h["titulo"]
        etiqueta = titulo if len(titulo) < 40 else titulo[:37] + "..."
        negentropia = h["indice_negentropia"]
        
        G.add_node(etiqueta, negentropia=negentropia)
        
        for otro in data:
            if h != otro and h["operador_emergente"] == otro["operador_emergente"] and h["operador_emergente"] != "No se detectó un operador emergente":
                otro_titulo = otro["titulo"]
                otro_etiqueta = otro_titulo if len(otro_titulo) < 40 else otro_titulo[:37] + "..."
                G.add_edge(etiqueta, otro_etiqueta)

    if not G.nodes:
        messagebox.showinfo("Sin nodos", "No hay suficientes datos para generar el grafo.")
        return

    pos = nx.spring_layout(G, k=0.8, iterations=50)
    negentropias = [G.nodes[n].get("negentropia", 0) for n in G.nodes]
    
    plt.figure(figsize=(10, 8))
    nx.draw_networkx(
        G, pos,
        with_labels=True,
        node_color=negentropias,
        cmap=plt.cm.plasma,
        node_size=1000,
        font_size=8,
        font_color="white",
        edge_color="#333",
        arrowstyle='-|>',
        arrowsize=15
    )
    
    sm = plt.cm.ScalarMappable(cmap=plt.cm.plasma, norm=plt.Normalize(vmin=min(negentropias), vmax=max(negentropias)))
    sm.set_array([])
    plt.colorbar(sm, label="Índice de Negentropía (ΔS)")
    
    plt.title("Grafo de Huellas Estructurales")
    plt.axis("off")
    plt.show()

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
        cid = subir_a_ipfs(ruta_md)
        tx_hash = anclar_en_ethereum(cid) if cid else None
        
        huella_registrada = registrar_huella(titulo, texto, ruta_md, neg_data, sem_data, cid, tx_hash)

        if huella_registrada:
            resultado = f"""
✅ Huella registrada
📄 Título: {huella_registrada['titulo']}
📉 Entropía semántica: {huella_registrada['entropia_semantica']}
📈 Índice de negentropía (ΔS): {huella_registrada['indice_negentropia']}
🧠 Operador emergente: {huella_registrada['operador_emergente']}
🧨 Idea sobrepasada: {huella_registrada['idea_sobrepasada']}
📡 CID IPFS: {huella_registrada['ipfs_cid']}
🔗 Estado IPFS: {huella_registrada['estado_ipfs']}
🧬 Ethereum TX: {huella_registrada['ethereum_tx']}
"""
            campo_resultado.config(state="normal")
            campo_resultado.delete("1.0", tk.END)
            campo_resultado.insert(tk.END, resultado)
            campo_resultado.config(state="disabled")
            
            messagebox.showinfo("Proceso Completo", "La huella estructural ha sido registrada exitosamente.")
        
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

tk.Button(ventana, text="Visualizar grafo de huellas", command=visualizar_grafo).pack(pady=10)

ventana.mainloop()