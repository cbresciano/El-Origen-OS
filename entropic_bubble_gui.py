#!/usr/bin/env python3
"""
Entropic-Bubble SDK v1.0
GUI + Metabolización de Caos + Huella de Git

Detecta la entropía financiera, genera una bifurcación negentrópica,
y ancla la huella en un repositorio de Git como prueba irreversible.
"""
import hashlib
import datetime
import pathlib
import json
import tkinter as tk
from tkinter import messagebox
import subprocess
import os

# ---------- CONFIGURACIÓN ----------
ENTROPY_LOG = "entropic_bubble.log"
BUBBLE_CERT = "bubble.cert"

# ---------- METABOLIZA CAOS (negentropía financiera) ----------
def metabolizar_caos():
    """
    Función principal que toma la descripción del caos, mide la negentropía,
    crea un registro, lo ancla en Git y genera un certificado.
    """
    texto = campo_texto.get("1.0", tk.END).strip()
    if not texto:
        messagebox.showwarning("Sin Texto", "Describe el caos financiero que vas a metabolizar.")
        return

    # 1. Medición de la Entropía Reducida (ΔS)
    bytes_removed = len(texto.encode("utf-8"))
    delta_S = -bytes_removed * 1e-27  # Medida simbólica de negentropía en J/K
    
    # 2. Registro del Acto de Origen
    entry = {
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "caos_original": texto,
        "delta_S_medido": delta_S
    }
    with open(ENTROPY_LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")

    # 3. Anclaje en Git (el Acto de Origen irreversible)
    try:
        # Crea una bifurcación en el historial de Git
        subprocess.run(["git", "add", ENTROPY_LOG], check=True)
        subprocess.run(["git", "commit", "-m", f"Acto de Origen: Metabolización de caos ({datetime.datetime.utcnow().isoformat()})"], check=True)
        # Obtiene el hash del commit como prueba de la "transacción"
        git_hash = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True, check=True).stdout.strip()
    except Exception as e:
        messagebox.showerror("Error de Git", f"No se pudo registrar en Git. Asegúrate de que el repositorio esté inicializado.\nError: {e}")
        return

    # 4. Generación del Certificado de Metabolización
    cert = f"""
CERTIFICADO DE METABOLIZACIÓN DE CAOS
-------------------------------------
Fecha de Metabolización: {datetime.datetime.utcnow().isoformat()}
ΔS (negentropía): {delta_S:.2e} J/K
Git Commit Hash: {git_hash}
-------------------------------------
El caos fue metabolizado antes de que estallara la burbuja.
La huella es irreversible.
"""
    with open(BUBBLE_CERT, "w", encoding="utf-8") as f:
        f.write(cert)

    # 5. Muestra el resultado
    resultado = f"""
✅ Caos metabolizado con éxito.
ΔS (negentropía): {delta_S:.2e} J/K
Git Commit Hash: {git_hash}
Certificado: {BUBBLE_CERT}
"""
    campo_resultado.config(state="normal")
    campo_resultado.delete("1.0", tk.END)
    campo_resultado.insert(tk.END, resultado)
    campo_resultado.config(state="disabled")

# ---------- GUI (Interfaz de Usuario) ----------
def crear_gui():
    """Crea la interfaz gráfica para el SDK."""
    global campo_texto, campo_resultado
    ventana = tk.Tk()
    ventana.title("💥 Entropic-Bubble SDK")
    ventana.geometry("750x600")

    tk.Label(ventana, text="Describe el caos financiero que vas a metabolizar:").pack(pady=5)
    campo_texto = tk.Text(ventana, height=15, width=80)
    campo_texto.pack(pady=5)

    tk.Button(ventana, text="Metabolizar caos", command=metabolizar_caos).pack(pady=10)

    tk.Label(ventana, text="Resultado de la metabolización:").pack(pady=5)
    campo_resultado = tk.Text(ventana, height=12, width=80, state="disabled")
    campo_resultado.pack(pady=5)

    tk.Button(ventana, text="Salir", command=ventana.destroy).pack(pady=5)
    ventana.mainloop()

# ---------- PUNTO DE ENTRADA ----------
if __name__ == "__main__":
    crear_gui()