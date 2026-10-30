
import pandas as pd


def validate_production_data(
    df: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Separa los registros válidos de los que requieren revisión.

    Devuelve:
        - DataFrame con registros válidos.
        - DataFrame con registros inválidos y sus errores.
    """
    data = df.copy()

    # Conserva el número de fila del Excel para localizar errores.
    data.insert(0, "Fila_excel", range(2, len(data) + 2))

    errors = pd.Series("", index=data.index, dtype="string")

    # Validar campos obligatorios.
    required_fields = [
        "Fecha",
        "Turno",
        "Producto",
        "Producidas",
        "Defectuosas",
    ]

    for column in required_fields:
        missing = (
            data[column].isna()
            | data[column].astype("string").str.strip().eq("").fillna(False)
        )
        errors.loc[missing] += f"{column} está vacío; "

    # Validar fechas.
    dates = pd.to_datetime(data["Fecha"], errors="coerce")
    invalid_dates = dates.isna() & data["Fecha"].notna()
    errors.loc[invalid_dates] += "Fecha inválida; "

    # Convertir cantidades y detectar valores no numéricos.
    for column in ["Producidas", "Defectuosas"]:
        original = data[column]
        numeric = pd.to_numeric(original, errors="coerce")

        invalid_numeric = numeric.isna() & original.notna()
        errors.loc[invalid_numeric] += f"{column} no es numérico; "

        negative = numeric.lt(0).fillna(False)
        errors.loc[negative] += f"{column} no puede ser negativo; "

        non_integer = (
            numeric.notna()
            & numeric.mod(1).ne(0)
        )
        errors.loc[non_integer] += f"{column} debe ser entero; "

        data[column] = numeric

    # Los defectos no pueden superar la producción.
    impossible = (
        data["Producidas"].notna()
        & data["Defectuosas"].notna()
        & data["Defectuosas"].gt(data["Producidas"])
    )
    errors.loc[impossible] += (
        "Defectuosas supera las unidades producidas; "
    )

    # Normalizar las fechas válidas.
    data["Fecha"] = dates

    # Clasificar registros.
    invalid_mask = errors.ne("")
    valid_data = data.loc[~invalid_mask].copy()
    invalid_data = data.loc[invalid_mask].copy()

    invalid_data["Errores"] = errors.loc[invalid_mask].str.rstrip("; ")

    return valid_data, invalid_data
