
from pathlib import Path

import pandas as pd


REQUIRED_COLUMNS = [
    "Fecha",
    "Turno",
    "Producto",
    "Producidas",
    "Defectuosas",
]


def read_production_excel(
    file_path: str | Path,
    sheet_name: str = "produccion",
) -> pd.DataFrame:
    """
    Lee un archivo Excel de producción y comprueba sus columnas.

    Args:
        file_path: Ruta del archivo Excel.
        sheet_name: Nombre de la hoja que se debe leer.

    Returns:
        Un DataFrame con los datos del archivo.

    Raises:
        FileNotFoundError: Si el archivo no existe.
        ValueError: Si el archivo o su estructura no son válidos.
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"No se encontró el archivo: {path}"
        )

    if not path.is_file():
        raise ValueError(
            f"La ruta no corresponde a un archivo: {path}"
        )

    if path.suffix.lower() != ".xlsx":
        raise ValueError(
            "El archivo debe tener extensión .xlsx."
        )

    try:
        df = pd.read_excel(
            path,
            sheet_name=sheet_name,
            engine="openpyxl",
        )
    except ValueError as error:
        raise ValueError(
            f"No se pudo leer la hoja '{sheet_name}'. "
            "Comprueba que exista y que el archivo sea válido."
        ) from error

    # Elimina espacios accidentales en los encabezados.
    df.columns = df.columns.str.strip()

    missing_columns = [
        column
        for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:
        missing = ", ".join(missing_columns)
        raise ValueError(
            f"Faltan columnas obligatorias: {missing}"
        )

    # Conserva solamente las columnas definidas para esta fase.
    return df[REQUIRED_COLUMNS].copy()
