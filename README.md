# Sistema de Normalización y Exploración de Transacciones Multifuente

**Programa:** AI Devs Jr. – Kodigo  
**Participante:** Katya Ivonne Viscarra Portillo  
**Proyecto académico:** Normalización y Exploración de Transacciones Multifuente

---

## 1. Descripción del proyecto

Este proyecto consiste en una aplicación desarrollada en Python para leer, normalizar, validar y analizar transacciones provenientes de diferentes fuentes de información: PayPal, Stripe y registros bancarios.

Su propósito es unificar estructuras de datos heterogéneas en un esquema común, identificar registros inválidos sin descartarlos y generar métricas que faciliten la exploración de la información.

La aplicación cuenta con una interfaz interactiva desarrollada con Streamlit, que permite visualizar estadísticas, consultar registros y descargar los resultados procesados.

## 2. Tecnologías utilizadas

- **Python 3.12:** lenguaje principal de desarrollo.
- **Streamlit:** creación de la interfaz web interactiva.
- **Pandas:** organización y presentación de los datos.

## 3. Estructura del proyecto

```text
normalizacion_transacciones/
│
├── app.py
├── lector.py
├── normalizador.py
├── validador.py
├── metricas.py
├── requirements.txt
│
├── config/
│   └── reglas.json
│
├── data/
│   └── transacciones.json
│
├── README.md
└── nota_tecnica.md
```

### Descripción de los módulos

- **app.py:** administra la interfaz gráfica y presenta los resultados mediante indicadores, gráficos, tablas y opciones de descarga.
- **lector.py:** lee los registros desde el archivo JSON y controla errores de lectura y formato.
- **normalizador.py:** identifica la fuente de cada transacción y transforma sus campos al esquema unificado.
- **validador.py:** verifica los campos obligatorios, monedas, montos, estados y fechas. Clasifica los registros como válidos o inválidos.
- **metricas.py:** calcula estadísticas generales, distribución por estado y totales netos por moneda.
- **config/reglas.json:** contiene las reglas de normalización y validación.
- **data/transacciones.json:** contiene los datos de prueba de las tres fuentes.
- **requirements.txt:** especifica las dependencias necesarias para ejecutar el proyecto.

## 4. Esquema de datos unificado

Todas las transacciones se convierten a una estructura común con los siguientes campos:

| Campo | Descripción |
|---|---|
| id | Identificador de la transacción |
| fuente | Sistema de origen |
| monto | Valor numérico de la operación |
| moneda | Código de moneda |
| estado | Estado normalizado |
| fecha | Fecha en formato YYYY-MM-DD |
| descripcion | Descripción de la operación |
| valida | Resultado de la validación |
| errores | Lista de inconsistencias detectadas |
| raw_data | Registro original de la fuente |

## 5. Reglas principales de normalización y validación

- Fuentes admitidas: PayPal, Stripe y banco.
- Monedas admitidas: USD, EUR, MXN y COP.
- Los estados originales se convierten a categorías comunes: completada, pendiente, fallida, cancelada y reembolsada.
- Las fechas se convierten al formato YYYY-MM-DD.
- Los montos deben ser numéricos y diferentes de cero.
- Se permiten montos negativos para representar reembolsos o ajustes.
- No se realiza conversión entre monedas.
- Los registros inválidos se conservan y se acompañan de sus respectivos mensajes de error.
- Los totales monetarios se calculan únicamente con transacciones válidas.

## 6. Instalación y ejecución

### Requisitos previos

- Python 3.12.
- Conexión a Internet para instalar las dependencias.

### Crear el entorno virtual

Desde la carpeta principal del proyecto, ejecutar:

```bash
py -3.12 -m venv venv
```

### Activar el entorno virtual en Windows CMD

```cmd
venv\Scripts\activate.bat
```

### Instalar las dependencias

```bash
python -m pip install -r requirements.txt
```

### Ejecutar la aplicación

```bash
python -m streamlit run app.py
```

La aplicación estará disponible en el navegador, normalmente en:

`http://localhost:8501`

## 7. Resultados de las pruebas

Se realizaron pruebas con 15 transacciones distribuidas entre las tres fuentes de información.

| Indicador | Resultado |
|---|---:|
| Transacciones procesadas | 15 |
| Transacciones válidas | 9 |
| Transacciones inválidas | 6 |
| Porcentaje de válidas | 60 % |
| Porcentaje de inválidas | 40 % |

Las pruebas permitieron comprobar la detección de:

- Montos iguales a cero.
- Monedas no soportadas.
- Montos no numéricos.
- Estados desconocidos.
- Fechas inválidas.
- Identificadores faltantes.

También se verificó la generación de gráficos, visualización de registros y exportación de resultados en formato CSV.

## 8. Consideraciones finales

Los registros inválidos no se eliminan, ya que conservarlos permite identificar problemas en las fuentes de información y facilita su revisión posterior.

Los importes se mantienen en sus monedas originales. Por lo tanto, los totales de cada moneda se presentan de forma independiente y no deben interpretarse como un total monetario combinado.

## 9. Clonar el repositorio desde GitHub

Para obtener una copia local del proyecto, sigue estos pasos:

### Requisitos previos

- Tener instalado Git.
- Tener instalado Python 3.12.
- Contar con conexión a Internet.

### 1. Clonar el repositorio

Abrir una terminal y ejecutar:

```bash
git clone https://github.com/KatyaViscarra/Normalizaci-n-de-Transacciones.git
```

### 2. Ingresar a la carpeta del proyecto

```bash
cd Normalizaci-n-de-Transacciones
```

### 3. Crear el entorno virtual

```bash
py -3.12 -m venv venv
```

### 4. Activar el entorno virtual

En Windows CMD:

```cmd
venv\Scripts\activate.bat
```

### 5. Instalar las dependencias

```bash
python -m pip install -r requirements.txt
```

### 6. Ejecutar la aplicación

```bash
python -m streamlit run app.py
```

La aplicación se abrirá en el navegador, normalmente en:

`http://localhost:8501`


