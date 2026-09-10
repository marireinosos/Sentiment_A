"""
🎭 Análisis de Sentimiento — Edición Creativa
Streamlit + TextBlob + Google Translate

Instalación:
    pip install streamlit textblob pandas Pillow googletrans==4.0.0-rc1

Ejecución:
    streamlit run app.py

Archivos de imagen necesarios en la misma carpeta:
    emoticones.jpg   (banner de cabecera)
    feliz.jpeg       (se muestra si el resultado es positivo)
    neutra.jpg.webp  (se muestra si el resultado es neutral)
    triste.jpg       (se muestra si el resultado es negativo)
"""

import streamlit as st
import pandas as pd
from PIL import Image
from textblob import TextBlob
from googletrans import Translator

# ─────────────────────────────────────────────
# CONFIGURACIÓN
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Análisis de Sentimiento 🎭",
    page_icon="🎭",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# ESTILOS — tema vibrante / glassmorphism emocional
# ─────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap');

    html, body, [class*="css"] { font-family: 'Space Grotesk', sans-serif; }

    @keyframes moodShift {
        0%   { background-position: 0% 50%; }
        50%  { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    .stApp {
        background: linear-gradient(120deg, #1a1440, #3a1c5c, #5c1c6e, #1c3a5c, #1a1440);
        background-size: 400% 400%;
        animation: moodShift 24s ease infinite;
    }

    [data-testid="stSidebar"] {
        background: rgba(20, 14, 45, 0.75) !important;
        backdrop-filter: blur(18px);
        border-right: 1px solid rgba(255,255,255,0.08);
    }
    [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        background: linear-gradient(90deg, #ffb86c, #ff6ec7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
    }
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] li { color: #cdc3ef !important; font-size: 0.88rem !important; }

    h1 {
        background: linear-gradient(90deg, #ffb86c, #ff6ec7 45%, #6ee7ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700 !important;
    }
    h2, h3, h4 { color: #f1edff !important; font-weight: 600 !important; }
    p, li, label, .stMarkdown { color: #d8d0f5 !important; }

    textarea, input[type="text"],
    div[data-baseweb="input"] input,
    div[data-baseweb="textarea"] textarea,
    .stTextInput input {
        background-color: #241a4d !important;
        border: 1px solid rgba(255,255,255,0.18) !important;
        border-radius: 12px !important;
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
        caret-color: #ffffff !important;
        font-size: 1rem !important;
        padding: 10px !important;
    }
    div[data-baseweb="input"], div[data-baseweb="base-input"] {
        background-color: #241a4d !important;
        border-radius: 12px !important;
    }
    textarea:focus, input[type="text"]:focus {
        border-color: #ff6ec7 !important;
        box-shadow: 0 0 0 3px rgba(255,110,199,0.25) !important;
    }
    ::placeholder { color: #a79ad1 !important; opacity: 1 !important; }

    .stButton > button {
        background: linear-gradient(90deg, #ffb86c, #ff6ec7, #6ee7ff) !important;
        background-size: 200% auto !important;
        color: #1a1440 !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        padding: 0.55rem 1.2rem !important;
        box-shadow: 0 4px 20px rgba(255,110,199,0.35) !important;
        transition: all 0.3s ease !important;
    }
    .stButton > button:hover {
        background-position: right center !important;
        box-shadow: 0 6px 26px rgba(110,231,255,0.5) !important;
        transform: translateY(-2px) !important;
    }

    [data-testid="metric-container"] {
        background: rgba(255,255,255,0.06);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.14);
        border-top: 3px solid transparent;
        border-image: linear-gradient(90deg, #ffb86c, #ff6ec7) 1;
        border-radius: 14px;
        padding: 16px 20px;
    }
    [data-testid="metric-container"] label { color: #b7acdf !important; font-size: 0.75rem !important; text-transform: uppercase; }
    [data-testid="metric-container"] [data-testid="stMetricValue"] { color: #ffffff !important; font-weight: 700 !important; }

    .header-card {
        background: rgba(255,255,255,0.06);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(255,255,255,0.15);
        border-radius: 20px;
        padding: 28px 34px;
        margin-bottom: 22px;
        box-shadow: 0 8px 40px rgba(90,30,120,0.35);
        display: flex;
        align-items: center;
        gap: 26px;
    }

    .glass-card {
        background: rgba(255,255,255,0.06);
        backdrop-filter: blur(14px);
        border: 1px solid rgba(255,255,255,0.14);
        border-radius: 18px;
        padding: 24px 28px;
        margin-bottom: 18px;
        box-shadow: 0 6px 28px rgba(0,0,0,0.25);
    }

    /* Medidores tipo gauge */
    .gauge-label { display:flex; justify-content:space-between; font-size:0.85rem; color:#cdc3ef; margin-bottom:4px; }
    .gauge-track { width:100%; height:16px; background:rgba(255,255,255,0.08); border-radius:10px; overflow:hidden; border:1px solid rgba(255,255,255,0.12); }
    .gauge-fill { height:100%; border-radius:10px; transition: width 0.6s ease; }

    .emo-bar-row { display:flex; align-items:center; gap:12px; padding:6px 12px; margin:4px 0;
                   background: rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.08); border-radius:10px; }
    .emo-fill { height:10px; border-radius:6px; }

    .result-tag {
        display:inline-block; padding:6px 18px; border-radius:20px; font-weight:700; font-size:1rem;
        box-shadow: 0 0 22px currentColor;
    }

    .emo-image-frame {
        border-radius: 20px; padding: 6px; display:inline-block;
        box-shadow: 0 0 34px currentColor;
    }

    div[data-testid="stExpander"] { border: 1px solid rgba(255,255,255,0.14) !important; border-radius: 14px !important; background: rgba(255,255,255,0.05) !important; }
    hr { border-color: rgba(255,255,255,0.12) !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# LÉXICO simple para el "detector de emociones" extra
# ─────────────────────────────────────────────
LEXICO_EMOCIONES = {
    "😄 Alegría":  ["feliz","alegre","content","genial","excelente","maravilloso","bien","amor",
                    "increíble","fantástico","bueno","éxito","sonrisa","encanta","gusta","hermoso",
                    "amo","disfruto","divertido","emocionado"],
    "😢 Tristeza": ["triste","mal","dolor","llorar","pena","decepcionado","solo","perdida","fracaso",
                    "deprimido","desanimado","lamento","extraño","sufro"],
    "😠 Enojo":    ["enojado","furioso","odio","rabia","molesto","indignado","irritado","harto",
                    "detesto","fastidioso"],
    "😨 Miedo":    ["miedo","temor","asustado","terror","pánico","nervioso","preocupado","ansioso"],
    "😲 Sorpresa": ["sorprendido","increíble","wow","inesperado","asombrado","impresionante","vaya"],
}

def detectar_emociones(texto):
    texto_l = texto.lower()
    conteo = {}
    for emocion, palabras in LEXICO_EMOCIONES.items():
        c = sum(texto_l.count(p) for p in palabras)
        conteo[emocion] = c
    return conteo


def clasificar_sentimiento(polaridad):
    if polaridad > 0.05:
        return "Positivo", "😊", "#4ade80", ["feliz.jpg", "feliz.jpeg", "feliz.png"]
    elif polaridad < -0.05:
        return "Negativo", "😔", "#f87171", ["triste.jpg", "triste.jpeg", "triste.png"]
    else:
        return "Neutral", "😐", "#94a3b8", ["neutro.jpg", "neutra.jpg", "neutra.jpg.webp", "neutro.png"]


def abrir_primera_imagen(nombres_posibles):
    for nombre in nombres_posibles:
        try:
            return Image.open(nombre)
        except FileNotFoundError:
            continue
    return None


def render_gauge(etiqueta, valor, minimo, maximo, color):
    pct = (valor - minimo) / (maximo - minimo) * 100
    pct = max(0, min(100, pct))
    st.markdown(f"""
    <div style="margin-bottom:14px;">
        <div class="gauge-label"><span>{etiqueta}</span><span style="color:{color}; font-weight:700;">{valor:.2f}</span></div>
        <div class="gauge-track">
            <div class="gauge-fill" style="width:{pct}%; background:linear-gradient(90deg, {color}aa, {color}); box-shadow:0 0 14px {color};"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_emo_bars(conteo):
    maximo = max(conteo.values()) if conteo.values() else 0
    colores = {"😄 Alegría": "#4ade80", "😢 Tristeza": "#60a5fa", "😠 Enojo": "#f87171",
               "😨 Miedo": "#c084fc", "😲 Sorpresa": "#fbbf24"}
    if maximo == 0:
        st.caption("No se detectaron palabras clave de emociones específicas en el texto.")
        return
    for emocion, valor in conteo.items():
        ancho = max(6, int((valor / maximo) * 220)) if maximo > 0 else 6
        color = colores.get(emocion, "#a78bfa")
        st.markdown(
            f'<div class="emo-bar-row">'
            f'<span style="min-width:120px; font-size:0.9rem;">{emocion}</span>'
            f'<div class="emo-fill" style="width:{ancho}px; background:{color}; box-shadow:0 0 10px {color};"></div>'
            f'<span style="font-family:\'IBM Plex Mono\',monospace; font-size:0.85rem; color:#d8d0f5;">{valor}</span>'
            f'</div>', unsafe_allow_html=True,
        )


translator = Translator()

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.subheader("🧭 Polaridad y Subjetividad")
    st.markdown("""
    **Polaridad:** indica si el sentimiento expresado en el texto es positivo, negativo o neutral.
    Su valor oscila entre **-1** (muy negativo) y **1** (muy positivo), con **0** como sentimiento neutral.

    **Subjetividad:** mide cuánto del contenido es subjetivo (opiniones, emociones, creencias)
    frente a objetivo (hechos). Va de **0** (completamente objetivo) a **1** (completamente subjetivo).
    """)
    st.divider()
    st.subheader("🎭 Detector de emociones")
    st.markdown("""
    Además de la polaridad, esta versión busca palabras clave en el texto para estimar
    qué tan presentes están la **alegría, tristeza, enojo, miedo y sorpresa**.
    """)
    st.divider()
    st.caption("Hecho con TextBlob + Google Translate 🌐")

# ─────────────────────────────────────────────
# ENCABEZADO
# ─────────────────────────────────────────────
col_img, col_titulo = st.columns([1, 4])
st.markdown('<div class="header-card">', unsafe_allow_html=True)
c1, c2 = st.columns([1, 4])
with c1:
    try:
        image = Image.open("emoticones.jpg")
        st.image(image, width=110)
    except FileNotFoundError:
        st.markdown("🎭", unsafe_allow_html=True)
with c2:
    st.markdown("<h1 style='margin:0; font-size:2.2rem;'>Análisis de Sentimiento</h1>", unsafe_allow_html=True)
    st.markdown("<p style='margin:6px 0 0 0;'>Escribe una frase y descubre su carga emocional, palabra por palabra ✨</p>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# EJEMPLOS RÁPIDOS
# ─────────────────────────────────────────────
if "frase" not in st.session_state:
    st.session_state.frase = ""
if "historial" not in st.session_state:
    st.session_state.historial = []

st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.markdown("#### ⚡ Prueba con un ejemplo o escribe tu propia frase")

ejemplos = {
    "😄 Positivo": "¡Hoy fue un día maravilloso, me siento muy feliz y agradecido!",
    "😔 Negativo": "Estoy muy triste y decepcionado, nada me ha salido bien hoy.",
    "😐 Neutral":  "La reunión está programada para las tres de la tarde en la oficina.",
}
cols_ej = st.columns(len(ejemplos))
for col, (nombre, frase_ej) in zip(cols_ej, ejemplos.items()):
    if col.button(nombre, use_container_width=True):
        st.session_state.frase = frase_ej
        st.session_state.trigger_analisis = True
        st.rerun()

text = st.text_input("Escribe la frase que deseas analizar:", key="frase",
                      placeholder="Ej: Hoy me siento súper contento con mi proyecto")
analizar = st.button("🔮 Analizar sentimiento", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

if "trigger_analisis" not in st.session_state:
    st.session_state.trigger_analisis = False
if analizar:
    st.session_state.trigger_analisis = True

# ─────────────────────────────────────────────
# ANÁLISIS — solo corre al presionar el botón (o al elegir un ejemplo)
# ─────────────────────────────────────────────
if st.session_state.trigger_analisis and text.strip():
    try:
        translation = translator.translate(text, src="es", dest="en")
        trans_text = translation.text
    except Exception:
        trans_text = text  # si falla el traductor, se analiza el texto tal cual

    blob = TextBlob(trans_text)
    polaridad = round(blob.sentiment.polarity, 2)
    subjetividad = round(blob.sentiment.subjectivity, 2)

    etiqueta, emoji_resultado, color, nombres_img = clasificar_sentimiento(polaridad)
    conteo_emociones = detectar_emociones(text)

    # Guardar en historial solo si es un análisis nuevo
    ultimo = st.session_state.historial[-1] if st.session_state.historial else None
    if ultimo is None or ultimo["Frase"] != text:
        st.session_state.historial.append({
            "Frase": text, "Polaridad": polaridad, "Subjetividad": subjetividad, "Resultado": etiqueta,
        })

    st.markdown("<br>", unsafe_allow_html=True)
    col_izq, col_der = st.columns([1, 2], gap="large")

    with col_izq:
        st.markdown('<div class="glass-card" style="text-align:center;">', unsafe_allow_html=True)
        st.markdown(f'<div class="emo-image-frame" style="color:{color};">', unsafe_allow_html=True)
        img_resultado = abrir_primera_imagen(nombres_img)
        if img_resultado is not None:
            st.image(img_resultado, use_container_width=True)
        else:
            st.markdown(f"<div style='font-size:5rem;'>{emoji_resultado}</div>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown(
            f'<div style="margin-top:14px;"><span class="result-tag" style="background:{color}22; color:{color};">'
            f'{emoji_resultado} Sentimiento {etiqueta}</span></div>',
            unsafe_allow_html=True,
        )
        st.markdown('</div>', unsafe_allow_html=True)

    with col_der:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("#### 📊 Medidores")
        render_gauge("Polaridad", polaridad, -1, 1, color)
        render_gauge("Subjetividad", subjetividad, 0, 1, "#a78bfa")

        m1, m2 = st.columns(2)
        m1.metric("Palabras", len(text.split()))
        m2.metric("Caracteres", len(text))

        st.markdown("#### 🎭 Detector de emociones por palabras clave")
        render_emo_bars(conteo_emociones)
        st.markdown('</div>', unsafe_allow_html=True)

    # Efectos sorpresa para el toque "wow"
    if polaridad > 0.6:
        st.balloons()
    elif polaridad < -0.6:
        st.snow()

# ─────────────────────────────────────────────
# HISTORIAL DE LA SESIÓN
# ─────────────────────────────────────────────
if st.session_state.historial:
    st.divider()
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("#### 🕓 Historial de frases analizadas en esta sesión")
    df_historial = pd.DataFrame(st.session_state.historial)
    st.dataframe(
        df_historial.style.background_gradient(subset=["Polaridad"], cmap="RdYlGn", vmin=-1, vmax=1),
        use_container_width=True,
    )
    csv_hist = df_historial.to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Descargar historial (.csv)", data=csv_hist,
                        file_name="historial_sentimiento.csv", mime="text/csv")
    if st.button("🗑️ Borrar historial"):
        st.session_state.historial = []
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
