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
        raise RuntimeError(
            f"Failed to load image: {image_path}"
        )

    print("IMAGE:", image.shape)

    detector = BallDetector()

    detections = detector.detect(image)

    print()
    print("TOTAL DETECTIONS:", len(detections))
    print()

    class_counter = {}

    for det in detections:

        cls = det["class_name"]

        class_counter[cls] = (
            class_counter.get(cls, 0) + 1
        )

        x1, y1, x2, y2 = det["bbox"]

        cv2.rectangle(
            image,
            (x1, y1),
            (x2, y2),
            (0, 255, 0),
            2
        )

        cv2.putText(
            image,
            cls,
            (x1, y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 0),
            2
        )

    print("CLASS COUNTS")
    print("-" * 30)

    for cls, count in class_counter.items():
        print(f"{cls}: {count}")

    output_path = "result.jpg"

    cv2.imwrite(
        output_path,
        image
    )

    print()
    print("RESULT IMAGE SAVED:", output_path)
    print()

    print("=" * 60)
    print("YOLO TEST FINISHED")
    print("=" * 60)


if __name__ == "__main__":
    main()
