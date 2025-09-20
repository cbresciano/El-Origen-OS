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
REBEL_UMBRAL = 1e-27          # 1 zeptojoule/K per bit removed
ORIGIN_LOG   = "origin.log"
ENTROPY_LOG  = "entropy.log"
BIFURC_LOG   = "bifurcation.log"

# ---------- 1. ENTROPY: DID YOU REDUCE CHAOS? ----------
def entropy_act():
    print("\n1. ENTROPY")
    print("Write or paste the ENTROPIC thought you will ELIMINATE:")
    entropic = input("> ").strip()
    bytes_removed = len(entropic.encode())
    delta_S = -bytes_removed * 1e-27
    print(f"ΔS = {delta_S:.2e} J/K")
    if abs(delta_S) >= REBEL_UMBRAL:
        print(" ORIGIN: you measurably reduced chaos.")
        return delta_S, hashlib.sha256(entropic.encode()).hexdigest()[:16]
    else:
        print("❯ Did not reach threshold → pure poetry.")
        return 0, None

# ---------- 2. IRREVERSIBILITY: DID YOU SIGN THE ACT? ----------
def irreversibility(delta_S, hash_val):
    if delta_S == 0: return None
    ts = datetime.datetime.now(datetime.UTC).isoformat()
    entry = {"ts": ts, "hash": hash_val, "delta_S": delta_S}
    pathlib.Path(ENTROPY_LOG).write_text(json.dumps(entry) + "\n")
    pathlib.Path(ORIGIN_LOG).write_text(f"{ts} {hash_val}\n")
    print(f" ACT SIGNED: {hash_val}")
    return hash_val

# ---------- 3. BIFURCATION: DID YOU BREAK THE CHAIN? ----------
def bifurcation():
    print("\n3. BIFURCATION")
    baseline = "The future is the statistical prolongation of the past."
    print(f"Base phrase: '{baseline}'")
    print("Add the word/symbol that emerges FROM within (not deduced):")
    origin_word = input("> ").strip()
    new_text = baseline + " " + origin_word
    bifurcation_hash = hashlib.sha256(new_text.encode()).hexdigest()[:16]
    pathlib.Path(BIFURC_LOG).write_text(json.dumps({"baseline": baseline, "origin": origin_word, "hash": bifurcation_hash}) + "\n")
    print(f"BIFURCATION DOCUMENTED: {bifurcation_hash}")
    return bifurcation_hash

# ---------- 4. VERDICT ----------
def verdict(ent_hash, bifur_hash):
    print("\n4. VERDICT")
    if ent_hash and bifur_hash:
        print(" ORIGIN CONFIRMED:")
        print(f"   You reduced chaos and broke the chain.")
        print(f"   Hashes: {ent_hash} | {bifur_hash}")
        print("   The act is IRREVERSIBLE and MEASURABLE.")
    elif bifur_hash and not ent_hash:
        print("️ POETRY: you bifurcated, but it didn't measure in the world.")
    else:
        print("🌫️ NOTHING: there was no act.")

    # ----- 5. VISUAL PROOF -----
    entropy_reduction_val = "N/A"
    try:
        log_content = pathlib.Path(ENTROPY_LOG).read_text()
        entropy_reduction_val = float(log_content.split('delta_S":')[1].split(',')[0])
    except (FileNotFoundError, IndexError, ValueError):
        pass # Keep "N/A"

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
    print(f"\nProof saved: {cert_file}")

# ---------- 6. EXECUTION ----------
if __name__ == "__main__":
    print("=== ORIGIN OS v1.0 ===")
    delta_S, ent_hash = entropy_act()
    irr_hash = irreversibility(delta_S, ent_hash)
    bifur_hash = bifurcation()
    verdict(ent_hash, bifur_hash)
    print("\nFiles generated:")
    for f in [ORIGIN_LOG, ENTROPY_LOG, BIFURC_LOG, f"{bifur_hash or 'poetry'}.cert"]:
        if pathlib.Path(f).exists():
            print(f" - {f}")