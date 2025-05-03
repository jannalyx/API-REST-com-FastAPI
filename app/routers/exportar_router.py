from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
import zipfile
import os
from pathlib import Path

router = APIRouter(prefix="/exportar", tags=["Exportação"])

@router.get("/zip", summary="Exportar CSVs em ZIP")
def exportar_csv_zip():
    try:
        base_dir = Path(__file__).resolve().parent.parent
        pasta_csv = base_dir / "csv"

        arquivos_csv = [
            pasta_csv / "usuarios.csv",
            pasta_csv / "livros.csv",
            pasta_csv / "pedidos.csv",
        ]

        zip_path = pasta_csv / "exportacao.zip"

        with zipfile.ZipFile(zip_path, "w") as zipf:
            for arquivo in arquivos_csv:
                if arquivo.exists():
                    zipf.write(arquivo, arcname=arquivo.name)
                else:
                    raise FileNotFoundError(f"Arquivo não encontrado: {arquivo.name}")

        return FileResponse(
            path=zip_path,
            filename="exportacao.zip",
            media_type="application/zip"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar ZIP: {str(e)}")
