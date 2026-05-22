import streamlit as st
import pandas as pd
import plotly.express as px

# =========================================
# CONFIGURACION PAGINA
# =========================================
st.set_page_config(
    page_title="Dashboard Avisos de Avería",
    page_icon="📊",
    layout="wide"
)

# =========================================
# TITULO
# =========================================
st.title("📊 Dashboard Avisos de Avería")

st.markdown(
    "Sistema interactivo para análisis de avisos y reportes"
)

# =========================================
# CARGAR EXCEL
# =========================================
archivo = "avisos de averia.xlsx"

# LEER TODAS LAS HOJAS
hojas = pd.read_excel(
    archivo,
    sheet_name=None
)

# =========================================
# SIDEBAR
# =========================================
st.sidebar.title("Configuración")

# SELECCIONAR HOJA
nombre_hoja = st.sidebar.selectbox(
    "Seleccionar hoja Excel",
    list(hojas.keys())
)

# DATAFRAME ACTIVO
DF = hojas[nombre_hoja].copy()

# =========================================
# LIMPIEZA
# =========================================
DF.columns = DF.columns.astype(str)

for col in DF.columns:
    DF[col] = DF[col].astype(str)

# =========================================
# INFORMACION GENERAL
# =========================================
st.subheader("Información General")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Registros",
        len(DF)
    )

with col2:
    st.metric(
        "Total Columnas",
        len(DF.columns)
    )

with col3:
    st.metric(
        "Hoja Activa",
        nombre_hoja
    )

with col4:
    st.metric(
        "Valores Únicos",
        int(DF.nunique().sum())
    )

# =========================================
# BUSCADOR GLOBAL
# =========================================
st.sidebar.subheader("Buscador")

texto_busqueda = st.sidebar.text_input(
    "Buscar cualquier valor"
)

if texto_busqueda:

    DF = DF[
        DF.apply(
            lambda fila:
            fila.astype(str)
            .str.contains(
                texto_busqueda,
                case=False
            )
            .any(),
            axis=1
        )
    ]

# =========================================
# FILTROS DINAMICOS
# =========================================
st.sidebar.subheader("Filtros")

activar_filtro = st.sidebar.checkbox(
    "Activar filtros"
)

if activar_filtro:

    columna_filtro = st.sidebar.selectbox(
        "Seleccionar columna",
        DF.columns
    )

    valores = sorted(
        DF[columna_filtro]
        .dropna()
        .unique()
    )

    seleccion = st.sidebar.multiselect(
        "Seleccionar valores",
        valores
    )

    if seleccion:

        DF = DF[
            DF[columna_filtro]
            .isin(seleccion)
        ]

# =========================================
# TABLA ORIGINAL
# =========================================
st.subheader("Base de Datos")

st.dataframe(
    DF,
    use_container_width=True,
    height=400
)

# =========================================
# AGRUPACION
# =========================================
st.subheader("Agrupación y Conteo")

columna_agrupacion = st.selectbox(
    "Seleccionar columna para agrupar",
    DF.columns
)

agrupado = (
    DF.groupby(columna_agrupacion)
    .size()
    .reset_index(name="Cantidad")
    .sort_values(
        by="Cantidad",
        ascending=False
    )
)

st.dataframe(
    agrupado,
    use_container_width=True
)

# =========================================
# GRAFICA
# =========================================
st.subheader("Gráfica Interactiva")

figura = px.bar(
    agrupado,
    x=columna_agrupacion,
    y="Cantidad",
    title=f"Conteo agrupado por {columna_agrupacion}"
)

st.plotly_chart(
    figura,
    use_container_width=True
)

# =========================================
# EXPORTAR EXCEL
# =========================================
st.subheader("Exportar Información")

nombre_exportacion = "avisos_filtrados.xlsx"

DF.to_excel(
    nombre_exportacion,
    index=False
)

with open(nombre_exportacion, "rb") as archivo_excel:

    st.download_button(
        label="📥 Descargar Excel Filtrado",
        data=archivo_excel,
        file_name=nombre_exportacion,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

# =========================================
# COLUMNAS DISPONIBLES
# =========================================
st.subheader("Columnas Detectadas")

st.write(list(DF.columns))