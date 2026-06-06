import os
from io import BytesIO
from datetime import date

import pandas as pd
import plotly.express as px
import streamlit as st

# ------------------------------------------------------------
# Configuración general
# ------------------------------------------------------------
st.set_page_config(
    page_title="Manino Run",
    page_icon="🏃",
    layout="wide",
    initial_sidebar_state="expanded",
)

LOGO_PATH = "assets/logo_manino.png"

# ------------------------------------------------------------
# Paleta Manino
# ------------------------------------------------------------
MANINO_ORANGE = "#D9551A"
ESPRESSO = "#2B1A12"
CREMA = "#FAF6EF"
BEIGE = "#EFE1D0"
BEIGE_2 = "#F6EADD"
OLIVE = "#6E7F4F"
TEXT = "#2A211C"
MUTED = "#73665F"
WHITE = "#FFFFFF"

# ------------------------------------------------------------
# CSS personalizado
# ------------------------------------------------------------
st.markdown(
    f"""
    <style>
        :root {{
            --manino-orange: {MANINO_ORANGE};
            --espresso: {ESPRESSO};
            --crema: {CREMA};
            --beige: {BEIGE};
            --olive: {OLIVE};
            --text: {TEXT};
            --muted: {MUTED};
        }}

        .stApp {{
            background: linear-gradient(180deg, #FFFFFF 0%, #FAF6EF 100%);
            color: var(--text);
        }}

        h1, h2, h3, h4, h5, h6 {{
            color: var(--espresso) !important;
            letter-spacing: -0.02em;
        }}

        p, li, label, span, div {{
            color: var(--text);
        }}

        section[data-testid="stSidebar"] {{
            background: #FFFFFF;
            border-right: 1px solid var(--beige);
        }}

        .hero {{
            background: linear-gradient(135deg, #FFFFFF 0%, #FAF6EF 48%, #F6EADD 100%);
            border: 1px solid var(--beige);
            border-radius: 28px;
            padding: 2rem 2.2rem;
            margin-bottom: 1.2rem;
            box-shadow: 0 18px 50px rgba(43, 26, 18, 0.08);
        }}

        .hero-eyebrow {{
            color: var(--manino-orange) !important;
            font-weight: 800;
            letter-spacing: 0.22em;
            text-transform: uppercase;
            font-size: 0.78rem;
            margin-bottom: 0.4rem;
        }}

        .hero-title {{
            font-size: 3.1rem;
            line-height: 1.02;
            font-weight: 900;
            margin: 0;
            color: var(--espresso) !important;
        }}

        .hero-subtitle {{
            font-size: 1.2rem;
            color: var(--muted) !important;
            margin-top: 0.75rem;
            max-width: 820px;
        }}

        .brand-pill {{
            display: inline-block;
            background: rgba(217, 85, 26, 0.10);
            color: var(--manino-orange) !important;
            border: 1px solid rgba(217, 85, 26, 0.25);
            border-radius: 999px;
            padding: 0.45rem 0.8rem;
            font-size: 0.9rem;
            font-weight: 700;
            margin-top: 1rem;
        }}

        .manino-card {{
            background: #FFFFFF;
            border: 1px solid var(--beige);
            border-radius: 22px;
            padding: 1.25rem;
            min-height: 150px;
            box-shadow: 0 12px 32px rgba(43, 26, 18, 0.06);
            margin-bottom: 1rem;
        }}

        .manino-card h3 {{
            font-size: 1.08rem;
            margin-bottom: 0.4rem;
            color: var(--espresso) !important;
        }}

        .manino-card p {{
            color: var(--muted) !important;
            margin-bottom: 0;
        }}

        .soft-box {{
            background: #FFFFFF;
            border-left: 6px solid var(--manino-orange);
            border-radius: 18px;
            padding: 1rem 1.2rem;
            box-shadow: 0 10px 30px rgba(43, 26, 18, 0.05);
            margin: 0.8rem 0;
        }}

        .warning-box {{
            background: #FFF8F2;
            border: 1px solid #F1CBB4;
            border-left: 6px solid var(--manino-orange);
            border-radius: 18px;
            padding: 1rem 1.2rem;
            margin: 1rem 0;
        }}

        .metric-wrap {{
            background: #FFFFFF;
            border: 1px solid var(--beige);
            border-radius: 20px;
            padding: 1rem;
            text-align: center;
            box-shadow: 0 10px 28px rgba(43, 26, 18, 0.05);
        }}

        .metric-wrap .big {{
            color: var(--manino-orange) !important;
            font-size: 1.9rem;
            font-weight: 900;
            margin: 0;
        }}

        .metric-wrap .label {{
            color: var(--muted) !important;
            font-size: 0.86rem;
            margin: 0;
        }}

        div.stButton > button {{
            background: var(--manino-orange);
            color: white;
            border: 0;
            border-radius: 14px;
            font-weight: 800;
            padding: 0.65rem 1rem;
            box-shadow: 0 8px 18px rgba(217, 85, 26, 0.22);
        }}

        div.stButton > button:hover {{
            background: #B84614;
            color: white;
        }}

        .stDownloadButton button {{
            background: #FFFFFF !important;
            color: var(--espresso) !important;
            border: 1px solid var(--beige) !important;
            border-radius: 14px !important;
            font-weight: 800 !important;
        }}

        [data-testid="stMetricValue"] {{
            color: var(--manino-orange) !important;
        }}

        [data-testid="stMetricLabel"] {{
            color: var(--espresso) !important;
        }}

        .footer {{
            text-align: center;
            color: var(--muted) !important;
            padding: 2rem 0 1rem;
            font-size: 0.9rem;
        }}
    </style>
    """,
    unsafe_allow_html=True,
)

