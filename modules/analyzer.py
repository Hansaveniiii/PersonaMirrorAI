import cv2


# =========================================================
# PERSONAMIRROR AI
# VISUAL ANALYSIS ENGINE
# =========================================================

def analyze_video(
    video_path,
    analysis_type="General Speech"
):

    cap = cv2.VideoCapture(video_path)

    # -----------------------------------------------------
    # Video unavailable
    # -----------------------------------------------------

    if not cap.isOpened():

        return {
            "analysis_type": analysis_type,
            "frames": 0,
            "faces": 0,
            "visibility": None,
            "face_visibility": None,
            "brightness": None,
            "face_centering": None,
            "head_stability": None,
            "engagement": None,
            "eye_contact": None,
            "smile": None,
            "posture": None,
            "gesture_score": None,

            "vision_available": False,
            "eye_contact_available": False,
            "posture_available": False,
            "gesture_available": False,

            "face_detection_reliable": False,
        }


    # -----------------------------------------------------
    # Face detector
    # -----------------------------------------------------

    face_detector = cv2.CascadeClassifier(
        cv2.data.haarcascades
        + "haarcascade_frontalface_default.xml"
    )


    if face_detector.empty():

        cap.release()

        return {
            "analysis_type": analysis_type,
            "frames": 0,
            "faces": 0,
            "visibility": None,
            "face_visibility": None,
            "brightness": None,

            "face_centering": None,
            "head_stability": None,
            "engagement": None,
            "eye_contact": None,
            "smile": None,
            "posture": None,
            "gesture_score": None,

            "vision_available": False,
            "eye_contact_available": False,
            "posture_available": False,
            "gesture_available": False,

            "face_detection_reliable": False,
        }


    # -----------------------------------------------------
    # Sampling
    #
    # We process enough frames to get a meaningful estimate
    # without analyzing every single frame.
    # -----------------------------------------------------

    sample_every = 8

    max_process_frames = 300


    total_frames = 0
    face_frames = 0

    brightness_total = 0

    face_sizes = []


    frame_number = 0


    # -----------------------------------------------------
    # Process video
    # -----------------------------------------------------

    while True:

        ret, frame = cap.read()

        if not ret:
            break


        frame_number += 1


        if frame_number % sample_every != 0:
            continue


        if total_frames >= max_process_frames:
            break


        # -------------------------------------------------
        # Resize while preserving aspect ratio
        # -------------------------------------------------

        height, width = frame.shape[:2]

        if width > 640:

            scale = 640 / width

            frame = cv2.resize(
                frame,
                (
                    640,
                    int(height * scale)
                )
            )


        gray = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2GRAY
        )


        # Improve detection under uneven lighting
        gray = cv2.equalizeHist(gray)


        brightness_total += float(
            gray.mean()
        )


        # -------------------------------------------------
        # Multi-scale face detection
        # -------------------------------------------------

        faces = face_detector.detectMultiScale(
            gray,
            scaleFactor=1.08,
            minNeighbors=5,
            minSize=(35, 35)
        )


        if len(faces) > 0:

            # Choose the largest detected face.
            # In a single-speaker recording this is usually
            # the speaker's face.

            largest_face = max(
                faces,
                key=lambda box: box[2] * box[3]
            )


            x, y, w, h = largest_face


            face_area = w * h

            frame_area = (
                frame.shape[0]
                * frame.shape[1]
            )


            face_ratio = (
                face_area / frame_area
            )


            # Ignore extremely tiny detections.
            if face_ratio >= 0.008:

                face_frames += 1

                face_sizes.append(
                    face_ratio
                )


        total_frames += 1


    cap.release()


    # -----------------------------------------------------
    # No usable frames
    # -----------------------------------------------------

    if total_frames == 0:

        return {
            "analysis_type": analysis_type,
            "frames": 0,
            "faces": 0,

            "visibility": None,
            "face_visibility": None,
            "brightness": None,

            "face_centering": None,
            "head_stability": None,
            "engagement": None,

            "eye_contact": None,
            "smile": None,
            "posture": None,
            "gesture_score": None,

            "vision_available": False,

            "eye_contact_available": False,
            "posture_available": False,
            "gesture_available": False,

            "face_detection_reliable": False,
        }


    # -----------------------------------------------------
    # Face detection coverage
    # -----------------------------------------------------

    detection_ratio = (
        face_frames / total_frames
    )


    # -----------------------------------------------------
    # Reliability
    #
    # We only call the measurement reliable when there
    # are enough detected frames.
    # -----------------------------------------------------

    if detection_ratio >= 0.60:

        face_detection_reliable = True

    elif detection_ratio >= 0.25:

        face_detection_reliable = True

    else:

        face_detection_reliable = False


    # -----------------------------------------------------
    # Face visibility
    #
    # IMPORTANT:
    #
    # This represents detected-face coverage.
    # It does NOT claim to measure audience eye contact.
    # -----------------------------------------------------

    if face_detection_reliable:

        visibility = round(
            detection_ratio * 100
        )

    else:

        visibility = None


    # -----------------------------------------------------
    # Brightness
    # -----------------------------------------------------

    brightness = round(
        brightness_total / total_frames
    )


    # -----------------------------------------------------
    # Result
    # -----------------------------------------------------

    return {

        "analysis_type": analysis_type,

        "frames": total_frames,

        "faces": face_frames,

        "visibility": visibility,

        "face_visibility": visibility,

        "brightness": brightness,


        # -------------------------------------------------
        # These require dedicated models and are therefore
        # not fabricated here.
        # -------------------------------------------------

        "face_centering": None,

        "head_stability": None,

        "engagement": None,

        "eye_contact": None,

        "smile": None,

        "posture": None,

        "gesture_score": None,


        "vision_available": True,

        "eye_contact_available": False,

        "posture_available": False,

        "gesture_available": False,

        "face_detection_reliable":
            face_detection_reliable,
    }