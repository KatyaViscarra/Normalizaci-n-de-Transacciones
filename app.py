
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
            t["fuente"] for t in validas + invalidas
        ))
    )

    st.divider()

    # Gráficos y estadísticas
    st.subheader("Análisis de transacciones")

    col_grafico1, col_grafico2 = st.columns(2)

    with col_grafico1:
        st.write("**Transacciones por estado**")

        datos_estados = pd.DataFrame(
            list(metricas["conteo_estados"].items()),
            columns=["Estado", "Cantidad"]
        )

        st.bar_chart(
            datos_estados.set_index("Estado")
        )

    with col_grafico2:
        st.write("**Totales netos por moneda**")

        datos_monedas = pd.DataFrame(
            [
                {
                    "Moneda": moneda,
                    "Total": float(total)
                }
                for moneda, total
                in metricas["totales_por_moneda"].items()
            ]
        )

        st.bar_chart(
            datos_monedas.set_index("Moneda")
        )

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

    df_validas = preparar_tabla(validas)
    df_invalidas = preparar_tabla(invalidas)

    # Tablas de resultados
    st.subheader("Detalle de transacciones")

    tab1, tab2 = st.tabs([
        "✅ Transacciones válidas",
        "❌ Transacciones inválidas"
    ])

    with tab1:
        st.write(
            f"Se encontraron {len(validas)} "
            "transacciones válidas."
        )
        st.dataframe(
            df_validas,
            use_container_width=True,
            hide_index=True
        )

    with tab2:
        st.write(
            f"Se encontraron {len(invalidas)} "
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

    df_completo = preparar_tabla(validas + invalidas)

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
