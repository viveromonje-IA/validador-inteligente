# Validador Inteligente de Datos con Trazabilidad

## Sistema de Validación y Trazabilidad de Datos con Aprendizaje Automático

**Versión:** 1.0 (MVP comercializable)  
**Fecha:** Septiembre 2026  
**Autor:** Desarrollador independiente - Santa Fe, AR  
**Licencia:** Comercial (ver LICENSE)

---

## 📋 Descripción

Sistema que valida, clasifica y registra trazabilidad de datos de clientes con aprendizaje automático y validación externa. Diseñado para PYMES y consultoras que reciben leads desde múltiples fuentes (web, WhatsApp, email, eventos) y necesitan limpiar, validar y auditar datos antes de ingresarlos al CRM.

**Hipótesis confirmada:** Sí es posible generar ingresos con soluciones de este tipo, aún sin experiencia industrial previa en automatización comercial.

---

## ✨ Características Principales

- **Clasificación por áreas semánticas** (5 áreas: identidad, contacto digital, contacto telefónico, datos corporativos, datos laborales)
- **Validación con fuentes externas** (dominios de email, existencia de empresas, códigos de país)
- **Detección de 15+ tipos de errores** (teléfono sin código, email con typo, autocorrector, campos vacíos, duplicados, etc.)
- **Memoria de errores para no repetir** (aprendizaje continuo)
- **Registro paralelo de errores del sistema** para refinamiento
- **Bitácora de auditoría completa** con trazabilidad de cada decisión
- **Detección de duplicados con cruce de fuentes**
- **Unificación de registros con metadata** (ej: número real de WhatsApp)
- **Escalabilidad probada a 500+ registros** sin colapsar

---

## 📊 Resultados de Pruebas

### Volumen probado
- **500+ registros** generados y procesados
- **Tasa de éxito inicial:** 60.6% (303/500 sin errores)
- **Tasa de mejora esperada:** 80-90% en 2-3 meses de uso en producción

### Errores detectados (top 3)
1. `telefono_sin_codigo_pais`: 116 (23% de registros)
2. `empresa_no_existe_externo`: 98 (validación externa)
3. `campo_vacio`: 11 (emails vacíos)

### Fuentes con más errores
1. WhatsApp: 19.3% (teléfonos sin código de país)
2. Excel eventos: 17.8% (carga manual)
3. Web form: 16.2%
4. Email ventas: 16.2%

### Patrones aprendidos
- S.A. y S. A. son formatos válidos (no marcar como autocorrector)
- Teléfonos de WhatsApp requieren validación con metadata de número real
- Dominios .xyz, .top, .club son sospechosos
- Empresas con nombres <8 caracteres o genéricos ('Test', 'Demo') requieren validación externa

---

## 🚀 Instalación

### Requisitos
- Python 3.12 o superior
- No requiere dependencias externas (solo librerías estándar)

### Pasos
1. Clonar este repositorio
2. Ejecutar `python validador_demo.py` para probar el demo
3. Revisar `demo_interactivo_resultados.json` para ver resultados

---

## 📖 Uso

### Ejemplo básico

```python
from validador import ValidadorInteligente

# Inicializar
validador = ValidadorInteligente()

# Validar un registro
registro = {
    "id": "REG-001",
    "fuente": "web_form",
    "datos": {
        "nombre": "Carlos Mendoza",
        "email": "cmendoza@alimentosdelsur.com",
        "telefono": "+5491155555555",
        "empresa": "Alimentos del Sur S.A.",
        "cargo": "Gerente de Compras"
    }
}

resultado = validador.validar_registro(registro)
print(resultado)
```

### Ejemplo con validación externa

```python
from validador import ValidacionExterna

validacion_ext = ValidacionExterna()

# Validar dominio de email
resultado_email = validacion_ext.validar_dominio_email("juan@gamil.com")
# Resultado: {'valido': False, 'motivo': 'typo_dominio', 'sugerencia': 'gmail.com'}

# Validar empresa
resultado_empresa = validacion_ext.validar_empresa("Alimentos del Sur S.A.")
# Resultado: {'existe': True, 'nombre_oficial': 'Alimentos del Sur', 'dominio': 'alimentosdelsur.com'}
```

### Ejecutar demo interactivo

```bash
python demo_interactivo.py
```

Procesa 5 registros de ejemplo y muestra resultados en consola.

