"""Bitácora de decisiones: conserva evidencia y confianza por campo."""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any


class BitacoraAuditoria:
    def __init__(self) -> None:
        self.entradas: list[dict[str, Any]] = []

    def registrar(self, registro_id: str, campo: str, resultado: dict[str, Any], fuente: str) -> dict[str, Any]:
        entrada = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "registro_id": registro_id,
            "campo": campo,
            "fuente": fuente,
            "area": resultado["area"],
            "accion": resultado["accion"],
            "confianza": resultado["confianza"],
            "errores": list(resultado["errores"]),
            "evidencia_externa": resultado.get("evidencia_externa"),
        }
        self.entradas.append(entrada)
        return entrada

    def pendientes_revision(self, umbral: float = 0.7) -> list[dict[str, Any]]:
        return [e for e in self.entradas if e["confianza"] < umbral]