# ------------------------------------------------------------
# Utilidades
# ------------------------------------------------------------
def show_logo(width=260):
    if os.path.exists(LOGO_PATH):
        st.image(LOGO_PATH, width=width)
    else:
        st.markdown("### Manino Run")


def parse_pace_to_seconds(pace_text: str) -> int:
    """Convierte pace mm:ss a segundos por km."""
    try:
        clean = pace_text.strip().replace(" ", "")
        if ":" not in clean:
            minutes = float(clean)
            return int(minutes * 60)
        m, s = clean.split(":", 1)
        return int(m) * 60 + int(s)
    except Exception:
        return 7 * 60


def seconds_to_pace(seconds: float) -> str:
    seconds = max(1, int(round(seconds)))
    m = seconds // 60
    s = seconds % 60
    return f"{m}:{s:02d}"


def pace_range(base_seconds: int, low_delta: int, high_delta: int) -> str:
    return f"{seconds_to_pace(base_seconds + low_delta)}–{seconds_to_pace(base_seconds + high_delta)} min/km"


def distance_label_to_km(label: str, custom_km: float) -> float:
    mapping = {
        "5K": 5.0,
        "10K": 10.0,
        "15K": 15.0,
        "Media maratón 21K": 21.1,
        "Maratón 42K": 42.2,
        "Distancia personalizada": float(custom_km),
    }
    return mapping.get(label, 5.0)


def ideal_weeks(distance_km: float, level: str) -> int:
    if distance_km <= 5:
        base = 8
    elif distance_km <= 10:
        base = 10
    elif distance_km <= 15:
        base = 12
    elif distance_km <= 21.1:
        base = 16
    else:
        base = 24

    if level == "Avanzado":
        return max(6, base - 2)
    if level == "Principiante":
        return base + 2
    return base


def suggested_training_days(distance_km: float, level: str, max_days: int, available_count: int) -> int:
    if level == "Principiante":
        suggested = 3 if distance_km <= 10 else 4
    elif level == "Intermedio":
        suggested = 4 if distance_km <= 21.1 else 5
    else:
        suggested = 5 if distance_km <= 21.1 else 6
    return max(2, min(suggested, max_days, available_count))


def choose_training_days(available_days, run_days_count, can_long_weekend=True, rest_preference=None):
    days = list(available_days)
    if not days:
        return []

    weekend = [d for d in ["Sábado", "Domingo"] if d in days]
    selected = []

    if can_long_weekend and weekend:
        selected.append(weekend[-1])
    else:
        selected.append(days[-1])

    preferred_order = ["Martes", "Jueves", "Lunes", "Miércoles", "Viernes", "Sábado", "Domingo"]
    for d in preferred_order:
        if len(selected) >= run_days_count:
            break
        if d in days and d not in selected and d != rest_preference:
            selected.append(d)

    for d in days:
        if len(selected) >= run_days_count:
            break
        if d not in selected:
            selected.append(d)

    week_order = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    return sorted(selected[:run_days_count], key=week_order.index)


def assign_session_types(training_days, level, week_number):
    n = len(training_days)
    if n == 0:
        return {}

    session_map = {}
    long_day = training_days[-1]

    if n == 2:
        types = ["Carrera suave", "Fondo largo"]
    elif n == 3:
        types = ["Carrera suave", "Tempo run", "Fondo largo"]
    elif n == 4:
        types = ["Recuperación", "Series o intervalos", "Carrera suave", "Fondo largo"]
    else:
        types = ["Recuperación", "Series o intervalos", "Carrera suave", "Tempo run", "Fondo largo"]
        while len(types) < n:
            types.insert(-1, "Carrera suave")

    if level == "Principiante" and week_number <= 3:
        types = ["Caminata/carrera para principiantes" if t in ["Series o intervalos", "Tempo run"] else t for t in types]

    for day, typ in zip(training_days, types[:n]):
        session_map[day] = typ
    session_map[long_day] = "Fondo largo"
    return session_map


