"""
Ejercicio 1: Superpoderes y Personalización del Agente
Autores: Angie Yesenia Giraldo Gavilan, Cesar Augusto Florez Castaño, Jhonatan Rojas Diaz
"""

#librerias necesarias para las herramientas y la interfaz

import random
import requests
from smolagents import CodeAgent, HfApiModel, tool, FinalAnswerTool
import gradio as gr
import math


#Herramienta 1: Calculadora de áreas de figuras geométricas
@tool
def calcular_area(figura: str, valor1: float, valor2: float = 0) -> str: #Se crea función para calcular el área de diferentes figuras geométricas con dos valores.
    
    #Instrucciones para el agente sobre la herramienta de calcular áreas.
    
    """
    Calcula el área de una figura geométrica.

    Args:
        figura: Nombre de la figura. Puede ser 'rectangulo', 'triangulo' o 'circulo'.
        valor1: Para rectángulo y triángulo es la base. Para círculo es el radio.
        valor2: Para rectángulo es la altura. Para triángulo es la altura. No aplica al círculo.

    Returns:
        Un string con el resultado del área calculada.
    """
    figura = figura.lower() # Convertimos el nombre de la figura a minúsculas para evitar problemas de mayúsculas y minúsculas
    
    if figura == "rectangulo":
        area = valor1 * valor2 # Para el rectángulo, el área se calcula multiplicando la base (valor1) por la altura (valor2)
        return f"El área del rectángulo con base {valor1} y altura {valor2} es: {area:.2f}"

    elif figura == "triangulo":
        area = (valor1 * valor2) / 2 # Para el triángulo, el área se calcula multiplicando la base (valor1) por la altura (valor2) y dividiendo entre 2
        return f"El área del triángulo con base {valor1} y altura {valor2} es: {area:.2f}"

    elif figura == "circulo":
        area = math.pi * (valor1 ** 2) # Para el círculo, el área se calcula multiplicando pi por el radio (valor1) al cuadrado
        return f"El área del círculo con radio {valor1} es: {area:.2f}"

    else:
        return f"Figura '{figura}' no reconocida. Usa: rectangulo, triangulo o circulo."


#herramienta 2: Obtener el clima de una ciudad usando la API gratuita de wttr.in
@tool
def obtener_clima(ciudad: str) -> str: #Función para obtener el clima actual de una ciudad usando la API gratuita de wttr.in.
    
    #Instrucciones para el agente sobre la herramienta de obtener clima.
    
    """
    Obtiene el clima actual de una ciudad usando la API gratuita de wttr.in.

    Args:
        ciudad: Nombre de la ciudad en español o inglés (ej: 'Medellin', 'Bogota', 'London').

    Returns:
        Un string con la información del clima actual de la ciudad.
    """
    try:
        # wttr.in es una API pública y gratuita, no requiere clave
        url = f"https://wttr.in/{ciudad}?format=3&lang=es"
        response = requests.get(url, timeout=5)

        if response.status_code == 200:
            return f"🌤️ Clima en {ciudad}: {response.text.strip()}" #Buca en la API la ciudad y retorna el resultado con la estructura definida
        else:
            return f"No pude obtener el clima de {ciudad}. Intenta con otro nombre de ciudad."

    except Exception as e:
        return f"Error al consultar el clima: {str(e)}" #En caso de error en la consulta, se captura la excepción y se devuelve un mensaje de error con la descripción del problema.


#modificamos el FinalAnswerTool para personalizar la respuesta final del agente personalizada

class MiFinalAnswerTool(FinalAnswerTool):

    #Instrcciones para el agente sobre la herramienta de respuesta final personalizada.

    """
    Versión personalizada del FinalAnswerTool.
    Agrega un prefijo, firma y conteo de caracteres a cada respuesta.
    """

    # Sobrescribimos el método forward que es el que genera la respuesta
    def forward(self, answer: str) -> str:
        #Contamos cuántos caracteres tiene la respuesta original
        num_caracteres = len(answer)

        #Construimos la respuesta con prefijo, contenido y firma
        respuesta_formateada = (
            f"🤖 Agente dice:\n\n"          # Prefijo con emoji
            f"{answer}\n\n"                  # Respuesta original del agente
            f"Esta respuesta tiene {num_caracteres} caracteres.\n"  # Conteo de caracteres
            f"--- Procesado por Angie, Cesar y Jhonatan ---"           # Firma del equipo
        )

        return respuesta_formateada


#Configuramos el agente con las herramientas personalizadas.
# Modelo que usará el agente (gratuito en HF Spaces)
modelo = HfApiModel(model_id="Qwen/Qwen2.5-Coder-32B-Instruct")

# Creamos el agente con las herramientas personalizadas
agente = CodeAgent(
    tools=[
        calcular_area,       # Herramienta 1: Calculador de áreas
        obtener_clima,       # Herramienta 2: Clima con API
        MiFinalAnswerTool(), # FinalAnswerTool modificado
    ],
    model=modelo,
    max_steps=5,
)


#Función para responder preguntas usando el agente
def responder(pregunta):
    resultado = agente.run(pregunta) #El agente procesa la pregunta, decide qué herramientas usar y genera una respuesta.
    return resultado

interfaz = gr.Interface( #Se crea la interfaz de usuario con Gradio, donde el usuario puede ingresar una pregunta y obtener la respuesta del agente.
    fn=responder,
    inputs=gr.Textbox(
        label="¿Qué quieres preguntarle al agente?",
        placeholder="Ej: ¿Cuál es el área de un rectángulo de base 5 y altura 3?"
    ),
    outputs=gr.Textbox(label="Respuesta del Agente"),
    title="🤖 Agente Inteligente - Ejercicio 1",
    description=(
        "Agente con superpoderes:\n"
        "Puede calcular áreas de figuras geométricas\n"
        "Puede consultar el clima de cualquier ciudad\n\n"
        "Autores: Angie Giraldo | Cesar Florez | Jhonatan Rojas"
    ),
    examples=[
        ["¿Cuál es el área de un triángulo con base 6 y altura 4?"],
        ["¿Qué clima hace hoy en Medellín?"],
        ["Calcula el área de un círculo con radio 7"],
        ["¿Cómo está el tiempo en Bogotá?"],
    ]
)

if __name__ == "__main__":
    interfaz.launch()
