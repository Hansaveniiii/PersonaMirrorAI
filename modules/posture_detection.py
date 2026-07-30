import cv2


def analyze_posture(video_path):
    cap = cv2.VideoCapture(video_path)

    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

    frames = 0
    upright = 0

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        frames += 1

        boxes, _ = hog.detectMultiScale(
            frame,
            winStride=(8, 8)
        )

        if len(boxes) > 0:
            upright += 1

    cap.release()

    if frames == 0:
        return {"posture": 0}

    posture = int((upright / frames) * 100)

    return {
        "posture": posture
    }