def session_distance(total_km, session_type, n_days, distance_km):
    if session_type == "Fondo largo":
        return total_km * (0.36 if distance_km <= 10 else 0.40)
    if session_type == "Series o intervalos":
        return total_km * 0.18
    if session_type == "Tempo run":
        return total_km * 0.20
    if session_type == "Recuperación":
        return total_km * 0.12
    if session_type == "Fuerza complementaria":
        return 0.0
    return total_km * (0.24 if n_days <= 3 else 0.16)


def session_pace(base_pace, session_type, level):
    if session_type == "Fondo largo":
        return pace_range(base_pace, 45, 90)
    if session_type == "Carrera suave":
        return pace_range(base_pace, 60, 105)
    if session_type == "Recuperación":
        return pace_range(base_pace, 90, 135)
    if session_type == "Tempo run":
        return pace_range(base_pace, -15, 20)
    if session_type == "Series o intervalos":
        return pace_range(base_pace, -50, -20)
    if session_type == "Caminata/carrera para principiantes":
        return "Ritmo cómodo + pausas caminando"
    return "Sin pace específico"


def session_objective(session_type):
    objectives = {
        "Carrera suave": "Construir base aeróbica sin acumular fatiga excesiva.",
        "Fondo largo": "Aumentar resistencia y confianza para la distancia objetivo.",
        "Series o intervalos": "Mejorar velocidad, técnica y economía de carrera.",
        "Tempo run": "Sostener un esfuerzo controlado cercano al ritmo objetivo.",
        "Recuperación": "Mover el cuerpo a baja intensidad y facilitar adaptación.",
        "Caminata/carrera para principiantes": "Adaptar articulaciones, respiración y ritmo sin forzar.",
        "Fuerza complementaria": "Fortalecer piernas, core y estabilidad para correr mejor.",
        "Descanso": "Permitir recuperación y reducir riesgo de sobrecarga.",
    }
    return objectives.get(session_type, "Entrenamiento complementario.")


def session_observation(session_type, week, is_deload):
    if is_deload:
        return "Semana de descarga: mantener esfuerzo cómodo y priorizar recuperación."
    obs = {
        "Carrera suave": "Debes poder conversar mientras corres.",
        "Fondo largo": "No busques velocidad; busca constancia y buena sensación.",
        "Series o intervalos": "Calienta bien y evita hacerlas si hay dolor o fatiga alta.",
        "Tempo run": "Esfuerzo firme, pero controlado; no debe sentirse como sprint.",
        "Recuperación": "Muy suave. Si estás cansado, cambia por caminata.",
        "Caminata/carrera para principiantes": "Alterna bloques cortos de trote y caminata según sensaciones.",
    }
    return obs.get(session_type, "Ajusta si aparece dolor persistente o cansancio excesivo.")


