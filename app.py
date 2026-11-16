
import streamlit as st
import pandas as pd
from pathlib import Path

from lector import cargar_transacciones
from normalizador import normalizar_transacciones, cargar_reglas
from validador import validar_transacciones
from metricas import calcular_metricas


# Configuración general
BASE_DIR = Path(__file__).parent

st.set_page_config(
    page_title="Explorador de Transacciones",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Explorador de Transacciones")
st.write(
    "Sistema de normalización, validación y análisis "
    "de transacciones multifuente."
)


# Procesamiento de datos
@st.cache_data
def procesar_datos():
    reglas = cargar_reglas()

    datos_originales = cargar_transacciones(
        str(BASE_DIR / "data" / "transacciones.json")
    )

    normalizadas = normalizar_transacciones(
        datos_originales, reglas
    )

    validas, invalidas = validar_transacciones(
        normalizadas, reglas
    )

    metricas = calcular_metricas(validas, invalidas)

    return validas, invalidas, metricas


try:
    validas, invalidas, metricas = procesar_datos()

        # --- Filtros en la barra lateral ---
    def valor(t, campo):
        return t[campo] or "(sin dato)"

    todas = validas + invalidas
    st.sidebar.header("Filtros")

    def selector(etiqueta, campo):
        opciones = sorted({valor(t, campo) for t in todas})
        return st.sidebar.multiselect(etiqueta, opciones, default=opciones)

    f_fuente = selector("Fuente", "fuente")
    f_moneda = selector("Moneda", "moneda")
    f_estado = selector("Estado", "estado")
    busqueda = st.sidebar.text_input("Buscar por ID o descripción").strip().lower()

    def filtrar(lista):
        return [
            t for t in lista
            if valor(t, "fuente") in f_fuente
            and valor(t, "moneda") in f_moneda
            and valor(t, "estado") in f_estado
            and busqueda in f"{t['id'] or ''} {t['descripcion'] or ''}".lower()
        ]

    validas_f = filtrar(validas)
    invalidas_f = filtrar(invalidas)
    metricas = calcular_metricas(validas_f, invalidas_f)

    # Indicadores principales
    st.subheader("Resumen general")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Procesadas",
        metricas["total_procesadas"]
    )

    col2.metric(
        "Válidas",
        metricas["total_validas"],
        f'{metricas["porcentaje_validas"]}%'
    )

    col3.metric(
        "Inválidas",
        metricas["total_invalidas"],
        f'{metricas["porcentaje_invalidas"]}%'
    )

    col4.metric(
        "Fuentes",
        len(set(
            t["fuente"] for t in validas_f + invalidas_f
        ))
    )

    st.divider()

    # Gráficos y estadísticas
    st.subheader("Análisis de transacciones")

    col_grafico1, col_grafico2 = st.columns(2)

    with col_grafico1:
        st.write("**Transacciones por estado**")

        if metricas["conteo_estados"]:
            datos_estados = pd.DataFrame(
                list(metricas["conteo_estados"].items()),
                columns=["Estado", "Cantidad"]
            )
            st.bar_chart(datos_estados.set_index("Estado"))
        else:
            st.info("Sin datos con los filtros actuales.")

    with col_grafico2:
        st.write("**Totales netos por moneda**")

        if metricas["totales_por_moneda"]:
            datos_monedas = pd.DataFrame(
                [
                    {"Moneda": moneda, "Total": float(total)}
                    for moneda, total
                    in metricas["totales_por_moneda"].items()
                ]
            )
            st.bar_chart(datos_monedas.set_index("Moneda"))
        else:
            st.info("Sin datos con los filtros actuales.")

    st.divider()

    # Preparación de tablas
    def preparar_tabla(transacciones):
        filas = []

        for t in transacciones:
            filas.append({
                "ID": t["id"],
                "Fuente": t["fuente"],
                "Monto": str(t["monto"]),
                "Moneda": t["moneda"],
                "Estado": t["estado"],
                "Fecha": t["fecha"],
                "Descripción": t["descripcion"],
                "Errores": "; ".join(t["errores"])
            })

        return pd.DataFrame(filas)

    df_validas = preparar_tabla(validas_f)
    df_invalidas = preparar_tabla(invalidas_f)

    # Tablas de resultados
    st.subheader("Detalle de transacciones")

    tab1, tab2 = st.tabs([
        "✅ Transacciones válidas",
        "❌ Transacciones inválidas"
    ])

    with tab1:
        st.write(
            f"Se encontraron {len(validas_f)} "
            "transacciones válidas."
        )
        st.dataframe(
            df_validas,
            use_container_width=True,
            hide_index=True
        )

    with tab2:
        st.write(
            f"Se encontraron {len(invalidas_f)} "
            "transacciones inválidas."
        )
        st.dataframe(
            df_invalidas,
            use_container_width=True,
            hide_index=True
        )

    st.divider()

    # Descarga de resultados
    st.subheader("Exportar resultados")

    df_completo = preparar_tabla(validas_f + invalidas_f)

    archivo_csv = df_completo.to_csv(
        index=False
    ).encode("utf-8-sig")

    st.download_button(
        label="📥 Descargar transacciones normalizadas (CSV)",
        data=archivo_csv,
        file_name="transacciones_normalizadas.csv",
        mime="text/csv"
    )

    st.caption(
        "Los registros inválidos se conservan para su revisión. "
        "Los totales monetarios consideran únicamente "
        "transacciones válidas."
    )

except Exception as error:
    st.error(f"Ocurrió un error al procesar los datos: {error}")
    st.info(
        "Verifica que los archivos de configuración y datos "
        "estén en sus respectivas carpetas."
    )
