#!/usr/bin/env python3
"""
Script extendido: ¿Tu pensamiento dejó huella y reconfiguró el sistema?
"""

import hashlib, datetime, pathlib

# — CONFIGURACIÓN —
REBELLION_THRESHOLD = 1e-27  # Umbral mínimo para considerar negentropía
LOG_FILE = "huella.log"

# — ENTROPÍA —
def medir_entropia(texto):
    bytes_texto = len(texto.encode())
    delta_S = -bytes_texto * 1e-27
    print(f"\n1. ENTROPÍA")
    print(f"ΔS = {delta_S:.2e} J/K")
    if abs(delta_S) >= REBELLION_THRESHOLD:
        print("✅ Origen: redujiste el caos.")
    else:
        print("❯ Poesía: no midió en el mundo físico.")
    return delta_S, hashlib.sha256(texto.encode()).hexdigest()[:8]

# — IRREVERSIBILIDAD —
def registrar_acto(hash_val, delta_S):
    ts = datetime.datetime.now(datetime.timezone.utc).isoformat()
    entrada = f"{ts} {hash_val} {delta_S:.2e}"
    pathlib.Path(LOG_FILE).write_text(entrada + "\n")
    print(f"\n2. IRREVERSIBILIDAD")
    print(f"✅ Acta registrada: {hash_val}")
    print("El universo puede olvidar, pero no deshacer.")

# — RUPTURA DETERMINISTA —
def romper_cadena(palabra):
    base = "The future is the statistical prolongation of the past."
    nuevo = base + " " + palabra
    h = hashlib.sha256(nuevo.encode()).hexdigest()[:8]
    print(f"\n3. ORIGEN")
    print(f"✅ Ruptura registrada: {h}")
    return nuevo, h

# — TRAZA NEURONAL —
def simular_vector(texto):
    return [hashlib.sha256((texto + str(i)).encode()).digest()[0] / 255 for i in range(10)]

def delta_vector(v1, v2):
    return sum((a - b)**2 for a, b in zip(v1, v2))**0.5

def registrar_traza(texto, estado_prev):
    estado_nuevo = simular_vector(texto)
    delta = delta_vector(estado_prev, estado_nuevo)
    energia = delta * 1e-27
    ts = datetime.datetime.now(datetime.timezone.utc).isoformat()
    print(f"\n4. TRAZA NEURONAL")
    print(f"Timestamp: {ts}")
    print(f"Delta cognitivo: {delta:.4f}")
    print(f"Energía computacional: {energia:.2e} J/K")
    return estado_nuevo

# — EJECUCIÓN —
if __name__ == "__main__":
    print("=== TEST DE ORIGEN EXTENDIDO ===")
    estado_inicial = simular_vector("estado basal")

    idea = input("¿Qué idea eliminaste del universo?\n> ").strip()
    delta_S, hash_entropia = medir_entropia(idea)
    if delta_S != 0:
        registrar_acto(hash_entropia, delta_S)

    palabra = input("Añade una palabra que rompa el determinismo:\n> ").strip()
    nuevo_texto, hash_origen = romper_cadena(palabra)

    estado_final = registrar_traza(nuevo_texto, estado_inicial)

    print("\n— VEREDICTO FINAL —")
    if delta_S > 0:
        print("🔪 Origen confirmado: el acto fue mensurable y dejó traza cognitiva.")
    elif hash_origen:
        print("✍️ Poesía pura: rompiste la cadena, y el sistema fue reconfigurado, aunque sin huella física.")
    else:
        print("🌫️ Nada ocurrió: ni siquiera rompiste la cadena.")
