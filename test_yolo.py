import time
import dxcam

from core.detector import BallDetector

def main():

```
print("=" * 60)
print("YOLO TEST STARTED")
print("=" * 60)

detector = BallDetector()

camera = dxcam.create(
    output_idx=0,
    output_color="BGR"
)

camera.start(target_fps=30)

frame_count = 0
last_time = time.time()

while True:

    frame = camera.get_latest_frame()

    if frame is None:
        continue

    detections = detector.detect(frame)

    frame_count += 1

    if time.time() - last_time >= 1:

        print("\n" + "=" * 60)
        print("FPS:", frame_count)
        print("DETECTIONS:", len(detections))

        counts = {}

        for det in detections:

            cls = det["class_name"]

            counts[cls] = counts.get(cls, 0) + 1

        for cls, cnt in counts.items():
            print(f"{cls}: {cnt}")

        print("=" * 60)

        frame_count = 0
        last_time = time.time()
```

if **name** == "**main**":
main()
