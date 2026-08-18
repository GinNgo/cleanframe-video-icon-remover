from __future__ import annotations

import shutil
import tempfile
from pathlib import Path

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from starlette.background import BackgroundTask

from app.core import VideoToolError, normalize_region, probe_video, process_video, sha256_file, write_audit_event

BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "app" / "static"
AUDIT_LOG = BASE_DIR / "data" / "audit.jsonl"
SUPPORTED_EXTENSIONS = {".mp4", ".mov", ".m4v", ".webm"}
MAX_UPLOAD_BYTES = 2 * 1024 * 1024 * 1024

app = FastAPI(title="CleanFrame", docs_url=None, redoc_url=None)


def remove_tree(path: Path) -> None:
    shutil.rmtree(path, ignore_errors=True)


@app.post("/api/process")
async def process_upload(
    video: UploadFile = File(...),
    x: int = Form(...),
    y: int = Form(...),
    width: int = Form(...),
    height: int = Form(...),
    mask_shape: str = Form("diamond"),
    rights_attested: bool = Form(False),
):
    if not rights_attested:
        raise HTTPException(403, "You must confirm ownership or explicit edit permission")
    suffix = Path(video.filename or "").suffix.lower()
    if suffix not in SUPPORTED_EXTENSIONS:
        raise HTTPException(415, "Supported formats: MP4, MOV, M4V, WebM")

    work_dir = Path(tempfile.mkdtemp(prefix="cleanframe-"))
    source = work_dir / f"source{suffix}"
    output = work_dir / "cleanframe-output.mp4"
    total = 0
    try:
        with source.open("wb") as destination:
            while chunk := await video.read(1024 * 1024):
                total += len(chunk)
                if total > MAX_UPLOAD_BYTES:
                    raise HTTPException(413, "Video exceeds the 2 GiB limit")
                destination.write(chunk)
        info = probe_video(source)
        region = normalize_region(x, y, width, height, info)
        checksum = sha256_file(source)
        process_video(source, output, region, info, mask_shape)
        write_audit_event(AUDIT_LOG, video.filename or source.name, checksum, info, region, mask_shape)
    except HTTPException:
        remove_tree(work_dir)
        raise
    except VideoToolError as exc:
        remove_tree(work_dir)
        raise HTTPException(422, str(exc)) from exc
    except Exception:
        remove_tree(work_dir)
        raise
    finally:
        await video.close()

    return FileResponse(
        output,
        media_type="video/mp4",
        filename=f"cleaned-{Path(video.filename or 'video').stem}.mp4",
        background=BackgroundTask(remove_tree, work_dir),
    )


app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="static")
