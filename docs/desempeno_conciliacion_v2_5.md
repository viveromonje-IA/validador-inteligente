# Desempeño — Conciliación banco–ledger (v2.5)

**Versión del motor de referencia:** v2.5_anclas_match  
**Fecha del informe:** 2026-09-27  
**Principio:** solo lectura (no modifica orígenes ni fusiona sin decisión humana)  

> Este documento resume resultados sobre un **benchmark público**.  
> El motor comercial y los datos de clientes **no se publican** en este repositorio.

---

## 1. Qué se evalúa

Matching entre:

- **Lado B** — movimientos de banco  
- **Lado A** — asientos / allocations contables  

El sistema **propone** matches con nivel de confianza y tipifica ambigüedades. No sustituye el ERP ni el cierre contable del cliente.

---

## 2. Dataset

| Ítem | Detalle |
|------|---------|
| Fuente | [BenchRec cash reconciliation](https://www.kaggle.com/datasets/benchmarkteam/benchrec-real-world-cash-reconciliation-dataset) (Kaggle) |
| Licencia | CC BY 4.0 |
| Universo eval | \~37.123 asientos (A) · \~32.048 movimientos banco (B) |
| Ground truth | `targetAllocation` en el archivo de solution del benchmark |

---

## 3. Anclas de decisión (diseño)

| Decisión | Condición |
|----------|-----------|
| **Match 1→1 / alta confianza** | Monto compatible **y** cuenta igual **y** fecha cercana; dominante si margen de puntaje ≥ 0,12 vs el 2º candidato |
| **Agrupado 1→N** | Suma de montos A ≈ \|B\| (partes del mismo movimiento banco) |
| **Gemelo / alternativa** | Contraste de texto o familia **y** 2º candidato pegado en puntaje (margen &lt; 0,12) |
| **Excepción (no Match)** | Faltan anclas (p. ej. sin fecha útil) u otros criterios insuficientes |

**Regla de producto:** sin ancla de fecha **no** se etiqueta como Match.  
Así se evita vender “match media” cuando la evidencia pública mostró \~26 % de acierto en solo monto+cuenta.

---

## 4. Resultados operativos (corrida completa)

| Métrica | Valor |
|---------|------:|
| Tasa de match **anclado** | **98,3 %** |
| Alta confianza | **23.244** |
| Media (incluye gemelos tipados) | **8.272** |
| Agrupados 1→N | **142** |
| Gemelos (contraste + margen) | **8.130** |
| Excepciones (sin Match) | **532** |
| Confianza promedio (propuestos) | **0,88** |
| Umbral de excepción | **0,50** |

---

## 5. Calidad vs solución oficial (ground truth)

Cotejo del tipado del producto contra `targetAllocation` (overlap de tokens de allocation):

| Tipo / nivel | n (con GT) | Overlap promedio | ≥ 0,5 | ≥ 0,7 |
|--------------|-----------:|-----------------:|------:|------:|
| **Alta** (`match` monto+fecha+cuenta) | 23.201 | **0,961** | **97,2 %** | **94,0 %** |
| Agrupado por suma | 142 | **0,964** | **96,5 %** | **93,0 %** |
| Gemelo | 8.042 | 0,899 | 89,4 % | 83,2 % |
| Excepción | 451 | 0,000 | 0 % | 0 % |

**Lectura:** cuando el sistema marca **alta confianza**, en \~**19 de cada 20** casos el solapamiento con la solución de referencia es ≥ 50 %. Las excepciones no se presentan como aciertos.

### Baseline histórico (matcher de señales, sin tipado de producto)

| Métrica | Valor |
|---------|------:|
| B con propuesta | **99,78 %** |
| Overlap promedio propuestos | **0,939** |
| Zona alta ≥ 0,5 | **96,4 %** |
| Propuestos con overlap 0 | **0** |
| Residuo overlap &lt; 0,3 | **220** |

Confirma que la base de señales es sólida; v2.5 **añade anclas** para que “Match” tenga significado estable.

---

## 6. Cómo interpretar gemelos y excepciones

| Etiqueta | No significa | Sí significa |
|----------|--------------|--------------|
| **Gemelo** | “Falló la mitad del archivo” | Hay contraste entre candidatos; no auto-cerrar; priorizar por materialidad |
| **Excepción** | “El sistema no sirve” | No hay Match anclado; cola de revisión humana |
| **Alta** | Garantía legal | Propuesta con anclas y alineación fuerte vs benchmark |

En operación real la cola humana se prioriza (monto, antigüedad, cuenta), no se vuelca el total de gemelos del benchmark.

---

## 7. Limitaciones

- BenchRec **no** es el plan de cuentas de un cliente concreto.  
- Los porcentajes son de un dataset público; en producción rigen las reglas de negocio locales.  
- Este repositorio es **demo / evidencia**; el motor de conciliación comercial se entrega en prueba acordada.  
- No sustituye dictamen contable ni auditoría externa.

---

## 8. Prueba sin costo (producto)

1. El interesado envía un CSV **anonimizado** y parámetros de referencia.  
2. Se devuelve planilla con propuestas, excepciones, etiquetas y trazas.  
3. Orígenes intactos; sin obligación de migrar sistemas.

**Contacto:** viveromonje@gmail.com  

---

## 9. Referencia de versión

| Campo | Valor |
|-------|--------|
| Código de referencia interno | v2.5_anclas_match |
| Umbral | 0,50 |
| Principio | solo_lectura |
| Documento de cierre técnico | MVP Financiero — informe final promocional 2026-09-27 |

---

*Última actualización de este resumen: septiembre 2026.*