#!/usr/bin/env python3
"""Procesador por lote del Validador Inteligente de Datos.

Uso:
    python scripts/validar_archivo.py --entrada leads.csv --salida resultados.json
    python scripts/validar_archivo.py --entrada leads.json --salida resultados.json

No modifica CRM, no envía mensajes y no sobrescribe la fuente original.
Lee registros, valida, crea una auditoría y exporta el resultado para revisión.
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src import ValidadorInteligente

CAMPOS_ADMITIDOS = ("nombre", "email", "telefono", "empresa", "cargo")


def cargar_json(ruta: Path) -> list[dict[str, Any]]:
    contenido = json.loads(ruta.read_text(encoding="utf-8"))
    if isinstance(contenido, dict):
        contenido = contenido.get("registros", [])
    if not isinstance(contenido, list):
        raise ValueError("El JSON debe ser una lista de registros o contener la clave 'registros'.")
    return contenido


def cargar_csv(ruta: Path, fuente_predeterminada: str) -> list[dict[str, Any]]:
    with ruta.open("r", encoding="utf-8-sig", newline="") as archivo:
        lector = csv.DictReader(archivo)
        if not lector.fieldnames:
            raise ValueError("El CSV no tiene encabezados.")
        registros = []
        for indice, fila in enumerate(lector, start=1):
            datos = {campo: (fila.get(campo) or "").strip() for campo in CAMPOS_ADMITIDOS}
            registros.append({
                "id": (fila.get("id") or f"CSV-{indice:06d}").strip(),
                "fuente": (fila.get("fuente") or fuente_predeterminada).strip(),
                "datos": datos,
            })
    return registros


def normalizar_registros(registros: list[dict[str, Any]], fuente_predeterminada: str) -> list[dict[str, Any]]:
    salida = []
    for indice, registro in enumerate(registros, start=1):
        datos_originales = registro.get("datos", registro)
        datos = {campo: str(datos_originales.get(campo, "") or "").strip() for campo in CAMPOS_ADMITIDOS}
        salida.append({
            "id": str(registro.get("id") or f"JSON-{indice:06d}"),
            "fuente": str(registro.get("fuente") or fuente_predeterminada),
            "datos": datos,
        })
    return salida


def resumir(resultados: list[dict[str, Any]]) -> dict[str, Any]:
    total = len(resultados)
    validos = sum(1 for item in resultados if item["valido"])
    acciones: dict[str, int] = {}
    errores: dict[str, int] = {}
    for item in resultados:
        for campo in item["resultados"].values():
            acciones[campo["accion"]] = acciones.get(campo["accion"], 0) + 1
            for error in campo["errores"]:
                errores[error] = errores.get(error, 0) + 1
    return {
        "total_registros": total,
        "registros_validos": validos,
        "registros_con_revision": total - validos,
        "tasa_validos": round(validos / total, 4) if total else 0.0,
        "acciones": dict(sorted(acciones.items(), key=lambda x: x[1], reverse=True)),
        "errores": dict(sorted(errores.items(), key=lambda x: x[1], reverse=True)),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Valida leads CSV o JSON y genera resultados auditables.")
    parser.add_argument("--entrada", required=True, help="Ruta de archivo .csv o .json")
    parser.add_argument("--salida", default="resultados_validacion.json", help="Ruta del JSON de salida")
    parser.add_argument("--fuente", default="archivo_importado", help="Fuente predeterminada para registros sin campo fuente")
    args = parser.parse_args()

    entrada = Path(args.entrada)
    salida = Path(args.salida)
    if not entrada.exists():
        raise SystemExit(f"No existe el archivo de entrada: {entrada}")

    extension = entrada.suffix.lower()
    if extension == ".csv":
        registros = cargar_csv(entrada, args.fuente)
    elif extension == ".json":
        registros = normalizar_registros(cargar_json(entrada), args.fuente)
    else:
        raise SystemExit("Formato no admitido. Usar .csv o .json")

    validador = ValidadorInteligente()
    resultados = [validador.validar_registro(registro) for registro in registros]

    reporte = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "modo": "solo_lectura",
        "entrada": str(entrada),
        "resumen": resumir(resultados),
        "resultados": resultados,
        "memoria": validador.memoria.resumen(),
        "auditoria": validador.bitacora.entradas,
        "nota": "El proceso no modifica CRM, no envía mensajes y no sobrescribe datos originales.",
    }
    salida.parent.mkdir(parents=True, exist_ok=True)
    salida.write_text(json.dumps(reporte, ensure_ascii=False, indent=2), encoding="utf-8")

    resumen = reporte["resumen"]
    print(f"Registros procesados: {resumen['total_registros']}")
    print(f"Registros válidos: {resumen['registros_validos']}")
    print(f"Registros con revisión: {resumen['registros_con_revision']}")
    print(f"Resultado guardado: {salida}")


if __name__ == "__main__":
    main()
