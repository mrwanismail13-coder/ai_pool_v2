from pathlib import Path
import cv2

from core.detector import BallDetector


def main():

    print("=" * 60)
    print("YOLO TEST START")
    print("=" * 60)

    image_path = Path("test_images/test.jpg")

    if not image_path.exists():
        raise FileNotFoundError(
            f"Test image not found: {image_path}"
        )

    image = cv2.imread(str(image_path))

    if image is None:
        raise RuntimeError("Failed to load image")

    print("IMAGE SHAPE:", image.shape)

    detector = BallDetector()

    detections = detector.detect(image)

    print()
    print("TOTAL DETECTIONS:", len(detections))
    print()

    for i, det in enumerate(detections, start=1):

        print(
            f"[{i}] "
            f"{det['class_name']} "
            f"conf={det['confidence']:.2f} "
            f"center={det['center']}"
        )

    print()
    print("=" * 60)
    print("YOLO TEST FINISHED")
    print("=" * 60)


if __name__ == "__main__":
    main()