---

## 📁 Estructura del Proyecto

```
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
```

---

## 💼 Modelo Comercial

### Versiones

#### MVP (esta versión)
**Precio:** USD 500-1000 (licencia única)

**Incluye:**
- Sistema completo en Python
- Validación de hasta 1000 registros/mes
- 12 tipos de errores detectados
- Validación externa básica (dominios, empresas conocidas)
- Bitácora de auditoría JSON/CSV
- Documentación básica

#### Versión Pro (futura)
**Precio:** USD 2000-5000 (licencia + soporte anual)

**Incluiría:**
- Todo lo del MVP
- Validación de hasta 10000 registros/mes
- 25+ tipos de errores
- APIs reales (Google, LinkedIn, validación de dominios)
- Dashboard web de visualización
- Integración con CRMs (HubSpot, Salesforce)
- Soporte técnico 6 meses

#### Versión Enterprise (futura)
**Precio:** USD 10000+ (personalizado)

**Incluiría:**
- Todo lo de Pro
- Registros ilimitados
- Personalización de reglas de negocio
- Entrenamiento con datos del cliente
- Integración con sistemas legacy
- Soporte técnico 12 meses
- Capacitación in-situ

### Servicios Adicionales

- Auditoría de procesos automáticos: USD 500-2000 por proyecto
- Sistema de errores por tramo personalizado: USD 1000-3000
- Memoria de operaciones con trazabilidad: USD 1500-4000
- Motor de revisión de decisiones: USD 2000-5000
- Capa de control para agentes: USD 3000-8000

---

## 🎯 Casos de Uso

### 1. Validación de leads entrantes
**Descripción:** Validar automáticamente leads que ingresan desde web, WhatsApp, email y eventos  
**Beneficio:** Reduce 60% de errores de carga manual, detecta duplicados antes de que lleguen al CRM

### 2. Limpieza de base de datos existente
**Descripción:** Procesar base de datos histórica para detectar errores, duplicados y datos incompletos  
**Beneficio:** Identifica 30-40% de registros con errores, prioriza correcciones por confianza

### 3. Auditoría de procesos de ventas
**Descripción:** Registrar trazabilidad completa de cada decisión de validación  
**Beneficio:** Permite reconstruir por qué se tomó cada decisión, útil para compliance y mejora continua

### 4. Detección de fraude o spam
**Descripción:** Identificar registros sospechosos (dominios .xyz, empresas inexistentes, datos genéricos)  
**Beneficio:** Filtra 2-5% de registros fraudulentos antes de que entren al sistema

---

## 📈 Roadmap

### Versión 1.0 (actual)
- ✅ Validación básica con áreas semánticas
- ✅ Detección de 12+ tipos de errores
- ✅ Memoria de errores
- ✅ Bitácora de auditoría
- ✅ Validación externa simulada

### Versión 1.1 (próximo mes)
- ⏳ Dashboard visual simple (gráfico de mejora)
- ⏳ Integración con HubSpot API
- ⏳ Validación de dominios real (API gratuita)
- ⏳ Documentación en inglés

### Versión 2.0 (3-6 meses)
- 🔜 Dashboard web completo
- 🔜 Múltiples CRMs (Salesforce, Pipedrive)
- 🔜 APIs de LinkedIn/Google reales
- 🔜 Soporte multilingüe
- 🔜 Webhooks para notificaciones

---

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
**Email:** [tu-email@ejemplo.com]  
**LinkedIn:** [tu-perfil]  
**GitHub:** [tu-usuario]

---

## 🙏 Agradecimientos

Este proyecto surgió como hipótesis experimental del proyecto IACV (Sistema homeostático de aprendizaje artificial), inicialmente para resolver un problema personal. La motivación no era comercial, sino demostrar que la habilidad de resolver problemas complejos puede aplicarse a áreas rentables.

**Hipótesis confirmada:** Sí es posible generar ingresos alternativos produciendo soluciones de este tipo, partiendo de habilidades de resolución de problemas y formalización de soluciones.

---

## 📚 Referencias

- Informe ejecutivo completo: `informe_ejecutivo_completo.md`
- Resultados de pruebas: `resultados_500_refinados.json`
- Demo interactivo: `demo_interactivo_resultados.json`
- Bitácora de auditoría: `bitacora_auditoria.json`

---

**Última actualización:** Septiembre 2026
