import cv2
import mediapipe as mp

mp_face_mesh = mp.solutions.face_mesh


def analyze_eye_contact(video_path):

    face_mesh = mp_face_mesh.FaceMesh(
        static_image_mode=False,
        max_num_faces=1,
        refine_landmarks=True
    )

    cap = cv2.VideoCapture(video_path)

    total_frames = 0
    eye_contact_frames = 0

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        total_frames += 1

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = face_mesh.process(rgb)

        if results.multi_face_landmarks:
            eye_contact_frames += 1

    cap.release()

    face_mesh.close()

    if total_frames == 0:
        return 0

    return round((eye_contact_frames / total_frames) * 100)