def generate_training_plan(user_data):
    distance_km = user_data["distance_km"]
    level = user_data["level"]
    weeks = int(user_data["weeks"])
    available_days = user_data["available_days"]
    max_days = int(user_data["max_days"])
    current_weekly_km = float(user_data["current_weekly_km"])
    current_max_km = float(user_data["current_max_km"])
    max_session_minutes = int(user_data["max_session_minutes"])
    base_pace_seconds = parse_pace_to_seconds(user_data["pace"])
    intensity = user_data["intensity"]
    can_long_weekend = user_data["can_long_weekend"]
    rest_preference = user_data["rest_preference"]

    recommended_weeks = ideal_weeks(distance_km, level)
    training_days_count = suggested_training_days(distance_km, level, max_days, len(available_days))
    training_days = choose_training_days(available_days, training_days_count, can_long_weekend, rest_preference)

    intensity_factor = {"Conservador": 0.85, "Moderado": 1.0, "Exigente": 1.12}.get(intensity, 1.0)
    level_factor = {"Principiante": 0.85, "Intermedio": 1.0, "Avanzado": 1.15}.get(level, 1.0)

    if distance_km <= 5:
        target_peak = 20
    elif distance_km <= 10:
        target_peak = 32
    elif distance_km <= 15:
        target_peak = 42
    elif distance_km <= 21.1:
        target_peak = 52
    else:
        target_peak = 68

    target_peak = target_peak * intensity_factor * level_factor
    start_volume = max(6, min(max(current_weekly_km, current_max_km * 1.6), target_peak * 0.68))

    if level == "Principiante":
        max_growth = 1.08 if intensity == "Conservador" else 1.10
    elif intensity == "Exigente":
        max_growth = 1.12
    else:
        max_growth = 1.10

    rows = []
    weekly_rows = []
    previous_volume = start_volume

    for week in range(1, weeks + 1):
        is_deload = week % 4 == 0 and week != weeks
        if week == 1:
            week_volume = start_volume
        elif is_deload:
            week_volume = previous_volume * 0.82
        else:
            planned = start_volume + (target_peak - start_volume) * ((week - 1) / max(1, weeks - 1))
            week_volume = min(planned, previous_volume * max_growth, target_peak)

        if week == weeks:
            if distance_km <= 10:
                week_volume = max(week_volume * 0.75, distance_km * 1.2)
            else:
                week_volume = week_volume * 0.70

        session_types = assign_session_types(training_days, level, week)
        raw_distances = []
        for day in training_days:
            typ = session_types.get(day, "Carrera suave")
            raw_distances.append(session_distance(week_volume, typ, len(training_days), distance_km))
        total_raw = sum(raw_distances) or 1

        for day, raw_distance in zip(training_days, raw_distances):
            typ = session_types.get(day, "Carrera suave")
            dist = round((raw_distance / total_raw) * week_volume, 1)
            if typ == "Fondo largo":
                dist = max(dist, min(distance_km * 0.55, max(current_max_km, 3)))
            if level == "Principiante" and typ == "Caminata/carrera para principiantes":
                dist = min(dist, max(2.0, current_max_km + week * 0.35))

            pace_text = session_pace(base_pace_seconds, typ, level)
            duration = int(round(dist * base_pace_seconds / 60)) if dist > 0 else 30

            duration_note = ""
            if duration > max_session_minutes and typ != "Fondo largo":
                capped_km = max_session_minutes / (base_pace_seconds / 60)
                dist = round(max(1.0, capped_km), 1)
                duration = max_session_minutes
                duration_note = " Ajustado al tiempo máximo disponible."

            rows.append(
                {
                    "Semana": week,
                    "Día": day,
                    "Tipo de entrenamiento": typ,
                    "Distancia": f"{dist:.1f} km" if dist > 0 else "-",
                    "Distancia_km": dist,
                    "Pace recomendado": pace_text,
                    "Duración estimada": f"{duration} min",
                    "Duración_min": duration,
                    "Objetivo de la sesión": session_objective(typ),
                    "Observaciones": session_observation(typ, week, is_deload) + duration_note,
                }
            )

        actual_week_total = sum(r["Distancia_km"] for r in rows if r["Semana"] == week)
        weekly_rows.append({"Semana": week, "Kilómetros": round(actual_week_total, 1), "Descarga": "Sí" if is_deload else "No"})
        previous_volume = actual_week_total

    plan_df = pd.DataFrame(rows)
    weekly_df = pd.DataFrame(weekly_rows)

    warnings = []
    if weeks < recommended_weeks:
        warnings.append(
            f"Para {distance_km:.1f} km y nivel {level}, se recomiendan aproximadamente {recommended_weeks} semanas. "
            f"Con {weeks} semanas, el plan debe manejarse con enfoque conservador."
        )
    if user_data["injury"] or user_data["medical_condition"]:
        warnings.append("Marcaste lesión o condición médica: consulta con un profesional antes de iniciar o aumentar carga.")
    if distance_km >= 21 and level == "Principiante" and weeks < recommended_weeks:
        warnings.append("La distancia objetivo es exigente para un inicio principiante; considera una meta intermedia o más semanas.")

    diagnostics = {
        "recommended_weeks": recommended_weeks,
        "training_days_count": training_days_count,
        "training_days": training_days,
        "warnings": warnings,
        "peak_week_km": float(weekly_df["Kilómetros"].max()) if not weekly_df.empty else 0,
        "long_day": training_days[-1] if training_days else "No definido",
    }
    return plan_df, weekly_df, diagnostics


def generate_ai_explanation(user_data, diagnostics):
    name = user_data.get("name", "corredor/a") or "corredor/a"
    days = ", ".join(diagnostics.get("training_days", []))
    warnings = diagnostics.get("warnings", [])

    text = f"""
    **{name}, este plan se construyó con una lógica progresiva y segura.**

    Se eligieron **{diagnostics['training_days_count']} días de carrera por semana** porque ese número respeta tu disponibilidad, tu nivel actual y el tiempo máximo que puedes dedicar por sesión. La distribución busca separar los estímulos importantes para evitar esfuerzos intensos en días consecutivos.

    Los días seleccionados fueron: **{days}**. El fondo largo se coloca en **{diagnostics['long_day']}**, porque normalmente es la sesión que requiere más tiempo y debe hacerse con menor presión.

    El volumen semanal sube de forma gradual y cada cuatro semanas se incluye una descarga. Esa descarga reduce la carga para que el cuerpo asimile el trabajo, llegue mejor a las siguientes semanas y disminuya el riesgo de sobrecarga.

    El pace se usa para estimar la duración de cada sesión: distancia × ritmo promedio. Las carreras suaves y fondos largos se programan más lentos que tu pace actual para construir base aeróbica; los trabajos tempo o intervalos se usan con moderación para mejorar ritmo sin promover sobreentrenamiento.

    Si te sientes muy cansado, con dolor persistente o sin buena recuperación, cambia la sesión intensa por carrera suave, caminata o descanso. El plan debe adaptarse a tus sensaciones, no al revés.
    """

    if warnings:
        text += "\n\n**Puntos de atención:**\n" + "\n".join([f"- {w}" for w in warnings])

    # La app queda lista para conectar una API externa en el futuro sin depender de ella.
    # Por seguridad y simplicidad, esta versión genera la explicación con reglas internas.
    return text


