import cv2


def analyze_gesture(video_path):
    cap = cv2.VideoCapture(video_path)

    ret, prev = cap.read()

    if not ret:
        return {"gesture_score": 0}

    prev = cv2.cvtColor(prev, cv2.COLOR_BGR2GRAY)

    movement = 0
    frames = 0

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        diff = cv2.absdiff(prev, gray)

        score = diff.mean()

        movement += score
        frames += 1

        prev = gray

    cap.release()

    if frames == 0:
        return {"gesture_score": 0}

    avg = movement / frames

    gesture = min(100, int(avg * 2))

    return {
        "gesture_score": gesture
    }