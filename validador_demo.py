#!/usr/bin/env python3
"""
Demo: Validador Inteligente de Datos con Trazabilidad
Versión 1.0 (MVP comercializable)

Este script muestra cómo usar el validador con 5 registros de ejemplo.
Ideal para probar el sistema antes de usarlo en producción.

Uso:
    python validador_demo.py

Resultados:
    Se guardan en: demo_resultados.json
"""

import json
import re
from datetime import datetime
from typing import Dict, List

# ============================================
# CLASES DEL SISTEMA (versión simplificada para demo)
# ============================================

class ValidacionExterna:
    """Validación con fuentes externas (dominios, empresas, países)"""

    def __init__(self):
        self.empresas_conocidas = {
            "alimentos del sur": {"existe": True, "dominio": "alimentosdelsur.com", "pais": "AR"},
            "techcorp": {"existe": True, "dominio": "techcorp.com", "pais": "AR"},
            "logistic sur": {"existe": True, "dominio": "logisticsur.com", "pais": "AR"},
            "chile import": {"existe": True, "dominio": "chileimport.cl", "pais": "CL"},
            "empresa inexistente": {"existe": False, "dominio": None, "pais": None}
        }
        self.dominios_validos = ['gmail.com', 'hotmail.com', 'yahoo.com', 'outlook.com']
        self.dominios_sospechosos = ['.xyz', '.top', '.club']

    def validar_dominio_email(self, email: str) -> Dict:
        if not email or '@' not in email:
            return {"valido": False, "motivo": "email_invalido"}

        dominio = email.split('@')[1].lower()

        if dominio in self.dominios_validos:
            return {"valido": True, "tipo": "gratuito", "dominio": dominio}

        for s in self.dominios_sospechosos:
            if dominio.endswith(s):
                return {"valido": False, "motivo": "dominio_sospechoso"}

        if dominio.endswith('.com') or dominio.endswith('.cl'):
            return {"valido": True, "tipo": "corporativo", "dominio": dominio}

        return {"valido": True, "tipo": "desconocido", "dominio": dominio}

    def validar_empresa(self, empresa: str) -> Dict:
        if not empresa:
            return {"existe": False, "motivo": "campo_vacio"}

        empresa_norm = empresa.lower().strip()
        empresa_norm = re.sub(r'[.\-,;:]', '', empresa_norm)
        empresa_norm = re.sub(r'\s*(s\.?\s*a\.?|s\.?\s*r\.?\s*l\.?|sr[l]?|sa)\s*$', '', empresa_norm)

        for nombre, datos in self.empresas_conocidas.items():
            if nombre in empresa_norm:
                return {"existe": datos["existe"], "nombre_oficial": nombre.title(), "dominio": datos["dominio"], "pais": datos["pais"]}

        if len(empresa_norm) > 8:
            return {"existe": True, "nombre_oficial": empresa.title(), "dominio": None, "pais": "desconocido"}

        return {"existe": False, "motivo": "empresa_corta_o_generica"}