def build_text_summary(user_data, plan_df, weekly_df, diagnostics):
    lines = []
    lines.append("MANINO RUN — PLAN DE ENTRENAMIENTO")
    lines.append("Corre con propósito. Entrena con inteligencia.")
    lines.append("")
    lines.append(f"Nombre: {user_data['name']}")
    lines.append(f"Distancia objetivo: {user_data['distance_label']} ({user_data['distance_km']:.1f} km)")
    lines.append(f"Semanas: {user_data['weeks']}")
    lines.append(f"Días de entrenamiento: {', '.join(diagnostics['training_days'])}")
    lines.append(f"Pace actual: {user_data['pace']} min/km")
    lines.append("")
    lines.append("Resumen semanal:")
    for _, row in weekly_df.iterrows():
        lines.append(f"Semana {int(row['Semana'])}: {row['Kilómetros']} km")
    lines.append("")
    lines.append("Plan detallado:")
    export_cols = ["Semana", "Día", "Tipo de entrenamiento", "Distancia", "Pace recomendado", "Duración estimada", "Objetivo de la sesión", "Observaciones"]
    for _, row in plan_df[export_cols].iterrows():
        lines.append(
            f"Semana {row['Semana']} | {row['Día']} | {row['Tipo de entrenamiento']} | {row['Distancia']} | "
            f"{row['Pace recomendado']} | {row['Duración estimada']} | {row['Observaciones']}"
        )
    lines.append("")
    lines.append("Aviso: Este plan es orientativo y no sustituye valoración médica ni acompañamiento profesional.")
    return "\n".join(lines)


