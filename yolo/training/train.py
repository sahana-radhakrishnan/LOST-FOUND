from pathlib import Path
import argparse

from ultralytics import YOLO


ROOT = Path(__file__).resolve().parents[1]

CONFIG_PATH = ROOT / "training" / "config.yaml"
MODELS_DIR = ROOT / "models"


def train_model(
    config_path=CONFIG_PATH,
    model_name="yolov8n.pt",
    epochs=50,
    batch=16,
    imgsz=640,
):
    MODELS_DIR.mkdir(parents=True, exist_ok=True)

    model = YOLO(model_name)

    results = model.train(
        data=str(config_path),
        epochs=epochs,
        batch=batch,
        imgsz=imgsz,
        project=str(MODELS_DIR / "runs"),
        name="lost_found",
        exist_ok=True,
    )

    best_weights = Path(results.save_dir) / "weights" / "best.pt"

    if not best_weights.exists():
        raise FileNotFoundError(
            f"Training completed, but best.pt was not found at {best_weights}"
        )

    destination = MODELS_DIR / "best.pt"

    destination.write_bytes(best_weights.read_bytes())

    print("\nTraining completed!")
    print(f"Best model saved to: {destination}")

    return destination


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--config",
        default=str(CONFIG_PATH)
    )

    parser.add_argument(
        "--model",
        default="yolov8n.pt"
    )

    parser.add_argument(
        "--epochs",
        type=int,
        default=50
    )

    parser.add_argument(
        "--batch",
        type=int,
        default=16
    )

    parser.add_argument(
        "--imgsz",
        type=int,
        default=640
    )

    args = parser.parse_args()

    train_model(
        config_path=args.config,
        model_name=args.model,
        epochs=args.epochs,
        batch=args.batch,
        imgsz=args.imgsz,
    )