def validar_campo(campo: str, valor: str, validacion_externa: ValidacionExterna) -> Dict:
    """Valida un campo individual"""
    areas = {"nombre": "identidad", "email": "contacto_digital", "telefono": "contacto_telefonico", "empresa": "datos_corporativos", "cargo": "datos_laborales"}
    area = areas.get(campo.lower(), "desconocida")

    resultado = {"campo": campo, "valor": valor, "area": area, "es_valido": True, "errores": [], "sugerencias": [], "accion": "ninguna", "confianza": 1.0, "validacion_externa": None}

    if not valor:
        resultado["es_valido"] = False
        resultado["errores"].append("campo_vacio")
        resultado["accion"] = "solicitar_dato_obligatorio"
        resultado["confianza"] = 0.5
        return resultado

    if area == "contacto_telefonico":
        telefono_limpio = re.sub(r'[^\d+]', '', valor)
        if not telefono_limpio.startswith('+'):
            resultado["errores"].append("telefono_sin_codigo_pais")
            resultado["sugerencias"].append("Agregar código de país (+54 para Argentina)")
            resultado["es_valido"] = False
            resultado["accion"] = "sugerir_llamada_corroboracion"
            resultado["confianza"] = 0.6
        if len(telefono_limpio) < 10:
            resultado["errores"].append("telefono_demasiado_corto")
            resultado["es_valido"] = False
            resultado["confianza"] = 0.5
        if '@' in valor:
            resultado["errores"].append("posible_cruce_areas_email_en_telefono")
            resultado["es_valido"] = False
            resultado["accion"] = "reasignar_campos"
            resultado["confianza"] = 0.4

    elif area == "contacto_digital":
        if '@' not in valor:
            resultado["errores"].append("email_sin_arroba")
            resultado["es_valido"] = False
            resultado["accion"] = "validar_dominio_o_sugerir_correccion"
            resultado["confianza"] = 0.5
        else:
            validacion_dom = validacion_externa.validar_dominio_email(valor)
            resultado["validacion_externa"] = validacion_dom
            if not validacion_dom["valido"]:
                resultado["errores"].append("dominio_email_invalido_externo")
                resultado["sugerencias"].append(f"Dominio inválido: {validacion_dom.get('motivo', '')}")
                resultado["es_valido"] = False
                resultado["confianza"] = 0.3
                resultado["accion"] = "validacion_externa_fallo"
            else:
                dominios_typos = {'gamil.com': 'gmail.com', 'hotmial.com': 'hotmail.com', 'yaho.com': 'yahoo.com', 'outlok.com': 'outlook.com'}
                dominio = valor.split('@')[1].lower()
                if dominio in dominios_typos:
                    resultado["errores"].append("email_typo_dominio_comun")
                    resultado["sugerencias"].append(f"Typo detectado: {dominio} -> {dominios_typos[dominio]}")
                    resultado["es_valido"] = False
                    resultado["accion"] = "sugerir_correccion_sintaxis"
                    resultado["confianza"] = 0.8

    elif area == "datos_corporativos":
        if re.search(r'S\.\s{2,}A\.', valor, re.IGNORECASE):
            resultado["errores"].append("autocorrector_intruso_espacio_empresa")
            resultado["accion"] = "normalizar_autocorrector"
            resultado["es_valido"] = False
            resultado["confianza"] = 0.7

        validacion_emp = validacion_externa.validar_empresa(valor)
        resultado["validacion_externa"] = validacion_emp
        if not validacion_emp.get("existe", False):
            resultado["errores"].append("empresa_no_existe_externo")
            resultado["sugerencias"].append(f"Empresa no encontrada: {validacion_emp.get('motivo', '')}")
            resultado["es_valido"] = False
            resultado["confianza"] = 0.3
            resultado["accion"] = "validacion_externa_fallo"
        if '@' in valor or valor.startswith('+') or re.match(r'^\d+$', valor):
            resultado["errores"].append("posible_cruce_areas_empresa_contiene_email_o_telefono")
            resultado["es_valido"] = False
            resultado["accion"] = "reasignar_campos"
            resultado["confianza"] = 0.4

    elif area == "datos_laborales":
        if re.search(r'[aeiou]Ã¡[sn]', valor, re.IGNORECASE):
            resultado["errores"].append("autocorrector_intruso_acento_cargo")
            resultado["accion"] = "sugerir_correccion_autocorrector"
            resultado["confianza"] = 0.7
        if re.search(r'\bDirecto\b', valor, re.IGNORECASE) and 'Director' not in valor:
            resultado["errores"].append("autocorrector_intruso_truncamiento_cargo")
            resultado["accion"] = "sugerir_correccion_autocorrector"
            resultado["confianza"] = 0.7
        if re.search(r'ub', valor, re.IGNORECASE):
            resultado["errores"].append("autocorrector_intruso_ortografia_cargo")
            resultado["accion"] = "corregir_automatico"
            resultado["confianza"] = 0.85

    return resultado

def validar_registro(registro: Dict, validacion_externa: ValidacionExterna) -> Dict:
    """Valida un registro completo"""
    resultados = {}
    todos_validos = True

    for campo, valor in registro["datos"].items():
        resultado = validar_campo(campo, valor, validacion_externa)
        resultados[campo] = resultado
        if not resultado["es_valido"]:
            todos_validos = False

    return {"registro_id": registro["id"], "fuente": registro["fuente"], "resultados": resultados, "todos_validos": todos_validos}

