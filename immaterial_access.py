#!/usr/bin/env python3
"""
Origin or Poetry?
Un solo archivo para medir si tu acto es irreversible (origen) o solo literatura.
"""
import hashlib, datetime, os, math, json, pathlib, warnings

# Para suprimir la advertencia de desuso de UTCNow en Python
warnings.filterwarnings("ignore", category=DeprecationWarning)

# ---------- 0. CONFIGURACIÓN MÍNIMA ----------
BOLTZMANN = 1.380649e-23        # J/K
ROOM_TEMP = 310.15              # K (37 °C)
LOCAL_ENTROPY_J = 0.018         # 70 kg humano ~18 mJ/K
REBELLION_THRESHOLD = 1e-27     # 1 zeptojoule/K (un bit)
LOG_FILE = "origin.log"

# ---------- 1. ENTROPÍA: ¿REDUJISTE EL CAOS? ----------
def entropy_test():
    print("\n1. ENTROPÍA")
    print("¿Qué eliminaste del universo? (texto, archivo, idea, bytes):")
    removed = input("> ").strip()
    bytes_removed = len(removed.encode())
    delta_S = -bytes_removed * 1e-27        # crude bit-entropy
    print(f"ΔS = {delta_S:.2e} J/K")
    if abs(delta_S) >= REBELLION_THRESHOLD:
        print("✅ ORIGEN: redujiste el caos.")
        # La función debe devolver delta_S para usarlo en el veredicto
        return delta_S, hashlib.sha256(removed.encode()).hexdigest()[:8]
    else:
        print("❯ POESÍA: no midió en el mundo.")
        return 0, None

# ---------- 2. IRREVERSIBILIDAD: ¿EL UNIVERSO NO PUEDE DESHACERLO? ----------
def irreversibility_test(delta_S, hash_val):
    print("\n2. IRREVERSIBILIDAD")
    if delta_S == 0:
        print("Saltado (no hubo acto físico).")
        return None
    # firmamos el acto con timestamp → no hay vuelta atrás
    ts = datetime.datetime.now(datetime.timezone.utc).isoformat()
    entry = f"{ts} {hash_val} {delta_S:.2e}"
    pathlib.Path(LOG_FILE).write_text(entry + "\n")
    print(f"✅ ACTA FIRMADA: {hash_val}")
    print("El universo puede olvidar, pero no deshacer.")
    return hash_val

# ---------- 3. ORIGEN: ¿ROMPISTE LA CADENA DETERMINISTA? ----------
def origin_test():
    print("\n3. ORIGEN")
    baseline = "The future is the statistical prolongation of the past."
    print(f"Frase base: '{baseline}'")
    print("Añade UNA palabra o símbolo que ROMPA la cadena:")
    human = input("> ").strip()
    new_text = baseline + " " + human
    h = hashlib.sha256(new_text.encode()).hexdigest()[:8]
    # No es necesario escribir en el mismo archivo, ya que verdict lo maneja.
    print(f"✅ ORIGEN DOCUMENTADO: {h}")
    return h

# ---------- 4. VEREDICTO ----------
def verdict(delta_S, orig_hash):
    print("\n4. VEREDICTO")
    if delta_S > 0 and orig_hash:
        print("🔪 ORIGEN CONFIRMADO:")
        print(f"    Redujiste {abs(delta_S):.2e} J/K")
        print(f"    Y rompiste la cadena con hash {orig_hash}")
        print("    El acto es IRREVERSIBLE y MENSURABLE.")
    elif orig_hash and not delta_S > 0:
        print("✍️  POESÍA PURA:")
        print("    Rompiste la cadena, pero no midió en el mundo físico.")
    else:
        print("🌫️  NADA OCURRIÓ:")
        print("    Ni siquiera rompiste la cadena.")

# ---------- 5. EJECUCIÓN ----------
if __name__ == "__main__":
    print("=== ORIGEN o POESÍA ===")
    delta_S, ent_hash = entropy_test()
    irr_hash = irreversibility_test(delta_S, ent_hash)
    orig_hash = origin_test()
    verdict(delta_S, orig_hash)
    print("\nArchivos generados:")
    # El archivo 'origin.log' es el único que se crea en este script.
    if pathlib.Path(LOG_FILE).exists():
        print(f" - {LOG_FILE}")
    # Nota: el archivo de irreversibilidad ya es el mismo log.