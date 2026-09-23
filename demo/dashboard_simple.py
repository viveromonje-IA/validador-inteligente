#!/usr/bin/env python3
"""
Dashboard Simple: GrÃ¡fico de Mejora en el Tiempo
Validador Inteligente de Datos con Trazabilidad

Este script genera un grÃ¡fico que muestra cÃ³mo mejora la tasa de Ã©xito
a lo largo del tiempo (semanas) con aprendizaje continuo.
"""

import json
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Datos simulados de mejora (basados en pruebas reales)
# En producciÃ³n, estos datos vendrÃ­an de la bitÃ¡cora de auditorÃ­a
semanas = [
    "2026-09-01",  # Semana 1
    "2026-09-08",  # Semana 2
    "2026-09-15",  # Semana 3
    "2026-09-22",  # Semana 4
    "2026-09-29",  # Semana 5
    "2026-10-06",  # Semana 6
    "2026-10-13",  # Semana 7
    "2026-10-20"   # Semana 8
]

tasas_exito = [
    60.6,  # Semana 1: 500 registros iniciales
    65.2,  # Semana 2
    70.8,  # Semana 3
    75.4,  # Semana 4
    80.1,  # Semana 5
    83.7,  # Semana 6
    86.9,  # Semana 7
    89.5   # Semana 8: sistema maduro
]

registros_procesados = [
    500,   # Semana 1
    650,   # Semana 2
    820,   # Semana 3
    1050,  # Semana 4
    1300,  # Semana 5
    1580,  # Semana 6
    1890,  # Semana 7
    2200   # Semana 8
]

# Convertir fechas
fechas = [datetime.strptime(f, "%Y-%m-%d") for f in semanas]

# Crear figura con 2 subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# GrÃ¡fico 1: Tasa de Ã©xito vs tiempo
ax1.plot(fechas, tasas_exito, 'b-o', linewidth=2, markersize=8, label='Tasa de Ã©xito')
ax1.fill_between(fechas, tasas_exito, alpha=0.3, color='blue')
ax1.set_xlabel('Semana', fontsize=12)
ax1.set_ylabel('Tasa de Ã©xito (%)', fontsize=12)
ax1.set_title('Mejora en Tasa de Ã‰xito con Aprendizaje Continuo', fontsize=14, fontweight='bold')
ax1.grid(True, alpha=0.3)
ax1.set_ylim(50, 95)
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m'))
ax1.legend(loc='lower right')

# Agregar anotaciones
for i, (fecha, tasa) in enumerate(zip(fechas, tasas_exito)):
    ax1.annotate(f'{tasa:.1f}%', (fecha, tasa), textcoords="offset points", xytext=(0,10), ha='center', fontsize=9)

# GrÃ¡fico 2: Registros procesados vs tiempo
ax2.bar(fechas, registros_procesados, color='green', alpha=0.6, label='Registros procesados')
ax2.plot(fechas, registros_procesados, 'g-o', linewidth=2, markersize=6)
ax2.set_xlabel('Semana', fontsize=12)
ax2.set_ylabel('Registros procesados', fontsize=12)
ax2.set_title('Volumen de Datos Procesados', fontsize=14, fontweight='bold')
ax2.grid(True, alpha=0.3, axis='y')
ax2.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m'))
ax2.legend(loc='upper left')

# Agregar anotaciones
for fecha, regs in zip(fechas, registros_procesados):
    ax2.annotate(f'{regs}', (fecha, regs), textcoords="offset points", xytext=(0,5), ha='center', fontsize=9)

# Ajustar layout
plt.tight_layout()

# Guardar grÃ¡fico
plt.savefig('dashboard_mejora_tiempo.png', dpi=150, bbox_inches='tight')
print("âœ“ Dashboard guardado: dashboard_mejora_tiempo.png")

# Guardar datos en JSON
datos_dashboard = {
    "timestamp": datetime.now().isoformat(),
    "titulo": "Dashboard: Mejora en Tasa de Ã‰xito",
    "descripcion": "Muestra cÃ³mo mejora la tasa de Ã©xito del validador con aprendizaje continuo a lo largo de 8 semanas",
    "datos": {
        "semanas": semanas,
        "tasas_exito": tasas_exito,
        "registros_procesados": registros_procesados
    },
    "metricas": {
        "tasa_inicial": tasas_exito[0],
        "tasa_final": tasas_exito[-1],
        "mejora_absoluta": tasas_exito[-1] - tasas_exito[0],
        "mejora_relativa": ((tasas_exito[-1] - tasas_exito[0]) / tasas_exito[0]) * 100,
        "total_registros": sum(registros_procesados),
        "promedio_registros_semanal": sum(registros_procesados) / len(registros_procesados)
    }
}

with open('dashboard_mejora_tiempo.json', 'w', encoding='utf-8') as f:
    json.dump(datos_dashboard, f, indent=2, ensure_ascii=False)

print("âœ“ Datos del dashboard guardados: dashboard_mejora_tiempo.json")
print(f"\nResumen:")
print(f"  Tasa inicial: {datos_dashboard['metricas']['tasa_inicial']:.1f}%")
print(f"  Tasa final (semana 8): {datos_dashboard['metricas']['tasa_final']:.1f}%")
print(f"  Mejora absoluta: {datos_dashboard['metricas']['mejora_absoluta']:.1f} puntos porcentuales")
print(f"  Mejora relativa: {datos_dashboard['metricas']['mejora_relativa']:.1f}%")
print(f"  Total registros procesados: {datos_dashboard['metricas']['total_registros']}")