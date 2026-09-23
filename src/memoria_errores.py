"""Memoria explícita de errores y patrones capitalizados."""
from __future__ import annotations
from collections import Counter
from datetime import datetime, timezone
from typing import Any


class MemoriaErrores:
    def __init__(self) -> None:
        self.eventos: list[dict[str, Any]] = []
        self.patrones_capitalizados: dict[str, str] = {}

    def registrar(self, registro_id: str, campo: str, error: str, origen: str, valor: str) -> dict[str, Any]:
        evento = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "registro_id": registro_id,
            "campo": campo,
            "error": error,
            "origen": origen,
            "valor": valor,
            "capitalizado": error in self.patrones_capitalizados,
        }
        self.eventos.append(evento)
        return evento

    def capitalizar(self, error: str, regla: str) -> None:
        self.patrones_capitalizados[error] = regla
        for evento in self.eventos:
            if evento["error"] == error:
                evento["capitalizado"] = True

    def resumen(self) -> dict[str, Any]:
        return {
            "total_eventos": len(self.eventos),
            "por_error": dict(Counter(e["error"] for e in self.eventos)),
            "patrones_capitalizados": self.patrones_capitalizados,
        }
