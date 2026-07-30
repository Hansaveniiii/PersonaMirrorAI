import cv2


def analyze_smile(video_path):
    face_detector = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

    smile_detector = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_smile.xml"
    )

    cap = cv2.VideoCapture(video_path)

    total_faces = 0
    smiling_faces = 0

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_detector.detectMultiScale(
            gray,
            1.3,
            5
        )

        for (x, y, w, h) in faces:

            total_faces += 1

            roi = gray[y:y+h, x:x+w]

            smiles = smile_detector.detectMultiScale(
                roi,
                scaleFactor=1.8,
                minNeighbors=20
            )

            if len(smiles) > 0:
                smiling_faces += 1

    cap.release()

    if total_faces == 0:
        return {
            "smile": 0
        }

    score = int(smiling_faces / total_faces * 100)

    return {
        "smile": score
    }