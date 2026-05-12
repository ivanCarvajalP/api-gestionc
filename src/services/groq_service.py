
import re
from groq import Groq
from src.core.config import settings

client = Groq(
    api_key=settings.GROQ_API_KEY,
)


def valid_products(products: list) -> list:
    """Filtra productos válidos para vehículos en una sola petición a Groq.

    Envía todos los productos como una lista numerada y recibe los índices
    de aquellos que son repuestos, accesorios o servicios válidos para un vehículo.
    """
    if not products:
        return []

    # Construir lista numerada de descripciones
    product_list = "\n".join(
        f"{i+1}. {p['descripcion']}" for i, p in enumerate(products)
    )

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": (
                    "Eres un clasificador estricto que determina si un producto "
                    "corresponde a un repuesto, accesorio o servicio válido para un vehículo. "
                    "Se te dará una lista numerada de productos. "
                    "Tu respuesta DEBE SER ÚNICAMENTE los números de los productos válidos, "
                    "separados por comas. Si ninguno es válido, responde 'ninguno'. "
                    "No agregues explicaciones, puntos finales, ni texto adicional. "
                    "Ejemplo de respuesta: 1,3,5"
                ),
            },
            {
                "role": "user",
                "content": f"Productos:\n{product_list}",
            },
        ],
        model="llama-3.3-70b-versatile",
        temperature=0.0,
    )

    answer = chat_completion.choices[0].message.content.strip().lower()

    if answer == "ninguno" or not answer:
        return []

    # Extraer todos los números de la respuesta
    valid_indices = set()
    for num_str in re.findall(r"\d+", answer):
        idx = int(num_str)
        if 1 <= idx <= len(products):
            valid_indices.add(idx)

    return [products[i - 1] for i in sorted(valid_indices)]