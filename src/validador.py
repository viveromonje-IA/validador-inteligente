"""Núcleo de validación por áreas semánticas."""
from __future__ import annotations
import re
from typing import Any
from .validacion_externa import ValidacionExternaLocal
from .memoria_errores import MemoriaErrores
from .bitacora_auditoria import BitacoraAuditoria


class ValidadorInteligente:
    AREAS = {
        "nombre": "identidad_personal",
        "email": "contacto_digital",
        "telefono": "contacto_telefonico",
        "empresa": "datos_corporativos",
        "cargo": "datos_laborales",
    }
    TYPOS_DOMINIO = {"gamil.com": "gmail.com", "hotmial.com": "hotmail.com", "outlok.com": "outlook.com"}

    def __init__(self, validacion_externa: ValidacionExternaLocal | None = None,
                 memoria: MemoriaErrores | None = None,
                 bitacora: BitacoraAuditoria | None = None) -> None:
        self.externa = validacion_externa or ValidacionExternaLocal()
        self.memoria = memoria or MemoriaErrores()
        self.bitacora = bitacora or BitacoraAuditoria()

    def validar_campo(self, campo: str, valor: str, registro_id: str, fuente: str) -> dict[str, Any]:
        area = self.AREAS.get(campo, "desconocida")
        r = {"campo": campo, "valor_original": valor, "area": area, "valido": True,
             "errores": [], "sugerencias": [], "accion": "aceptar", "confianza": 1.0,
             "evidencia_externa": None}
        if not valor:
            r.update(valido=False, accion="solicitar_dato", confianza=0.5)
            r["errores"].append("campo_vacio")
        elif area == "contacto_telefonico":
            limpio = re.sub(r"[^\d+]", "", valor)
            if "@" in valor:
                r.update(valido=False, accion="reasignar_campos", confianza=0.4)
                r["errores"].append("email_en_casilla_telefono")
            elif not limpio.startswith("+"):
                r.update(valido=False, accion="confirmar_por_fuente_o_llamada", confianza=0.6)
                r["errores"].append("telefono_sin_codigo_pais")
                r["sugerencias"].append("Usar número confirmado por WhatsApp o solicitar formato internacional.")
            elif len(limpio) < 10:
                r.update(valido=False, accion="solicitar_dato", confianza=0.5)
                r["errores"].append("telefono_demasiado_corto")
        elif area == "contacto_digital":
            evidencia = self.externa.validar_email(valor)
            r["evidencia_externa"] = evidencia
            if not evidencia["valido"]:
                r.update(valido=False, accion="revisar_email", confianza=0.3)
                r["errores"].append(evidencia["motivo"])
            else:
                dominio = evidencia["dominio"]
                if dominio in self.TYPOS_DOMINIO:
                    r.update(valido=False, accion="sugerir_correccion", confianza=0.8)
                    r["errores"].append("typo_dominio_comun")
                    r["sugerencias"].append(f"¿Quiso decir {self.TYPOS_DOMINIO[dominio]}?")
        elif area == "datos_corporativos":
            evidencia = self.externa.validar_empresa(valor)
            r["evidencia_externa"] = evidencia
            if "@" in valor or valor.startswith("+"):
                r.update(valido=False, accion="reasignar_campos", confianza=0.4)
                r["errores"].append("dato_contacto_en_casilla_empresa")
            elif evidencia["existe"] is False:
                r.update(valido=False, accion="requerir_segunda_fuente", confianza=0.3)
                r["errores"].append("empresa_no_confirmada")
            elif evidencia["existe"] is None:
                r.update(accion="mantener_incertidumbre", confianza=0.65)
                r["sugerencias"].append("No hay referencia local: verificar con una fuente externa real o revisión humana.")
        elif area == "datos_laborales":
            if re.search(r"\bDirecto\b", valor, re.IGNORECASE):
                r.update(valido=False, accion="sugerir_correccion", confianza=0.7)
                r["errores"].append("posible_autocorrector_truncamiento")
            elif "Distrubucion" in valor:
                r.update(accion="corregir_y_registrar", confianza=0.85)
                r["errores"].append("posible_autocorrector_ortografico")
        for error in r["errores"]:
            self.memoria.registrar(registro_id, campo, error, fuente, valor)
        self.bitacora.registrar(registro_id, campo, r, fuente)
        return r

    def validar_registro(self, registro: dict[str, Any]) -> dict[str, Any]:
        registro_id = registro["id"]
        fuente = registro.get("fuente", "desconocida")
        resultados = {campo: self.validar_campo(campo, str(valor or ""), registro_id, fuente)
                      for campo, valor in registro["datos"].items()}
        return {
            "registro_id": registro_id,
            "fuente": fuente,
            "resultados": resultados,
            "valido": all(r["valido"] for r in resultados.values()),
        }
