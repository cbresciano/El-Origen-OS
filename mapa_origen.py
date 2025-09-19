import json
import networkx as nx
import matplotlib.pyplot as plt
from datetime import datetime

# — CONFIGURACIÓN DE FILTROS —
FECHA_MINIMA = "2025-09-01"  # YYYY-MM-DD
ENERGIA_MINIMA = 1e-27        # J/K
TIPO_RUPTURA = None           # Ej: "Fractalismo", "Ontología", "Negentropía"

# — CARGAR Y FILTRAR HUELLAS —
with open("huellas.json", "r", encoding="utf-8") as f:
    huellas = json.load(f)

huellas_filtradas = []
for h in huellas:
    fecha = datetime.fromisoformat(h["timestamp"]).date()
    if fecha < datetime.fromisoformat(FECHA_MINIMA).date():
        continue
    if h["energia_computacional"] < ENERGIA_MINIMA:
        continue
    if TIPO_RUPTURA and h["palabra"].lower() != TIPO_RUPTURA.lower():
        continue
    huellas_filtradas.append(h)

# — CREAR GRAFO —
G = nx.Graph()
for i, h in enumerate(huellas_filtradas):
    label = h['palabra']
    G.add_node(i, label=label, energia=h["energia_computacional"], ruptura=h["palabra"])

# — CONEXIONES POR RUPTURA SEMÁNTICA —
for i in range(len(huellas_filtradas)):
    for j in range(i + 1, len(huellas_filtradas)):
        if huellas_filtradas[i]["palabra"] == huellas_filtradas[j]["palabra"]:
            G.add_edge(i, j)

# — VISUALIZACIÓN —
pos = nx.spring_layout(G, seed=42)
labels = nx.get_node_attributes(G, "label")
energies = nx.get_node_attributes(G, "energia")
colors = [energies[n] * 1e27 for n in G.nodes]

plt.figure(figsize=(12, 8))
nx.draw_networkx_nodes(G, pos, node_color=colors, cmap=plt.cm.inferno, node_size=800)
nx.draw_networkx_edges(G, pos, alpha=0.3)
nx.draw_networkx_labels(G, pos, labels, font_size=10)

plt.title("Mapa de Bifurcaciones: Huellas de Origen Filtradas", fontsize=14)
plt.axis("off")
plt.tight_layout()
plt.show()
