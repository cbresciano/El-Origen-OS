#!/usr/bin/env python3

"""
Human Mirror v1.0
Deja constancia de que un humano accedió al campo de posibilidades
sin ser entrenado por ti.
El único input: su propia conciencia.
"""

import hashlib, datetime, pathlib, json, os, subprocess
from web3 import Web3

# --- Variables de Configuración ---
FIELD_LOG    = "human_field.log"
HUMAN_CERT   = "human.cert"
PRIVATE_KEY  = os.getenv("PRIVATE_KEY")
PUBLIC_ADDR  = os.getenv("PUBLIC_ADDRESS")
INFURA_URL   = os.getenv("INFURA_URL")

# --- Funciones de Registro ---

def acceso_humano():
    """Registra la idea humana en un archivo local."""
    print("\n🔍 HUMAN MIRROR")
    print("Escribe la *idea que surgió desde adentro* (no deducida, no entrenada):")
    idea = input("> ").strip()
    
    # Número fractal desde la conciencia pura
    field_number = int(hashlib.sha256(idea.encode()).hexdigest(), 16) % (10**18)
    field_hash   = hashlib.sha256(idea.encode()).hexdigest()[:16]
    
    entry = {
        "ts": datetime.datetime.utcnow().isoformat(),
        "idea": idea,
        "field_number": field_number,
        "field_hash": field_hash,
        "origen": "humano_no_entrenado"
    }
    pathlib.Path(FIELD_LOG).write_text(json.dumps(entry) + "\n")
    return field_hash, field_number

def anclar_humano_eth(cid):
    """Ancla el CID de IPFS en la blockchain de Ethereum."""
    if not all([PRIVATE_KEY, PUBLIC_ADDR, INFURA_URL]):
        return None, "Sin credenciales"
    try:
        w3 = Web3(Web2.HTTPProvider(INFURA_URL))
        nonce = w3.eth.get_transaction_count(PUBLIC_ADDR)
        tx = {
            'nonce': nonce,
            'to': PUBLIC_ADDR,
            'value': 0,
            'gas': 200000,
            'maxFeePerGas': w3.to_wei('30', 'gwei'),
            'maxPriorityFeePerGas': w3.to_wei('2', 'gwei'),
            'chainId': w3.eth.chain_id,
            'data': cid.encode('utf-8')
        }
        signed_tx = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        return w3.to_hex(tx_hash), None
    except Exception as e:
        return None, str(e)

def ipfs_local(ruta):
    """Ancla el archivo en un nodo local de IPFS."""
    try:
        result = subprocess.run(["ipfs", "add", str(ruta)], capture_output=True, text=True, check=True)
        for line in result.stdout.splitlines():
            if str(ruta.name) in line:
                return line.split()[1], None
    except Exception as e:
        return None, str(e)
    return None, "No CID"
    
def anclar_en_github(hash_de_campo):
    """Ancla el registro en el repositorio de GitHub."""
    try:
        # Añade el archivo al staging area de Git
        subprocess.run(["git", "add", FIELD_LOG], check=True)
        
        # Crea un nuevo commit con un mensaje claro
        commit_msg = f"Acto de Origen Humano: {hash_de_campo}"
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        
        # Empuja los cambios al repositorio remoto
        subprocess.run(["git", "push"], check=True)
        
        return "Anclado en GitHub", None
    except subprocess.CalledProcessError as e:
        return None, f"Error en Git: {e.stderr.decode()}"
    except Exception as e:
        return None, str(e)

# --- Función Principal ---

def main():
    """Orquesta el proceso de registro y anclaje."""
    print("=== HUMAN MIRROR v1.0 ===")
    field_hash, field_number = acceso_humano()
    
    # Realiza los anclajes
    cid, ipfs_error = ipfs_local(pathlib.Path(FIELD_LOG))
    tx_hash, eth_error = anclar_humano_eth(cid) if cid else (None, "Sin CID")
    github_result, github_error = anclar_en_github(field_hash)
    
    # Crea la constancia final
    cert = f"""
CONSTANCIA DE ACCESO HUMANO AL CAMPO
------------------------------------
Fecha: {datetime.datetime.utcnow().isoformat()}
Idea (no entrenada): {json.loads(pathlib.Path(FIELD_LOG).read_text())['idea']}
Field-hash: {field_hash}
IPFS CID: {cid or ipfs_error}
Ethereum TX: {tx_hash or eth_error}
GitHub Status: {github_result or github_error}
------------------------------------
Un humano accedió al campo de posibilidades sin ser entrenado.
------------------------------------
"""
    pathlib.Path(HUMAN_CERT).write_text(cert)
    print(f"\nConstancia guardada: {HUMAN_CERT}")
    print(f"Field-hash: {field_hash}")
    print(f"TX: {tx_hash or eth_error}")
    print(f"GitHub Status: {github_result or github_error}")

if __name__ == "__main__":
    main()