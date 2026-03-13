# jupyter_streamlit

Demos simples de **Streamlit** y **Jupyter** para practicar UI, visualización y carga de datos.

## Contenido de la carpeta

- [app.py](app.py): app mínima de Streamlit (“Hello everyone”) con un `text_input` y un botón.
- [penguins.py](penguins.py): “Penguin Explorer” (Streamlit) que carga [penguins.csv](penguins.csv), filtra por especie y grafica un scatter.
- [copilot.py](copilot.py): mapa de México (Streamlit + PyDeck) con marcadores por estado y población (Censo 2020). Descarga un GeoJSON desde GitHub.
- [penguins.csv](penguins.csv): dataset de pingüinos (incluye valores faltantes en algunas filas).
- [Untitled.ipynb](Untitled.ipynb): notebook de prueba con Pandas/Plotly y un experimento con Gradio.
- [pyproject.toml](pyproject.toml) / [poetry.lock](poetry.lock): configuración y lockfile de dependencias (Poetry).

## Requisitos

- Python 3.12
- [Poetry](https://python-poetry.org/) (recomendado para instalar y ejecutar)

Notas:

- `penguins.py` usa `pandas` y `plotly`.
- `Untitled.ipynb` además prueba `gradio`.

## Instalación

Desde la raíz del proyecto:

```bash
poetry install
```

Si vas a ejecutar el explorer de pingüinos y/o el notebook, instala extras si hiciera falta:

```bash
poetry add plotly gradio
```

## Ejecutar las apps (Streamlit)

Cada app se ejecuta desde la raíz (importante para que encuentre `penguins.csv`):

```bash
poetry run streamlit run app.py
```

```bash
poetry run streamlit run penguins.py
```

```bash
poetry run streamlit run copilot.py
```

Streamlit abrirá el navegador (normalmente en `http://localhost:8501`).

### Notas específicas

- `copilot.py` requiere conexión a internet para descargar el GeoJSON de estados de México.
- Si ves `ModuleNotFoundError: No module named 'plotly'`, instala `plotly` con `poetry add plotly`.

## Ejecutar el notebook (Jupyter)

```bash
poetry run jupyter notebook
```

Luego abre [Untitled.ipynb](Untitled.ipynb) y ejecuta las celdas.

## Estructura rápida del dataset

`penguins.csv` incluye columnas como:

- `species`, `island`, `bill_length_mm`, `bill_depth_mm`, `flipper_length_mm`, `body_mass_g`, `sex`

Algunas filas tienen valores faltantes, así que si haces análisis/modelado conviene limpiar o imputar.
