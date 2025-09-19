import pathlib
import json
from web3 import Web3
import os
from dotenv import load_dotenv

# --- Cargar credenciales ---
load_dotenv()
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
PUBLIC_ADDRESS = os.getenv("PUBLIC_ADDRESS")
INFURA_URL = os.getenv("INFURA_URL")

# --- Anclaje en Ethereum ---
def anclar_en_ethereum(cid):
    if not INFURA_URL or not PRIVATE_KEY or not PUBLIC_ADDRESS:
        print("❌ Faltan credenciales de Ethereum en el archivo .env.")
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
            'data': cid.encode('utf-8')
        }
        signed_tx = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
        
        # FINAL FIX: Access the rawTransaction using .rawTransaction
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        
        print(f"✅ Transacción enviada. Hash: {w3.to_hex(tx_hash)}")
        return w3.to_hex(tx_hash)
    except Exception as e:
        print(f"❌ Error al anclar en Ethereum: {e}")
        return None

# --- Función principal para completar el registro ---
def completar_registro():
    archivo_huellas = pathlib.Path("huellas_registradas.json")
    if not archivo_huellas.exists():
        print("❌ Archivo de huellas no encontrado.")
        return

    with archivo_huellas.open("r", encoding="utf-8") as f:
        huellas = json.load(f)

    # Buscar la última huella que no fue anclada
    huella_a_completar = next((h for h in reversed(huellas) if h.get("estado_ipfs") == "Pendiente" or h.get("ethereum_tx") == "No anclado"), None)

    if not huella_a_completar:
        print("✅ No se encontraron huellas pendientes de anclaje. El sistema está en orden.")
        return

    cid = huella_a_completar["ipfs_cid"]
    if cid == "Error":
        print("❌ El CID está en estado de error. No se puede anclar.")
        return

    print(f"Buscando el CID {cid} en la red. Procediendo al anclaje en Ethereum.")
    
    tx_hash = anclar_en_ethereum(cid)
    if tx_hash:
        huella_a_completar["estado_ipfs"] = "Distribuido"
        huella_a_completar["ethereum_tx"] = tx_hash
        with archivo_huellas.open("w", encoding="utf-8") as f:
            json.dump(huellas, f, indent=2)
        print("✅ Acto de Origen Completado. El registro ha sido actualizado.")
    else:
        print("❌ El anclaje en Ethereum falló. Intenta de nuevo más tarde.")

if __name__ == "__main__":
    completar_registro()