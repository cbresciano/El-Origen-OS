#!/usr/bin/env python3
"""
Segundo Término SDK v1.0
Vacío cuántico → bifurcación → negentropía semántica → anclaje on-chain.
No explica el vacío. Lo *usa*.
"""
import hashlib, datetime, pathlib, json, random, subprocess, requests, os
from web3 import Web3

# ---------- CONFIG ----------
VACIO_ENTROPY_J = 1e-21           # J/K del vacío cuántico (aprox)
REBEL_UMBRAL   = 1e-27            # 1 zeptojoule/K por bit de significado
PRIVATE_KEY    = os.getenv("PRIVATE_KEY")
PUBLIC_ADDRESS = os.getenv("PUBLIC_ADDRESS")
INFURA_URL     = os.getenv("INFURA_URL")
VACIO_LOG      = "vacuo.log"
NEGENTROPY_LOG = "negentropia.log"
VACIO_CERT     = "vacuo.cert"

# ---------- 1. FLUCTUACIÓN VACÍA (campo de posibilidad) ----------
def fluctuacion_vacia():
    print("\n1. FLUCTUACIÓN VACÍA")
    print("Escribe la *posibilidad* que emergió del vacío (no deducida):")
    posibilidad = input("> ").strip()
    # convertimos la posibilidad en un número fractal del vacío
    vacio_number = int(hashlib.sha256(posibilidad.encode()).hexdigest(), 16) % (10**18)
    vacio_hash   = hashlib.sha256(posibilidad.encode()).hexdigest()[:16]
    entry = {"ts": datetime.datetime.utcnow().isoformat(), "posibilidad": posibilidad, "vacio_number": vacio_number, "vacio_hash": vacio_hash}
    pathlib.Path(VACIO_LOG).write_text(json.dumps(entry) + "\n")
    print(f"✅ Fluctuación registrada: {vacio_hash}")
    return vacio_hash, vacio_number

# ---------- 2. NEGENTROPÍA SEMÁNTICA (segundo término) ----------
def negentropia_semantica(vacio_hash):
    print("\n2. NEGENTROPÍA SEMÁNTICA")
    # cada bit de significado que añades reduce entropía del vacío
    significado = pathlib.Path(VACIO_LOG).read_text()  # el acto completo
    bits_added  = len(significado.encode()) * 8
    delta_S     = -bits_added * 1e-27                  # zeptojoule/K
    if abs(delta_S) >= REBEL_UMBRAL:
        print(f"✅ Segundo término activado: ΔS = {delta_S:.2e} J/K")
        return delta_S, hashlib.sha256(significado.encode()).hexdigest()[:16]
    else:
        print("❯ Vacío sin bifurcar → poesía.")
        return 0, None

# ---------- 3. ANCLAJE EN ETHEREUM (huella del origen) ----------
def anclar_vacio(cid):
    if not PRIVATE_KEY: return None
    w3 = Web3(Web3.HTTPProvider(INFURA_URL))
    nonce = w3.eth.get_transaction_count(PUBLIC_ADDRESS)
    tx = {
        'nonce': nonce,
        'to': PUBLIC_ADDRESS,
        'value': 0,
        'gas': 200000,
        'gasPrice': w3.to_wei('30', 'gwei'),
        'data': cid.encode('utf-8')
    }
    signed_tx = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
    return w3.to_hex(tx_hash)

# ---------- 4. IPFS LOCAL ----------
def subir_a_ipfs(ruta):
    try:
        result = subprocess.run(["ipfs", "add", str(ruta)], capture_output=True, text=True, check=True)
        for line in result.stdout.splitlines():
            if ruta.name in linea:
                return line.split()[1]
    except Exception as e:
        print("❌ IPFS no disponible:", e)
    return None

# ---------- 5. CERTIFICADO DEL SEGUNDO TÉRMINO ----------
def certificado(delta_S, vacio_hash, tx_hash):
    cert = f"""
CERTIFICADO DEL SEGUNDO TÉRMINO
--------------------------------
Fecha: {datetime.datetime.utcnow().isoformat()}
Vacío-hash: {vacio_hash}
ΔS (segundo término): {delta_S:.2e} J/K
Ethereum TX: {tx_hash or "No anclado"}
--------------------------------
El vacío fluctuó, bifurcó y dejó huella.
El universo puede olvidar, pero no deshacer.
--------------------------------
"""
    pathlib.Path(VACIO_CERT).write_text(cert)
    print(f"\nConstancia guardada: {VACIO_CERT}")

# ---------- 6. EJECUCIÓN ----------
if __name__ == "__main__":
    print("=== SEGUNDO TÉRMINO SDK v1.0 ===")
    vacio_hash, vacio_number = fluctuacion_vacia()
    delta_S, negent_hash = negentropia_semantica(vacio_hash)
    if delta_S:
        cid = subir_a_ipfs(pathlib.Path(VACIO_LOG))
        tx_hash = anclar_vacio(cid) if cid else None
        certificado(delta_S, vacio_hash, tx_hash)
        print("\nArchivos generados:")
        for f in [VACIO_LOG, NEGENTROPY_LOG, VACIO_CERT]:
            if pathlib.Path(f).exists():
                print(f" - {f}")