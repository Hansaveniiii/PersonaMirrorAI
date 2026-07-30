import cv2


def analyze_eye_contact(video_path):

    cap = cv2.VideoCapture(video_path)

    total_frames = 0
    looking_frames = 0

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        total_frames += 1

        # Placeholder eye tracking logic
        # Real MediaPipe Tasks integration will be added next

        gray = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2GRAY
        )

        brightness = gray.mean()

        if brightness > 30:
            looking_frames += 1


    cap.release()


    if total_frames == 0:
        return 0


    eye_contact_score = int(
        (looking_frames / total_frames) * 100
    )


    return eye_contact_score