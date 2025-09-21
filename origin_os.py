#!/usr/bin/env python3
"""
Origin OS v1.0
Operating system for validating philosophies by their ability to:
1. Measurably reduce entropy.
2. Sign irreversibility.
3. Reconfigure the system (bifurcate).
It's not argued. It's executed.
"""
import hashlib, datetime, pathlib, json, os

# ---------- CONFIG ----------
REBEL_UMBRAL = 1e-27            # 1 zeptojoule/K per bit removed
ORIGIN_LOG   = "origin.log"
ENTROPY_LOG  = "entropy.log"
BIFURC_LOG   = "bifurcation.log"

# ---------- 1. ENTROPY: DID YOU REDUCE CHAOS? ----------
def entropy_act(entropic_thought):
    bytes_removed = len(entropic_thought.encode())
    delta_S = -bytes_removed * 1e-27
    if abs(delta_S) >= REBEL_UMBRAL:
        return delta_S, hashlib.sha256(entropic_thought.encode()).hexdigest()[:16]
    else:
        return 0, None

# ---------- 2. IRREVERSIBILITY: DID YOU SIGN THE ACT? ----------
def irreversibility(delta_S, hash_val):
    if delta_S == 0: return None
    ts = datetime.datetime.now(datetime.UTC).isoformat()
    entry = {"ts": ts, "hash": hash_val, "delta_S": delta_S}
    pathlib.Path(ENTROPY_LOG).write_text(json.dumps(entry) + "\n")
    pathlib.Path(ORIGIN_LOG).write_text(f"{ts} {hash_val}\n")
    return hash_val

# ---------- 3. BIFURCATION: DID YOU BREAK THE CHAIN? ----------
def bifurcation(origin_word):
    baseline = "The future is the statistical prolongation of the past."
    new_text = baseline + " " + origin_word
    bifurcation_hash = hashlib.sha256(new_text.encode()).hexdigest()[:16]
    pathlib.Path(BIFURC_LOG).write_text(json.dumps({"baseline": baseline, "origin": origin_word, "hash": bifurcation_hash}) + "\n")
    return bifurcation_hash

# ---------- 4. VERDICT ----------
def verdict(ent_hash, bifur_hash):
    if ent_hash and bifur_hash:
        return f"""
ORIGIN CONFIRMED:
   You reduced chaos and broke the chain.
   Hashes: {ent_hash} | {bifur_hash}
   The act is IRREVERSIBLE and MEASURABLE.
"""
    elif bifur_hash and not ent_hash:
        return "POETRY: you bifurcated, but it didn't measure in the world."
    else:
        return "NOTHING: there was no act."

# ---------- 5. VISUAL PROOF ----------
def create_proof_file(bifur_hash, ent_hash):
    entropy_reduction_val = "N/A"
    try:
        log_content = pathlib.Path(ENTROPY_LOG).read_text()
        entropy_reduction_val = float(log_content.split('delta_S":')[1].split(',')[0])
    except (FileNotFoundError, IndexError, ValueError):
        pass

    cert = f"""
ORIGIN OS - PROOF OF ACT
------------------------------
Date: {datetime.datetime.now(datetime.UTC).isoformat()}
Entropy reduction: {entropy_reduction_val if isinstance(entropy_reduction_val, str) else f"{entropy_reduction_val:.2e}"} J/K
Entropy hash: {ent_hash or "N/A"}
Bifurcation hash: {bifur_hash or "N/A"}
------------------------------
The universe can forget, but not undo.
------------------------------
"""
    cert_file = f"{bifur_hash or 'poetry'}.cert"
    pathlib.Path(cert_file).write_text(cert)
    
    return cert_file

# ---------- NUEVA FUNCIÓN PARA LA GUI ----------
def generate_act_of_origin_gui(entropic_thought, bifurcation_phrase):
    # 1. Ejecuta el Acto de la Entropía
    delta_S, ent_hash = entropy_act(entropic_thought)

    # 2. Registra la Irreversibilidad
    irr_hash = irreversibility(delta_S, ent_hash)

    # 3. Ejecuta la Bifurcación
    bifur_hash = bifurcation(bifurcation_phrase)
    
    # 4. Obtiene el Veredicto
    verdict_text = verdict(ent_hash, bifur_hash)
    
    # 5. Crea el certificado
    cert_file = create_proof_file(bifur_hash, ent_hash)
    
    # 6. Devuelve el output completo como una cadena de texto
    output = f"""
=== ORIGIN OS v1.0 ===

1. ENTROPY
Write or paste the ENTROPIC thought you will ELIMINATE:
> {entropic_thought}
ΔS = {delta_S:.2e} J/K
✅ ORIGIN: you measurably reduced chaos.
✅ ACT SIGNED: {ent_hash}

3. BIFURCATION
Base phrase: 'The future is the statistical prolongation of the past.'
Add the word/symbol that emerges FROM within (not deduced):
> {bifurcation_phrase}
✅ BIFURCATION DOCUMENTED: {bifur_hash}

4. VERDICT
🔥 {verdict_text}

Proof saved: {cert_file}

"""
    return output

# ---------- 6. EXECUTION (Mantenemos la lógica de la línea de comandos) ----------
if __name__ == "__main__":
    print("=== ORIGIN OS v1.0 ===")
    delta_S, ent_hash = entropy_act(input("Write or paste the ENTROPIC thought you will ELIMINATE:\n> ").strip())
    irr_hash = irreversibility(delta_S, ent_hash)
    print(f" ACT SIGNED: {irr_hash}")
    
    print("\n3. BIFURCATION")
    baseline = "The future is the statistical prolongation of the past."
    print(f"Base phrase: '{baseline}'")
    bifur_hash = bifurcation(input("Add the word/symbol that emerges FROM within (not deduced):\n> ").strip())
    print(f"BIFURCATION DOCUMENTED: {bifur_hash}")
    
    print("\n4. VERDICT")
    print(verdict(ent_hash, bifur_hash))
    
    cert_file = create_proof_file(bifur_hash, ent_hash)
    print(f"\nProof saved: {cert_file}")
    
    print("\nFiles generated:")
    for f in [ORIGIN_LOG, ENTROPY_LOG, BIFURC_LOG, cert_file]:
        if pathlib.Path(f).exists():
            print(f" - {f}")