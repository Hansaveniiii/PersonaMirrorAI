import cv2


def analyze_eye_contact(video_path):

    cap = cv2.VideoCapture(video_path)

    face_detector = cv2.CascadeClassifier(
        cv2.data.haarcascades +
        "haarcascade_frontalface_default.xml"
    )

    total_frames = 0
    looking_frames = 0

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        total_frames += 1

        gray = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2GRAY
        )

        faces = face_detector.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(50, 50)
        )

        if len(faces) > 0:
            looking_frames += 1

    cap.release()

    if total_frames == 0:
        return 0

    return int((looking_frames / total_frames) * 100)