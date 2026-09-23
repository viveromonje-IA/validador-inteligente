"""Validaciones externas locales y sustituibles.

Esta implementación no consulta Internet ni APIs reales. Representa una segunda
fuente controlada basada en un catálogo local, útil para demos y pruebas.
"""
from __future__ import annotations
import re
from typing import Any


class ValidacionExternaLocal:
    def __init__(self, empresas: dict[str, dict[str, Any]] | None = None):
        self.empresas = empresas or {
            "alimentos del sur": {"dominio": "alimentosdelsur.com", "pais": "AR"},
            "techcorp": {"dominio": "techcorp.com", "pais": "AR"},
            "logistic sur": {"dominio": "logisticsur.com", "pais": "AR"},
            "chile import": {"dominio": "chileimport.cl", "pais": "CL"},
        }
        self.dominios_gratuitos = {"gmail.com", "hotmail.com", "outlook.com", "yahoo.com"}
        self.dominios_sospechosos = (".xyz", ".top", ".club", ".click")

    @staticmethod
    def normalizar_empresa(valor: str) -> str:
        valor = valor.lower().strip()
        valor = re.sub(r"[.,;:-]", "", valor)
        valor = re.sub(r"\s*(s\s*a|s\s*r\s*l|sa|srl)\s*$", "", valor)
        return re.sub(r"\s+", " ", valor).strip()

    def validar_email(self, email: str) -> dict[str, Any]:
        if not email or "@" not in email or email.count("@") != 1:
            return {"valido": False, "motivo": "email_invalido", "fuente": "catalogo_local"}
        dominio = email.rsplit("@", 1)[1].lower().strip()
        if any(dominio.endswith(sufijo) for sufijo in self.dominios_sospechosos):
            return {"valido": False, "motivo": "dominio_sospechoso", "dominio": dominio, "fuente": "catalogo_local"}
        tipo = "gratuito" if dominio in self.dominios_gratuitos else "corporativo_o_desconocido"
        return {"valido": True, "dominio": dominio, "tipo": tipo, "fuente": "catalogo_local"}

    def validar_empresa(self, empresa: str) -> dict[str, Any]:
        normalizada = self.normalizar_empresa(empresa)
        if not normalizada:
            return {"existe": False, "motivo": "empresa_vacia", "fuente": "catalogo_local"}
        for nombre, datos in self.empresas.items():
            if nombre in normalizada or normalizada in nombre:
                return {"existe": True, "nombre_referencia": nombre.title(), **datos, "fuente": "catalogo_local"}
        return {"existe": None, "motivo": "sin_referencia_local", "fuente": "catalogo_local"}