# ============================================
# DATOS DE DEMO
# ============================================

registros_demo = [
    {"id": "DEMO-001", "fuente": "web_form", "datos": {"nombre": "Carlos Mendoza", "email": "cmendoza@alimentosdelsur.com", "telefono": "+5491155555555", "empresa": "Alimentos del Sur S.A.", "cargo": "Gerente de Compras"}},
    {"id": "DEMO-002", "fuente": "whatsapp", "datos": {"nombre": "Juan Pérez", "email": "jperez@gamil.com", "telefono": "1155555555", "empresa": "TechCorp S.A.", "cargo": "Director"}},
    {"id": "DEMO-003", "fuente": "excel_eventos", "datos": {"nombre": "Maria Gonzalez", "email": "maria@empresainexistente.xyz", "telefono": "+5493514445566", "empresa": "Empresa Inexistente XYZ", "cargo": "Ventas y Distrubucion"}},
    {"id": "DEMO-004", "fuente": "web_form_movil", "datos": {"nombre": "Ana Rodriguez", "email": "ana@logisticsur.com", "telefono": "+5491144332211", "empresa": "Logistic Sur S.A.", "cargo": "Gerente de Compras"}},
    {"id": "DEMO-005", "fuente": "linkedin", "datos": {"nombre": "Diego Torres", "email": "diego@chileimport.cl", "telefono": "+56922334455", "empresa": "Chile Import Ltda", "cargo": "Director Ejecutivo"}}
]

# ============================================
# EJECUCIÓN DEL DEMO
# ============================================

if __name__ == "__main__":
    print("="*80)
    print("DEMO: VALIDADOR INTELIGENTE DE DATOS CON TRAZABILIDAD")
    print("Versión 1.0 (MVP comercializable)")
    print("="*80)
    print()

    validacion_externa = ValidacionExterna()
    resultados_demo = []

    for reg in registros_demo:
        print(f"Procesando {reg['id']} ({reg['fuente']})...")
        print("-" * 80)

        resultado_registro = validar_registro(reg, validacion_externa)
        resultados_demo.append(resultado_registro)

        for campo, resultado in resultado_registro["resultados"].items():
            estado = "✓ VÁLIDO" if resultado["es_valido"] else "✗ ERROR"
            print(f"  {campo}: {estado} (confianza: {resultado['confianza']:.2f})")

            if resultado["errores"]:
                print(f"    Errores: {', '.join(resultado['errores'])}")
            if resultado["sugerencias"]:
                print(f"    Sugerencias: {', '.join(resultado['sugerencias'])}")
            if resultado["accion"] != "ninguna":
                print(f"    Acción: {resultado['accion']}")
            if resultado.get("validacion_externa"):
                ve = resultado["validacion_externa"]
                if "valido" in ve:
                    print(f"    Validación externa email: {ve['valido']} ({ve.get('tipo', 'N/A')})")
                if "existe" in ve:
                    print(f"    Validación externa empresa: {ve['existe']} ({ve.get('nombre_oficial', 'N/A')})")

        print()

    # Resumen final
    print("="*80)
    print("RESUMEN")
    print("="*80)

    registros_validos = len([r for r in resultados_demo if r["todos_validos"]])
    registros_con_errores = len([r for r in resultados_demo if not r["todos_validos"]])

    print(f"\nRegistros procesados: {len(resultados_demo)}")
    print(f"  - Válidos: {registros_validos} ({registros_validos/len(resultados_demo)*100:.1f}%)")
    print(f"  - Con errores: {registros_con_errores} ({registros_con_errores/len(resultados_demo)*100:.1f}%)")

    # Guardar resultados
    demo_resultados = {
        "timestamp": datetime.now().isoformat(),
        "titulo": "Demo: Validador Inteligente de Datos",
        "registros_procesados": len(resultados_demo),
        "registros_validos": registros_validos,
        "registros_con_errores": registros_con_errores,
        "resultados_detallados": resultados_demo
    }

    with open('demo_resultados.json', 'w', encoding='utf-8') as f:
        json.dump(demo_resultados, f, indent=2, ensure_ascii=False)

    print(f"\n✓ Resultados guardados en: demo_resultados.json")
    print("\n" + "="*80)
    print("¡Demo completado exitosamente!")
    print("="*80)
