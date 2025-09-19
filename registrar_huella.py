import json
from datetime import datetime
import pathlib

def registrar_huella_structural(delta_S, hash_entropia, palabra, hash_origen, delta_vector, energia):
    """
    Registra la huella de un acto de origen en un archivo JSON.
    """
    huella_data = {
        "timestamp": datetime.utcnow().isoformat(),
        "delta_entropia": delta_S,
        "hash_entropia": hash_entropia,
        "palabra": palabra,
        "hash_origen": hash_origen,
        "delta_cognitivo": delta_vector,
        "energia_computacional": energia,
    }
    
    huellas_file = pathlib.Path("huellas.json")
    
    # Lee los datos existentes o inicializa una lista
    if huellas_file.exists():
        with huellas_file.open("r", encoding="utf-8") as f:
            datos = json.load(f)
    else:
        datos = []
        
    datos.append(huella_data)
    
    with huellas_file.open("w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4)
        
    print("\n✅ Huella estructural registrada en huellas.json")


# Ejecuta el registro con los valores de tu último test
if __name__ == "__main__":
    registrar_huella_structural(-3.30e-26, "822ca754", "Fractalismo", "0212b266", 1.5204, 1.52e-27)