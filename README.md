# Validador Inteligente — Decisiones con trazabilidad

Este es un sistema de Validación y Trazabilidad de Datos con Aprendizaje Automático.
No es un limpiador de datos a ciegas. Valida, propone correcciones y deja cada decisión "registrada y auditable": qué se marcó, por qué y bajo qué regla. Los orígenes **no se modifican** (solo lectura / propuestas).

## Destinatarios

- Empresas que manejan volúmenes altos de datos cruzados y necesitan depurarlos con criterio
- Operaciones que deben explicar cambios ante auditoría o compliance
- Equipos que reciben leads desde web, WhatsApp y otras fuentes

## Funcionamiento

- Validación de tipo/formato y reglas de negocio
- Detección de errores frecuentes (teléfono sin código de país, typos de dominio, campos vacíos, duplicados entre fuentes)
- Memoria de errores para no repetir la misma corrección
- Bitácora de auditoría por registro

## Líneas de producto

| Módulo | Uso |
|--------|-----|
| **Leads / contactos** (demo en este repositorio) | Higiene multi-fuente antes del CRM |
| **Conciliación banco–ledger** | Match anclado (monto + cuenta + fecha), agrupados, excepciones tipadas |

## Prueba sin costo

1. Enviá un CSV **anonimizado** y parámetros de referencia.
2. Recibís una planilla con resultados y trazas de decisión.
3. No requiere migrar sistemas; los datos originales no se alteran.

**Contacto:** (Ver Contacto)


## Demo local

git clone https://github.com/viveromonje-IA/validador-inteligente.git
cd validador-inteligente
python demo_interactivo.py

## 📁 Estructura del Proyecto

validador-inteligente/
├── README.md                    # Este archivo
├── LICENSE                      # Licencia comercial
├── validador.py                 # Módulo principal
├── validacion_externa.py        # Validación con fuentes externas
├── memoria_errores.py           # Memoria y aprendizaje
├── bitacora_auditoria.py        # Auditoría y trazabilidad
├── demo_interactivo.py          # Demo interactivo
├── demo_interactivo_resultados.json  # Resultados del demo
├── informe_ejecutivo_completo.md     # Informe ejecutivo completo
└── tests/                       # Pruebas unitarias
    ├── test_validador.py
    └── test_validacion_externa.py


## 🤝 Contribución

Este es un producto comercial con licencia cerrada. No se aceptan pull requests directos, pero podés:

- Reportar bugs o sugerencias en Issues
- Contactar al autor para licencias enterprise
- Compartir casos de éxito (con autorización)

---

## 📄 Licencia

**Licencia Comercial Cerrada**

Este software es propiedad intelectual del autor. Su uso está sujeto a los términos de la licencia comercial (ver archivo LICENSE).

**Resumen:**
- ✅ Uso personal o comercial con licencia válida
- ✅ Modificación para uso propio con licencia válida
- ❌ Distribución sin autorización
- ❌ Venta o re-licenciamiento sin autorización
- ❌ Uso en producción sin licencia válida

**Para adquirir una licencia:** Contactar al autor (ver sección de contacto).

---

## 📞 Contacto

**Autor:** Desarrollador independiente  
**Ubicación:** Santa Fe, Argentina  
**Email:** [viveromonje@gmail.com]  
**LinkedIn:** [en desarrollo]  
**GitHub:** [viveromonje-IA]
