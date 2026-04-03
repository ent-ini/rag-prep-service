from __future__ import annotations

from pathlib import Path
from typing import Any

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import Response

from .extractors import UnsupportedFileTypeError, extract_bytes

app = FastAPI(title="rag-prep-service", version="0.1.0")


@app.post("/convert")
async def convert_file(file: UploadFile = File(...)) -> Any:
    try:
        contents = await file.read()
        doc = extract_bytes(file.filename or "file", contents)
        output_name = f"{Path(file.filename or 'document').stem}.md"
        headers = {"Content-Disposition": f'attachment; filename="{output_name}"'}
        return Response(content=doc.text.encode("utf-8"), media_type="text/markdown; charset=utf-8", headers=headers)
    except UnsupportedFileTypeError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
