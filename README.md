# Manino Run

**Manino Run** es una aplicación en Streamlit para crear planes personalizados de entrenamiento para carreras, inspirada visualmente en la marca Manino Coffee.

## Funciones principales

- Registro de perfil del corredor.
- Selección de distancia objetivo: 5K, 10K, 15K, 21K, 42K o personalizada.
- Plan de entrenamiento según nivel, pace y disponibilidad semanal.
- Progresión semanal con semanas de descarga.
- Gráficos con Plotly.
- Exportación a CSV, Excel y TXT.
- Diseño claro con estética Manino.

## Estructura

```text
app.py
requirements.txt
README.md
.streamlit/
    config.toml
assets/
    logo_manino.png
```

## Instalación local

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Despliegue en Streamlit Cloud

1. Sube todos los archivos a GitHub.
2. En Streamlit Cloud, selecciona el repositorio.
3. Define `app.py` como archivo principal.
4. Despliega la app.

## Assets

El logo debe ubicarse en:

```text
assets/logo_manino.png
```

Si el logo no existe, la app sigue funcionando sin errores.

## Aviso responsable

Este plan es orientativo y no sustituye una valoración médica ni el acompañamiento de un entrenador profesional. Si tienes lesiones, dolor persistente o condiciones médicas, consulta con un profesional antes de iniciar o aumentar carga.
