from __future__ import annotations

import hashlib
import json
import subprocess
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


class VideoToolError(RuntimeError):
    pass


@dataclass(frozen=True)
class VideoInfo:
    width: int
    height: int
    fps: float
    duration: float
    video_bitrate: int | None
    has_audio: bool


def _run(command: list[str]) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(command, capture_output=True, text=True, check=True)
    except FileNotFoundError as exc:
        raise VideoToolError(f"Missing required executable: {command[0]}") from exc
    except subprocess.CalledProcessError as exc:
        message = exc.stderr.strip() or exc.stdout.strip() or "Media command failed"
        raise VideoToolError(message[-2000:]) from exc


def probe_video(path: Path) -> VideoInfo:
    result = _run([
        "ffprobe", "-v", "error", "-show_streams", "-show_format",
        "-of", "json", str(path),
    ])
    payload = json.loads(result.stdout)
    video = next((s for s in payload.get("streams", []) if s.get("codec_type") == "video"), None)
    if not video:
        raise VideoToolError("The uploaded file has no video stream")
    rate = video.get("avg_frame_rate") or video.get("r_frame_rate") or "0/1"
    numerator, denominator = (int(part) for part in rate.split("/"))
    fps = numerator / denominator if denominator else 0.0
    duration = float(video.get("duration") or payload.get("format", {}).get("duration") or 0)
    bitrate_value = video.get("bit_rate") or payload.get("format", {}).get("bit_rate")
    return VideoInfo(
        width=int(video["width"]),
        height=int(video["height"]),
        fps=fps,
        duration=duration,
        video_bitrate=int(bitrate_value) if bitrate_value else None,
        has_audio=any(s.get("codec_type") == "audio" for s in payload.get("streams", [])),
    )


def normalize_region(x: int, y: int, width: int, height: int, info: VideoInfo) -> tuple[int, int, int, int]:
    values = [max(0, value - (value % 2)) for value in (x, y, width, height)]
    nx, ny, nw, nh = values
    if nw < 8 or nh < 8:
        raise VideoToolError("Selection must be at least 8 x 8 pixels")
    if nx + nw > info.width or ny + nh > info.height:
        raise VideoToolError("Selection extends outside the video frame")
    return nx, ny, nw, nh


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def process_video(source: Path, output: Path, region: tuple[int, int, int, int], info: VideoInfo) -> None:
    x, y, width, height = region
    bitrate_args = ["-b:v", str(info.video_bitrate)] if info.video_bitrate else ["-crf", "18"]
    command = [
        "ffmpeg", "-y", "-v", "error", "-i", str(source),
        "-vf", f"delogo=x={x}:y={y}:w={width}:h={height}:show=0",
        "-c:v", "libx264", "-preset", "medium", *bitrate_args,
        "-pix_fmt", "yuv420p", "-map", "0:v:0", "-map", "0:a?",
        "-c:a", "copy", "-map_metadata", "0", "-movflags", "+faststart", str(output),
    ]
    _run(command)


def write_audit_event(log_path: Path, source_name: str, checksum: str, info: VideoInfo, region: tuple[int, int, int, int]) -> None:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    event = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event": "AUTHORIZED_ICON_REMOVAL",
        "source_name": source_name,
        "source_sha256": checksum,
        "width": info.width,
        "height": info.height,
        "fps": info.fps,
        "duration": info.duration,
        "region": {"x": region[0], "y": region[1], "width": region[2], "height": region[3]},
        "rights_attested": True,
    }
    with log_path.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(event, ensure_ascii=True) + "\n")

