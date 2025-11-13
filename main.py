# ------------------------------------------------------------
# 🧠 CALCULADORA CIENTÍFICA INTELIGENTE
# ------------------------------------------------------------
# Streamlit + Groq + SymPy + Clasificación Automática Total
# Resuelve matemáticas, física, química, estadísticas,
# genera ejercicios, explica, calcula y entiende lenguaje natural.
# ------------------------------------------------------------

import streamlit as st
from groq import Groq
import sympy as sp
import re
import os

# ===========================
# ⚙️ CONFIGURACIÓN GENERAL
# ===========================
ALTURA_CHAT = 600
STREAMING = True
MODELOS = ["llama-3.3-70b-versatile", "llama-3.1-8b-instant"]

# ===========================
# 🎨 INTERFAZ
# ===========================

def configurar_pagina():
    st.set_page_config(page_title="Calculadora Científica IA", page_icon="🧠")
    st.title("🧠 Calculadora Científica Inteligente")

    st.sidebar.title("⚙️ Configuración")
    modelo = st.sidebar.selectbox("Elegí modelo Groq", MODELOS)
    return modelo

def crear_cliente():
    api_key = st.secrets.get("CLAVE_API") or os.getenv("CLAVE_API")

    if not api_key:
        st.error("❌ Falta CLAVE_API en secrets.")
        st.stop()

    try:
        cliente = Groq(api_key=api_key)
        st.sidebar.success("🔗 Conectado a Groq")
        return cliente
    except Exception as e:
        st.error(f"❌ Error conectando a Groq: {e}")
        st.stop()

# --------------------------------------------------------------------
# 🔢 NORMALIZACIÓN ULTRA ROBUSTA (VERSIÓN FINAL – A PRUEBA DE TODO)
# --------------------------------------------------------------------

NUMEROS = {
    "cero": "0", "uno": "1", "una": "1", "dos": "2", "tres": "3",
    "cuatro": "4", "cinco": "5", "seis": "6", "siete": "7",
    "ocho": "8", "nueve": "9", "diez": "10",
}

def reemplazar_numeros_palabras(texto: str) -> str:
    for palabra, digito in NUMEROS.items():
        texto = re.sub(rf"\b{palabra}\b", digito, texto)
    return texto


def normalizar_expresion(texto: str) -> str:
    if not texto:
        return ""

    texto = texto.lower().strip()
    texto = texto.replace(",", ".")

    # 🔥 1 — Eliminación de ruido del lenguaje natural
    frases_ruido = [
        "cuanto es","cuánto es","que es","qué es",
        "cuanto vale","cuánto vale","resultado de",
        "calcula","calcular","resolver","resuelve",
        "por favor","decime","dime",
        "cuanto da","cuánto da","cuanto sería","cuánto sería",
        "el resultado de","la respuesta de",
        "porfa","podrías","quiero saber"
    ]
    for f in frases_ruido:
        texto = texto.replace(f, "")

    # 🔥 2 — Números escritos en palabras
    texto = reemplazar_numeros_palabras(texto)

    # 🔥 3 — Reemplazo inteligente de operadores
    reemplazos = {
        "multiplicado por": "*",
        "multiplicar por": "*",
        "por": "*",
        "x": "*",  # ahora sí seguro

        "dividido por": "/",
        "dividido entre": "/",
        "entre": "/",
        "sobre": "/",

        "elevado a la potencia de": "**",
        "elevado a": "**",
        "a la potencia de": "**",

        "al cuadrado": "**2",
        "al cubo": "**3",

        "raiz cuadrada de": "sqrt(",
        "raíz cuadrada de": "sqrt(",
        "raiz de": "sqrt(",
        "raíz de": "sqrt(",

        "logaritmo de": "log(",
        "log de": "log(",

        "seno de": "sin(",
        "sen de": "sin(",
        "coseno de": "cos(",
        "tangente de": "tan(",

        "pi": "pi",
        "euler": "E",
    }

    # Reemplazar del más largo al más corto
    for k in sorted(reemplazos.keys(), key=len, reverse=True):
        texto = texto.replace(k, reemplazos[k])

    # 🔥 4 — Cerrar paréntesis automáticamente
    if texto.count("(") > texto.count(")"):
        texto += ")"

    # 🔥 5 — Limpiar caracteres inválidos
    texto = re.sub(r"[^0-9A-Za-z\+\-\*\/\^\(\)\.\sEpi]", " ", texto)
    texto = re.sub(r"\s+", " ", texto).strip()

    return texto


