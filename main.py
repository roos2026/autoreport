
from pathlib import Path

from src.reader import read_production_excel
from src.validator import validate_production_data


BASE_DIR = Path(__file__).resolve().parent
INPUT_FILE = BASE_DIR / "data" / "input" / "produccion_turno.xlsx"


def main() -> None:
    try:
        df = read_production_excel(INPUT_FILE)

        valid_data, invalid_data = validate_production_data(df)

        print(f"Registros leídos: {len(df)}")
        print(f"Registros validos: {len(valid_data)}")
        print(f"Registros por revisar: {len(invalid_data)}")
      
        if not invalid_data.empty:
            print("\nRegistros inválidos:")
            print(invalid_data[["Fila_excel", "Errores"]].to_string(index=False))
        else:
            print("\nTodos los registros son válidos.")
            

    except (FileNotFoundError, ValueError, PermissionError) as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    main()
