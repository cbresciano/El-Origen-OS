import json
import hashlib
import pathlib
import re
from datetime import datetime
from collections import Counter

# — FUNCIONES —
def calcular_hash(texto):
    return hashlib.sha256(texto.encode("utf-8")).hexdigest()[:8]

def calcular_delta_cognitivo(texto):
    palabras = texto.split()
    longitud = len(palabras)
    densidad = sum(len(p) for p in palabras) / max(1, longitud)
    return round((longitud * densidad) / 1000, 4)

def detectar_idea_sobrepasada(texto):
    patrones = [
        r"(se concibe como .*?)\.", r"(se articula desde .*?)\.",
        r"(se metaboliza en .*?)\.", r"(se bifurca hacia .*?)\.",
        r"(se reinterpreta .*?)\.", r"(se codifica como .*?)\.",
        r"(se extiende hacia .*?)\.", r"(se reabsorbe en .*?)\."
    ]
    for patron in patrones:
        coincidencias = re.findall(patron, texto, re.IGNORECASE)
        if coincidencias:
            return coincidencias[0].strip()
    return "Sobrepasamiento no detectado"

def detectar_operador_emergente(texto):
    texto = texto.lower()
    texto = re.sub(r"[^\w\s]", "", texto)
    palabras = texto.split()

    contextos = ["se articula", "se metaboliza", "se bifurca", "se codifica", "se concibe", "como operador", "estructura", "emerge", "ruptura", "origen"]
    frases = re.findall(r"\b(?:\w+\s){0,5}(?:%s)(?:\s\w+){0,5}\b" % "|".join(contextos), texto)

    candidatos = []
    for frase in frases:
        tokens = frase.split()
        for t in tokens:
            if len(t) > 6 and t not in ["estructura", "ruptura", "origen"]:
                candidatos.append(t)

    frecuencia = Counter(candidatos)
    operador = frecuencia.most_common(1)
    return operador[0][0] if operador else "Origen"

def registrar_huella_articulo(texto):
    idea_sobrepasada = detectar_idea_sobrepasada(texto)
    palabra_ruptura = detectar_operador_emergente(texto)

    delta_S = -3.30e-26
    hash_entropia = calcular_hash(idea_sobrepasada)
    hash_origen = calcular_hash(palabra_ruptura + texto)
    delta_cognitivo = calcular_delta_cognitivo(texto)
    energia = delta_cognitivo * 1e-27

    huella = {
        "timestamp": datetime.utcnow().isoformat(),
        "tipo": "articulo",
        "idea_sobrepasada": idea_sobrepasada,
        "palabra": palabra_ruptura,
        "hash_entropia": hash_entropia,
        "hash_origen": hash_origen,
        "delta_cognitivo": delta_cognitivo,
        "energia_computacional": energia
    }

    archivo = pathlib.Path("huellas.json")
    if archivo.exists():
        with archivo.open("r", encoding="utf-8") as f:
            datos = json.load(f)
    else:
        datos = []

    datos.append(huella)

    with archivo.open("w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)

    print(f"\n✅ Huella registrada.")
    print(f"🧠 Idea sobrepasada detectada: “{idea_sobrepasada}”")
    print(f"🧬 Operador emergente detectado: “{palabra_ruptura}”")

# — USO —
if __name__ == "__main__":
    texto = """Pega aquí el contenido completo de tu artículo desde Medium. El pensamiento no representa: metaboliza. La conciencia se articula como operador de bifurcación. El sistema se reabsorbe en una geometría de origen. Lo fractal no refleja: activa."""
    registrar_huella_articulo(texto)
