from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[3]
YOLO_RESULTS_DIR = (PROJECT_ROOT / "yolo" / "results").resolve()


def _relative_image_path(image_path: str | None) -> Path | None:
    if not image_path:
        return None

    normalized = str(image_path).replace("\\", "/")
    marker = "/yolo/results/"
    lowered = normalized.lower()
    marker_index = lowered.find(marker)

    if marker_index >= 0:
        return Path(normalized[marker_index + len(marker):])

    if lowered.startswith("/results/"):
        return Path(normalized[len("/results/"):])

    if lowered.startswith("results/"):
        return Path(normalized[len("results/"):])

    if lowered.startswith("yolo/results/"):
        return Path(normalized[len("yolo/results/"):])

    return Path(normalized.lstrip("/"))


def resolve_image_path(image_path: str | None) -> Path | None:
    relative_path = _relative_image_path(image_path)
    if relative_path is None:
        return None

    candidate = (YOLO_RESULTS_DIR / relative_path).resolve()
    try:
        candidate.relative_to(YOLO_RESULTS_DIR)
    except ValueError:
        return None

    return candidate


def image_url(image_path: str | None) -> str | None:
    resolved = resolve_image_path(image_path)
    if resolved is None or not resolved.is_file():
        return None

    relative_path = resolved.relative_to(YOLO_RESULTS_DIR).as_posix()
    return f"/media/{relative_path}"