# ======================================================
# 🤖 CLASIFICACIÓN AUTOMÁTICA TOTAL (VERSIÓN FINAL PRO)
# ======================================================
def es_expresion_matematica(texto: str) -> bool:
    t = texto.lower()
    normal = normalizar_expresion(texto)

    # Preguntas de creación o descripción → IA
    señales_creación = ["haceme", "hazme", "crea", "inventá", "inventa", "genera", "generá"]
    if any(s in t for s in señales_creación):
        return False

    # Pedidos conceptuales → IA
    señales_teoria = ["explica", "define", "qué significa", "que significa", "por qué"]
    if any(s in t for s in señales_teoria):
        return False

    # Problemas completos → IA
    señales_problemas = ["problema", "ejercicio", "desafío", "dificil", "complicado"]
    if any(s in t for s in señales_problemas):
        return False

    # Si contiene operadores o variables matemáticas → matemáticas
    if re.search(r"[0-9\+\-\*/\^\(\)]", normal):
        return True

    # Funciones matemáticas
    if any(f in normal for f in ["sin", "cos", "tan", "sqrt", "log"]):
        return True

    return False


# ======================================================
# 🧮 RESOLUCIÓN SIMBÓLICA – MÁXIMA ESTABILIDAD
# ======================================================
def resolver_expresion(texto: str):
    try:
        expr = normalizar_expresion(texto)
        simb = sp.sympify(expr)
        resultado = sp.simplify(simb)

        return (
            f"🧮 **Resultado:** {resultado}\n\n"
            f"📘 **Expresión normalizada:** `{expr}`\n"
            f"🔎 **Simplificación:** `{resultado}`"
        )
    except Exception:
        return f"⚠️ No pude resolver la expresión. Intenté: `{texto}`"


# ======================================================
# 🤖 GROQ – IA CIENTÍFICA AVANZADA
# ======================================================
def responder_ia(cliente, modelo, prompt):
    return cliente.chat.completions.create(
        model=modelo,
        messages=[
            {
                "role": "system",
                "content": (
                    "Sos una IA científica experta y universal. "
                    "Podés resolver problemas de matemáticas, física, química, biología, "
                    "estadística, ingeniería, y cualquier ciencia existente o futura. "
                    "Podés también generar ejercicios, resolverlos paso a paso, "
                    "explicar conceptos y analizar situaciones complejas."
                )
            },
            {"role": "user", "content": prompt}
        ],
        stream=STREAMING
    )


def procesar_stream(res):
    texto = ""
    for parte in res:
        if parte.choices[0].delta and parte.choices[0].delta.content:
            frag = parte.choices[0].delta.content
            texto += frag
            yield frag
    return texto


# ===========================
# 💬 HISTORIAL
# ===========================
def iniciar_estado():
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = []

def agregar_msg(rol, contenido, avatar):
    st.session_state.mensajes.append({"role": rol, "content": contenido, "avatar": avatar})

def mostrar_historial():
    for m in st.session_state.mensajes:
        with st.chat_message(m["role"], avatar=m["avatar"]):
            st.markdown(m["content"])


# ===========================
# 🏁 MAIN
# ===========================
def main():
    modelo = configurar_pagina()
    cliente = crear_cliente()
    iniciar_estado()

    cont = st.container(border=True, height=ALTURA_CHAT)
    with cont:
        mostrar_historial()

    prompt = st.chat_input("Escribí tu cálculo o pregunta científica...")

    if prompt:
        agregar_msg("user", prompt, "👤")

        if es_expresion_matematica(prompt):
            # 🧮 Resolver matemáticamente
            resp = resolver_expresion(prompt)
            agregar_msg("assistant", resp, "🤖")
        else:
            # 🤖 Respuesta IA científica
            respuesta = responder_ia(cliente, modelo, prompt)
            with st.chat_message("assistant", avatar="🤖"):
                texto = st.write_stream(procesar_stream(respuesta))
                agregar_msg("assistant", texto, "🤖")

        st.rerun()


if __name__ == "__main__":
    main()



