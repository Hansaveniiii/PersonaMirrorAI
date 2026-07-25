import cv2


def detect_faces(video_path):

    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

    cap = cv2.VideoCapture(video_path)

    total_frames = 0
    total_faces = 0
    max_faces = 0
    frames_with_face = 0

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        total_frames += 1

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(60, 60)
        )

        count = len(faces)

        total_faces += count

        if count > 0:
            frames_with_face += 1

        if count > max_faces:
            max_faces = count

    cap.release()

    average_faces = (
        total_faces / total_frames if total_frames else 0
    )

    face_visibility = (
        (frames_with_face / total_frames) * 100
        if total_frames else 0
    )

    return {
        "frames": total_frames,
        "faces": max_faces,
        "average_faces": round(average_faces, 2),
        "visibility": round(face_visibility, 2)
    }