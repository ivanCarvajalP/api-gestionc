from rdflib import Graph
import os

# Ruta donde el usuario debe colocar su archivo .ttl de Protegé
ONTOLOGY_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "ontologia.ttl")

# Variable global para mantener la gráfica en memoria
_graph = None

def get_semantic_graph() -> Graph:
    """
    Carga la ontología .ttl en memoria solo la primera vez que se llama,
    luego retorna el objeto Graph ya cargado para hacer consultas SPARQL.
    """
    global _graph
    if _graph is None:
        _graph = Graph()
        if os.path.exists(ONTOLOGY_PATH):
            print(f"Cargando ontología desde {ONTOLOGY_PATH}...")
            _graph.parse(ONTOLOGY_PATH, format="turtle")
            print("Ontología cargada exitosamente.")
        else:
            print(f"Advertencia: No se encontró el archivo {ONTOLOGY_PATH}")
    return _graph

def ejecutar_sparql(query: str):
    """
    Ejecuta una consulta SPARQL nativa sobre la ontología y retorna los resultados
    en una lista de diccionarios.
    """
    g = get_semantic_graph()
    resultados = g.query(query)
    
    # Procesar resultados a un formato JSON
    lista_resultados = []
    for fila in resultados:
        fila_dict = {}
        for var in resultados.vars:
            valor = fila[var]
            fila_dict[str(var)] = str(valor) if valor is not None else None
        lista_resultados.append(fila_dict)
        
    return lista_resultados