def dataframe_to_excel_bytes(plan_df, weekly_df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        plan_df.drop(columns=["Distancia_km", "Duración_min"], errors="ignore").to_excel(writer, index=False, sheet_name="Plan")
        weekly_df.to_excel(writer, index=False, sheet_name="Resumen semanal")
    return output.getvalue()


def render_metric_cards(metrics):
    cols = st.columns(len(metrics))
    for col, (label, value) in zip(cols, metrics):
        with col:
            st.markdown(
                f"""
                <div class="metric-wrap">
                    <p class="big">{value}</p>
                    <p class="label">{label}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

# ------------------------------------------------------------
# Sidebar
# ------------------------------------------------------------
with st.sidebar:
    show_logo(width=190)
    st.markdown("### Manino Run")
    st.caption("Planificador inteligente para preparar tu próxima carrera.")
    st.divider()
    st.markdown("**Frase de marca**")
    st.markdown("Corre con propósito. Entrena con inteligencia.")
    st.divider()
    st.info("Este plan es orientativo. Si tienes lesiones, dolor persistente o condiciones médicas, consulta con un profesional.")

# ------------------------------------------------------------
# Navegación
# ------------------------------------------------------------
tab_inicio, tab_perfil, tab_plan, tab_explicacion, tab_graficos, tab_exportar = st.tabs(
    ["🏠 Inicio", "👤 Perfil del corredor", "📋 Plan generado", "🧠 ¿Por qué este plan?", "📈 Gráficos", "⬇️ Exportar"]
)

# ------------------------------------------------------------
# Inicio
# ------------------------------------------------------------
with tab_inicio:
    col_logo, col_hero = st.columns([1, 3])
    with col_logo:
        show_logo(width=280)
    with col_hero:
        st.markdown(
            """
            <div class="hero">
                <div class="hero-eyebrow">MANINO RUN</div>
                <h1 class="hero-title">Planificador inteligente para preparar tu próxima carrera</h1>
                <p class="hero-subtitle">Una herramienta para convertir tu objetivo de 5K, 10K, 21K o más en un plan semanal claro, progresivo y fácil de seguir.</p>
                <span class="brand-pill">Corre con propósito. Entrena con inteligencia.</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("### ¿Qué hace Manino Run?")
    st.markdown(
        "Manino Run toma tus datos, tu disponibilidad, tu pace actual y la distancia objetivo para construir un plan de entrenamiento progresivo. "
        "El sistema funciona con lógica interna, por lo que no depende de una API externa para generar el plan."
    )

    c1, c2, c3, c4 = st.columns(4)
    cards = [
        ("🏁 Distancias", "Planes para 5K, 10K, 15K, 21K, 42K o una distancia personalizada."),
        ("⏱️ Pace", "El ritmo actual se usa para estimar duración y zonas de entrenamiento."),
        ("📅 Disponibilidad", "El plan se ajusta a los días reales que puedes correr."),
        ("📈 Progresión", "Aumenta volumen con semanas de descarga y enfoque preventivo."),
    ]
    for col, (title, body) in zip([c1, c2, c3, c4], cards):
        with col:
            st.markdown(f"<div class='manino-card'><h3>{title}</h3><p>{body}</p></div>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class="warning-box">
            <strong>Aviso responsable:</strong> Este plan es orientativo y no sustituye una valoración médica ni el acompañamiento de un entrenador profesional. Si aparece dolor persistente, fatiga excesiva o falta de recuperación, baja la carga y consulta con un profesional.
        </div>
        """,
        unsafe_allow_html=True,
    )

# ------------------------------------------------------------
# Perfil
# ------------------------------------------------------------
with tab_perfil:
    st.header("Perfil del corredor")
    st.write("Completa los datos para generar tu plan. Mientras más realistas sean las respuestas, más útil será el resultado.")

    with st.form("runner_form"):
        st.subheader("Datos personales")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            name = st.text_input("Nombre", value="Maximiliano")
        with col2:
            age = st.number_input("Edad", min_value=12, max_value=90, value=30)
        with col3:
            sex = st.selectbox("Sexo, opcional", ["Prefiero no indicar", "Femenino", "Masculino", "Otro"])
        with col4:
            height_cm = st.number_input("Estatura (cm)", min_value=120, max_value=220, value=170)

        col5, col6 = st.columns(2)
        with col5:
            weight_kg = st.number_input("Peso (kg)", min_value=30.0, max_value=180.0, value=70.0, step=0.5)
        with col6:
            strength_training = st.selectbox("¿Entrenas fuerza actualmente?", ["No", "Sí, 1 vez/semana", "Sí, 2 o más veces/semana"])

        st.subheader("Objetivo")
        col1, col2, col3 = st.columns(3)
        with col1:
            distance_label = st.selectbox(
                "Distancia objetivo",
                ["5K", "10K", "15K", "Media maratón 21K", "Maratón 42K", "Distancia personalizada"],
            )
        with col2:
            custom_km = st.number_input("Kilómetros personalizados", min_value=1.0, max_value=100.0, value=8.0, step=0.5, disabled=distance_label != "Distancia personalizada")
        with col3:
            weeks = st.number_input("Semanas disponibles", min_value=4, max_value=36, value=10)

        col4, col5 = st.columns(2)
        with col4:
            race_date = st.date_input("Fecha de carrera, opcional", value=date.today())
        with col5:
            main_goal = st.selectbox("Objetivo principal", ["Terminar la carrera", "Mejorar condición física", "Mejorar tiempo", "Bajar pace", "Preparación recreativa"])

        st.subheader("Nivel actual")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            level = st.selectbox("Nivel de experiencia", ["Principiante", "Intermedio", "Avanzado"])
        with col2:
            current_run_days = st.number_input("Días que corres actualmente/semana", min_value=0, max_value=7, value=2)
        with col3:
            current_max_km = st.number_input("Máximo actual sin detenerte (km)", min_value=0.0, max_value=60.0, value=3.0, step=0.5)
        with col4:
            current_weekly_km = st.number_input("Km aproximados por semana", min_value=0.0, max_value=160.0, value=8.0, step=0.5)

        col5, col6 = st.columns(2)
        with col5:
            pace = st.text_input("Pace actual promedio (min/km)", value="7:00", help="Ejemplo: 6:30 significa 6 minutos y 30 segundos por kilómetro.")
        with col6:
            recent_time = st.text_input("Tiempo reciente 5K o 10K, opcional", value="")

        st.subheader("Disponibilidad")
        available_days = st.multiselect(
            "Días disponibles para entrenar",
            ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"],
            default=["Martes", "Jueves", "Sábado", "Domingo"],
        )
        col1, col2, col3 = st.columns(3)
        with col1:
            max_days = st.number_input("Máximo de días por semana", min_value=2, max_value=7, value=4)
        with col2:
            max_session_minutes = st.number_input("Tiempo máximo por sesión (min)", min_value=20, max_value=240, value=60)
        with col3:
            rest_preference = st.selectbox("Día preferido de descanso", ["Ninguno", "Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"])

        can_long_weekend = st.checkbox("Puedo hacer fondo largo el fin de semana", value=True)

        st.subheader("Condición física y seguridad")
        col1, col2, col3 = st.columns(3)
        with col1:
            injury = st.checkbox("Tengo lesión actual o reciente")
        with col2:
            medical_condition = st.checkbox("Tengo una condición médica relevante")
        with col3:
            intensity = st.selectbox("Tipo de plan", ["Conservador", "Moderado", "Exigente"])

        submitted = st.form_submit_button("Generar plan Manino Run")

    if submitted:
        if len(available_days) < 2:
            st.error("Selecciona al menos 2 días disponibles para poder generar un plan básico.")
        else:
            distance_km = distance_label_to_km(distance_label, custom_km)
            bmi = weight_kg / ((height_cm / 100) ** 2)
            user_data = {
                "name": name,
                "age": int(age),
                "sex": sex,
                "height_cm": height_cm,
                "weight_kg": weight_kg,
                "bmi": bmi,
                "distance_label": distance_label,
                "distance_km": distance_km,
                "weeks": int(weeks),
                "race_date": race_date.isoformat(),
                "main_goal": main_goal,
                "level": level,
                "current_run_days": int(current_run_days),
                "current_max_km": float(current_max_km),
                "current_weekly_km": float(current_weekly_km),
                "pace": pace,
                "recent_time": recent_time,
                "strength_training": strength_training,
                "available_days": available_days,
                "max_days": int(max_days),
                "max_session_minutes": int(max_session_minutes),
                "rest_preference": None if rest_preference == "Ninguno" else rest_preference,
                "can_long_weekend": can_long_weekend,
                "injury": injury,
                "medical_condition": medical_condition,
                "intensity": intensity,
            }
            plan_df, weekly_df, diagnostics = generate_training_plan(user_data)
            st.session_state["user_data"] = user_data
            st.session_state["plan_df"] = plan_df
            st.session_state["weekly_df"] = weekly_df
            st.session_state["diagnostics"] = diagnostics
            st.success("Plan generado. Ve a las pestañas 'Plan generado', 'Gráficos' y 'Exportar'.")

# ------------------------------------------------------------
# Plan generado
# ------------------------------------------------------------
with tab_plan:
    st.header("Plan generado")
    if "plan_df" not in st.session_state:
        st.info("Primero completa el formulario en la pestaña 'Perfil del corredor'.")
    else:
        user_data = st.session_state["user_data"]
        plan_df = st.session_state["plan_df"]
        weekly_df = st.session_state["weekly_df"]
        diagnostics = st.session_state["diagnostics"]

        render_metric_cards(
            [
                ("Distancia objetivo", f"{user_data['distance_km']:.1f} km"),
                ("Semanas", user_data["weeks"]),
                ("Días/semana", diagnostics["training_days_count"]),
                ("Pico semanal", f"{diagnostics['peak_week_km']:.1f} km"),
            ]
        )

        st.subheader("Resumen del corredor")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Nombre", user_data["name"] or "Sin nombre")
            st.metric("Edad", user_data["age"])
        with col2:
            st.metric("IMC técnico", f"{user_data['bmi']:.1f}", help="Dato técnico de referencia. No se usa para juzgar apariencia ni valor personal.")
            st.metric("Nivel", user_data["level"])
        with col3:
            st.metric("Pace actual", f"{user_data['pace']} min/km")
            st.metric("Fondo largo", diagnostics["long_day"])

        if diagnostics["warnings"]:
            for warning in diagnostics["warnings"]:
                st.warning(warning)

        st.markdown(
            f"""
            <div class="soft-box">
                <strong>Diagnóstico inicial:</strong><br>
                Para tu objetivo de <strong>{user_data['distance_km']:.1f} km</strong>, la preparación ideal estimada es de aproximadamente <strong>{diagnostics['recommended_weeks']} semanas</strong>. Tu plan usa <strong>{diagnostics['training_days_count']} días por semana</strong> y una progresión con descargas para favorecer adaptación y recuperación.
            </div>
            """,
            unsafe_allow_html=True,
        )

        display_cols = ["Semana", "Día", "Tipo de entrenamiento", "Distancia", "Pace recomendado", "Duración estimada", "Objetivo de la sesión", "Observaciones"]
        st.dataframe(plan_df[display_cols], use_container_width=True, hide_index=True)

        st.subheader("Resumen semanal")
        st.dataframe(weekly_df, use_container_width=True, hide_index=True)

        st.subheader("Recomendaciones generales")
        st.markdown(
            """
            - Calienta entre 8 y 12 minutos antes de correr: movilidad suave, caminata rápida y trote fácil.
            - Termina con 5 a 10 minutos suaves y respiración controlada.
            - Prioriza sueño y recuperación. Un plan funciona mejor cuando el cuerpo asimila el estímulo.
            - Si aparece dolor persistente, cambia la sesión por descanso y consulta con un profesional.
            - La fuerza complementaria 1 o 2 veces por semana puede ayudar a mejorar estabilidad y reducir sobrecargas.
            """
        )

# ------------------------------------------------------------
# Explicación
# ------------------------------------------------------------
with tab_explicacion:
    st.header("¿Por qué este plan?")
    if "plan_df" not in st.session_state:
        st.info("Primero genera un plan en la pestaña 'Perfil del corredor'.")
    else:
        explanation = generate_ai_explanation(st.session_state["user_data"], st.session_state["diagnostics"])
        st.markdown(explanation)
        st.markdown(
            """
            <div class="warning-box">
                <strong>Importante:</strong> El plan debe ajustarse si aparece fatiga excesiva, dolor persistente o falta de recuperación. Entrenar más no siempre es entrenar mejor.
            </div>
            """,
            unsafe_allow_html=True,
        )

# ------------------------------------------------------------
# Gráficos
# ------------------------------------------------------------
with tab_graficos:
    st.header("Gráficos del plan")
    if "plan_df" not in st.session_state:
        st.info("Primero genera un plan en la pestaña 'Perfil del corredor'.")
    else:
        plan_df = st.session_state["plan_df"]
        weekly_df = st.session_state["weekly_df"]
        user_data = st.session_state["user_data"]

        fig_km = px.line(
            weekly_df,
            x="Semana",
            y="Kilómetros",
            markers=True,
            title="Progresión de kilómetros semanales",
        )
        fig_km.update_traces(line_color=MANINO_ORANGE, marker_color=MANINO_ORANGE)
        fig_km.update_layout(plot_bgcolor=WHITE, paper_bgcolor=WHITE, font_color=TEXT)
        st.plotly_chart(fig_km, use_container_width=True)

        c1, c2 = st.columns(2)
        with c1:
            type_counts = plan_df["Tipo de entrenamiento"].value_counts().reset_index()
            type_counts.columns = ["Tipo", "Sesiones"]
            fig_types = px.pie(type_counts, names="Tipo", values="Sesiones", title="Distribución de tipos de entrenamiento")
            fig_types.update_layout(paper_bgcolor=WHITE, font_color=TEXT)
            st.plotly_chart(fig_types, use_container_width=True)

        with c2:
            duration_week = plan_df.groupby("Semana", as_index=False)["Duración_min"].sum()
            fig_duration = px.bar(duration_week, x="Semana", y="Duración_min", title="Duración estimada por semana")
            fig_duration.update_traces(marker_color=OLIVE)
            fig_duration.update_layout(plot_bgcolor=WHITE, paper_bgcolor=WHITE, font_color=TEXT, yaxis_title="Minutos")
            st.plotly_chart(fig_duration, use_container_width=True)

        comparison = pd.DataFrame(
            {
                "Concepto": ["Volumen actual", "Pico del plan"],
                "Km/semana": [user_data["current_weekly_km"], weekly_df["Kilómetros"].max()],
            }
        )
        fig_compare = px.bar(comparison, x="Concepto", y="Km/semana", title="Comparación entre volumen actual y volumen objetivo del plan")
        fig_compare.update_traces(marker_color=[BEIGE, MANINO_ORANGE])
        fig_compare.update_layout(plot_bgcolor=WHITE, paper_bgcolor=WHITE, font_color=TEXT)
        st.plotly_chart(fig_compare, use_container_width=True)

# ------------------------------------------------------------
# Exportar
# ------------------------------------------------------------
with tab_exportar:
    st.header("Exportar plan")
    if "plan_df" not in st.session_state:
        st.info("Primero genera un plan en la pestaña 'Perfil del corredor'.")
    else:
        user_data = st.session_state["user_data"]
        plan_df = st.session_state["plan_df"]
        weekly_df = st.session_state["weekly_df"]
        diagnostics = st.session_state["diagnostics"]

        export_cols = ["Semana", "Día", "Tipo de entrenamiento", "Distancia", "Pace recomendado", "Duración estimada", "Objetivo de la sesión", "Observaciones"]
        csv_bytes = plan_df[export_cols].to_csv(index=False).encode("utf-8-sig")
        excel_bytes = dataframe_to_excel_bytes(plan_df, weekly_df)
        summary_text = build_text_summary(user_data, plan_df, weekly_df, diagnostics)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.download_button("Descargar CSV", data=csv_bytes, file_name="manino_run_plan.csv", mime="text/csv")
        with col2:
            st.download_button("Descargar Excel", data=excel_bytes, file_name="manino_run_plan.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        with col3:
            st.download_button("Descargar resumen TXT", data=summary_text.encode("utf-8"), file_name="manino_run_resumen.txt", mime="text/plain")

        st.text_area("Resumen para copiar", value=summary_text, height=360)

st.markdown("<div class='footer'>Manino Run · Corre con propósito. Entrena con inteligencia.</div>", unsafe_allow_html=True)
