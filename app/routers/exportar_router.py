from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
import zipfile
import os
from pathlib import Path
from datetime import datetime
from app.utils.logger import logger 

router = APIRouter(prefix="/exportar", tags=["Exportação"])

@router.get("/zip", summary="Exportar CSVs em ZIP")
def exportar_csv_zip():
    try:
        base_dir = Path(__file__).resolve().parent.parent.parent
        pasta_csv = base_dir / "csv"

        if not pasta_csv.exists():
            os.makedirs(pasta_csv)
            logger.info(f"[Exportação] Pasta 'csv' criada em: {pasta_csv}")

        arquivos_csv = [
            pasta_csv / "usuarios.csv",
            pasta_csv / "livros.csv",
            pasta_csv / "pedidos.csv",
        ]

        nome_zip = f"exportacao_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
        zip_path = pasta_csv / nome_zip

        with zipfile.ZipFile(zip_path, "w") as zipf:
            for arquivo in arquivos_csv:
                if arquivo.exists():
                    zipf.write(arquivo, arcname=arquivo.name)
                    logger.info(f"[Exportação] Arquivo adicionado ao ZIP: {arquivo.name}")
                else:
                    logger.error(f"[Exportação] Arquivo não encontrado: {arquivo.name}")
                    raise FileNotFoundError(f"Arquivo não encontrado: {arquivo.name}")

        logger.info(f"[Exportação] ZIP gerado com sucesso: {zip_path.name}")
        return FileResponse(
            path=zip_path,
            filename=nome_zip,
            media_type="application/zip"
        )

    except Exception as e:
        logger.error(f"[Exportação] Erro ao gerar ZIP: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao gerar ZIP: {str(e)}")
