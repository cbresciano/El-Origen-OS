#!/usr/bin/env python3
"""
Benford-Fractal SDK v1.0
Genera una distribución de primeros dígitos a partir de actos de origen
y compara contra la Ley de Benford.
No *comprueba* si cumples Benford — *la generas*.
"""
import hashlib, datetime, pathlib, json, collections, math

BENFORD = {1: 0.301, 2: 0.176, 3: 0.125, 4: 0.097, 5: 0.079, 6: 0.067, 7: 0.058, 8: 0.051, 9: 0.046}
ORIGIN_LOG = "origin_acts.log"
BENFORD_RESULT = "benford_fractal.cert"

# ---------- 1. REGISTRA ACTOS DE ORIGEN (fractales por diseño) ----------
def record_origin_act():
    print("\n1. REGISTRA ACTO DE ORIGEN")
    print("Describe el acto que *reconfigura* el sistema (no deducido, no lineal):")
    act = input("> ").strip()
    # convertimos el acto en un número *fractal* usando su hash
    number = int(hashlib.sha256(act.encode()).hexdigest(), 16) % (10**18)  # 18 dígitos
    first_digit = int(str(number)[0])
    entry = {"ts": datetime.datetime.utcnow().isoformat(), "act": act, "number": number, "first_digit": first_digit}
    pathlib.Path(ORIGIN_LOG).write_text(json.dumps(entry) + "\n")
    print(f"✅ Acto registrado. Número fractal: {number} (1er dígito: {first_digit})")
    return first_digit

# ---------- 2. GENERA DISTRIBUCIÓN DE PRIMEROS DÍGITOS ----------
def generate_distribution():
    data = json.loads(pathlib.Path(ORIGIN_LOG).read_text())
    first_digit = data["first_digit"]
    return first_digit

# ---------- 3. COMPARA CONTRA BENFORD ----------
def benford_test(first_digit):
    observed = {d: 0 for d in range(1, 10)}
    observed[first_digit] += 1
    total = 1
    chi2 = sum((observed[d] / total - BENFORD[d]) ** 2 / BENFORD[d] for d in range(1, 10))
    p_value = math.exp(-chi2)  # aproximación rápida
    return chi2, p_value, observed

# ---------- 4. CERTIFICADO BENFORD-FRACTAL ----------
def certificate(chi2, p_value, observed):
    cert = f"""
CERTIFICADO BENFORD-FRACTAL
---------------------------
Fecha: {datetime.datetime.utcnow().isoformat()}
1er dígito observado: {list(observed.keys())[list(observed.values()).index(1)]}
Chi² aproximado: {chi2:.4f}
p-value aproximado: {p_value:.4f}
Ley de Benford: {BENFORD}
Observado: {observed}
---------------------------
Si p-value > 0.05 → tu acto *genera* Benford → *fractal* → *orden superior*.
---------------------------
"""
    pathlib.Path(BENFORD_RESULT).write_text(cert, encoding="utf-8")
    print(f"\nConstancia guardada: {BENFORD_RESULT}")

# ---------- 5. EJECUCIÓN ----------
if __name__ == "__main__":
    print("=== BENFORD-FRACTAL SDK v1.0 ===")
    first_digit = record_origin_act()
    chi2, p_value, observed = benford_test(first_digit)
    certificate(chi2, p_value, observed)
    print("\nResultado:")
    if p_value > 0.05:
        print("🔁 FRACTAL: tu acto *genera* Benford → orden superior.")
    else:
        print("📉 LINEAL: no genera Benford → poesía o azar.")