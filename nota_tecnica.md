# Nota técnica: Normalización y Exploración de Transacciones Multifuente

## 1. Diseño del esquema unificado

Se implementó un esquema común para integrar transacciones provenientes de tres fuentes: PayPal, Stripe y registros bancarios. Los datos se transforman a una estructura estandarizada que contiene identificador, fuente, monto, moneda, estado, fecha, descripción, indicador de validez y motivos de error.

Se incorporó el campo `raw_data` para conservar el registro original y facilitar su trazabilidad.

## 2. Criterios de normalización

Se establecieron las siguientes reglas:

- **Monedas:** se admiten USD, EUR, MXN y COP. No se realizan conversiones entre monedas.
- **Estados:** se unifican las distintas denominaciones de cada fuente en estados comunes: completada, pendiente, fallida, cancelada y reembolsada.
- **Fechas:** se aceptan distintos formatos de entrada y se estandarizan como `YYYY-MM-DD`.
- **Montos:** se utiliza `Decimal` para evitar imprecisiones en operaciones monetarias. Se permiten montos negativos para representar reembolsos o ajustes, pero no montos iguales a cero.

## 3. Validación y tratamiento de errores

Se verifican los identificadores, fuentes, montos, monedas, estados y fechas. Cuando un registro incumple alguna regla, se marca como inválido (`valida = False`) y se almacena el motivo correspondiente en el campo `errores`.

Se decidió conservar los registros inválidos en lugar de descartarlos, permitiendo identificar problemas en los datos de origen y mantener la trazabilidad del proceso.

## 4. Métricas y resultados

Las métricas consideran el total de registros procesados, válidos e inválidos, sus porcentajes, el conteo por estado y los totales monetarios por moneda. Los totales se calculan únicamente con transacciones válidas y mantienen los montos negativos, por lo que representan saldos netos por moneda, sin conversión cambiaria.

En las pruebas realizadas con 15 registros, se obtuvieron 9 transacciones válidas (60 %) y 6 inválidas (40 %).

## 5. Uso de inteligencia artificial y criterio humano

Se utilizó inteligencia artificial como herramienta de apoyo para revisar y documentar partes de la solución. Sin embargo, las decisiones sobre el esquema unificado, las monedas admitidas, las equivalencias de estados, los formatos de fecha y los criterios de validación asi como el desarrollo de la aplicación fueron definidas y revisadas por el valor humano, en este caso, mi persona como estudiante.

Finalmente, se ejecutaron pruebas funcionales para comprobar la normalización, identificación de errores, generación de métricas y exportación de resultados.