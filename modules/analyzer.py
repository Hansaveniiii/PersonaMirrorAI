# =========================================================
# PERSONAMIRROR AI
# REAL VISUAL ANALYSIS ENGINE
# =========================================================

try:
    import cv2
    CV2_AVAILABLE = True
    CV2_ERROR = None
except Exception as e:
    cv2 = None
    CV2_AVAILABLE = False
    CV2_ERROR = str(e)


def clamp(value, minimum=0, maximum=100):
    try:
        return max(
            minimum,
            min(
                maximum,
                float(value)
            )
        )
    except (TypeError, ValueError):
        return None


def analyze_video(
    video_path,
    analysis_type="General Speech"
):

    # =====================================================
    # OpenCV unavailable
    # =====================================================

    if not CV2_AVAILABLE:

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

            "vision_error": CV2_ERROR,
        }


    cap = cv2.VideoCapture(video_path)


    # =====================================================
    # Video unavailable
    # =====================================================

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

            "vision_error": "Unable to open video.",
        }


    # =====================================================
    # Haar face detector
    # =====================================================

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


    # =====================================================
    # Eye detector
    # =====================================================

    eye_detector = cv2.CascadeClassifier(
        cv2.data.haarcascades
        + "haarcascade_eye.xml"
    )


    # =====================================================
    # Smile detector
    # =====================================================

    smile_detector = cv2.CascadeClassifier(
        cv2.data.haarcascades
        + "haarcascade_smile.xml"
    )


    # =====================================================
    # Sampling
    # =====================================================

    sample_every = 6
    max_process_frames = 400


    total_frames = 0
    face_frames = 0

    brightness_values = []

    face_center_values = []

    face_size_values = []

    eye_detected_frames = 0

    smile_detected_frames = 0

    face_widths = []
    face_heights = []


    previous_center = None
    movement_values = []


    frame_number = 0


    # =====================================================
    # PROCESS VIDEO
    # =====================================================

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
        # Resize
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


        frame_height, frame_width = frame.shape[:2]


        # -------------------------------------------------
        # Grayscale
        # -------------------------------------------------

        gray = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2GRAY
        )

        gray_equalized = cv2.equalizeHist(gray)


        # -------------------------------------------------
        # Brightness
        # -------------------------------------------------

        brightness_values.append(
            float(gray.mean())
        )


        # -------------------------------------------------
        # Face detection
        # -------------------------------------------------

        faces = face_detector.detectMultiScale(
            gray_equalized,
            scaleFactor=1.08,
            minNeighbors=5,
            minSize=(35, 35)
        )


        total_frames += 1


        if len(faces) == 0:
            continue


        # -------------------------------------------------
        # Select largest face
        # -------------------------------------------------

        face = max(
            faces,
            key=lambda box: box[2] * box[3]
        )


        x, y, w, h = face


        face_area = w * h

        frame_area = (
            frame_width
            * frame_height
        )


        face_ratio = (
            face_area / frame_area
        )


        # Ignore tiny detections
        if face_ratio < 0.008:
            continue


        face_frames += 1


        face_widths.append(w)
        face_heights.append(h)

        face_size_values.append(
            face_ratio
        )


        # =================================================
        # FACE CENTERING
        # =================================================

        face_center_x = (
            x + (w / 2)
        )

        face_center_y = (
            y + (h / 2)
        )


        normalized_x = (
            face_center_x
            / frame_width
        )


        normalized_y = (
            face_center_y
            / frame_height
        )


        # Ideal center = 0.5
        horizontal_error = abs(
            normalized_x - 0.5
        )

        vertical_error = abs(
            normalized_y - 0.5
        )


        centering_error = (
            horizontal_error * 0.7
            +
            vertical_error * 0.3
        )


        centering_score = (
            100
            -
            min(
                centering_error * 200,
                100
            )
        )


        face_center_values.append(
            centering_score
        )


        # =================================================
        # HEAD STABILITY
        # =================================================

        current_center = (
            normalized_x,
            normalized_y
        )


        if previous_center is not None:

            movement = (
                abs(
                    current_center[0]
                    - previous_center[0]
                )
                +
                abs(
                    current_center[1]
                    - previous_center[1]
                )
            )

            movement_values.append(
                movement
            )


        previous_center = current_center


        # =================================================
        # EYE DETECTION
        # =================================================

        face_roi = gray_equalized[
            y:y + h,
            x:x + w
        ]


        if (
            face_roi is not None
            and face_roi.size > 0
            and not eye_detector.empty()
        ):

            eyes = eye_detector.detectMultiScale(
                face_roi,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(15, 15)
            )


            # We only use this as a face-attention signal.
            # It is NOT claimed to be exact eye contact.
            if len(eyes) >= 1:

                eye_detected_frames += 1


        # =================================================
        # SMILE DETECTION
        # =================================================

        if (
            face_roi is not None
            and face_roi.size > 0
            and not smile_detector.empty()
        ):

            smiles = smile_detector.detectMultiScale(
                face_roi,
                scaleFactor=1.7,
                minNeighbors=20,
                minSize=(25, 15)
            )


            if len(smiles) > 0:

                smile_detected_frames += 1


    cap.release()


    # =====================================================
    # NO FRAMES
    # =====================================================

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


    # =====================================================
    # DETECTION RATIO
    # =====================================================

    detection_ratio = (
        face_frames
        / total_frames
    )


    # =====================================================
    # RELIABILITY
    # =====================================================

    face_detection_reliable = (
        detection_ratio >= 0.25
    )


    # =====================================================
    # FACE VISIBILITY
    # =====================================================

    if face_detection_reliable:

        visibility = round(
            detection_ratio * 100
        )

    else:

        visibility = None


    # =====================================================
    # BRIGHTNESS
    # =====================================================

    if brightness_values:

        brightness = round(
            sum(brightness_values)
            / len(brightness_values)
        )

    else:

        brightness = None


    # =====================================================
    # FACE CENTERING
    # =====================================================

    if face_center_values:

        face_centering = round(
            sum(face_center_values)
            / len(face_center_values)
        )

    else:

        face_centering = None


    # =====================================================
    # HEAD STABILITY
    # =====================================================

    if movement_values:

        average_movement = (
            sum(movement_values)
            / len(movement_values)
        )


        # Small movement = stable.
        # Excessive movement lowers score.

        head_stability = (
            100
            -
            min(
                average_movement * 450,
                100
            )
        )


        head_stability = round(
            head_stability
        )

    else:

        head_stability = None


    # =====================================================
    # EYE / FACE ATTENTION SIGNAL
    # =====================================================

    if (
        face_detection_reliable
        and face_frames > 0
        and eye_detector.empty() is False
    ):

        eye_ratio = (
            eye_detected_frames
            / face_frames
        )


        eye_contact = round(
            clamp(
                eye_ratio * 100
            )
        )

        eye_contact_available = True

    else:

        eye_contact = None
        eye_contact_available = False


    # =====================================================
    # SMILE
    # =====================================================

    if face_detection_reliable:

        smile_ratio = (
            smile_detected_frames
            / max(
                face_frames,
                1
            )
        )


        smile = round(
            clamp(
                smile_ratio * 100
            )
        )

    else:

        smile = None


    # =====================================================
    # ENGAGEMENT
    #
    # Engagement is based on:
    # - face visibility
    # - centering
    # - head stability
    #
    # It is deliberately NOT claimed to be emotion
    # recognition.
    # =====================================================

    engagement_components = []


    if visibility is not None:

        engagement_components.append(
            (visibility, 0.45)
        )


    if face_centering is not None:

        engagement_components.append(
            (face_centering, 0.30)
        )


    if head_stability is not None:

        engagement_components.append(
            (head_stability, 0.25)
        )


    if engagement_components:

        total_weight = sum(
            weight
            for _, weight
            in engagement_components
        )


        engagement = round(
            sum(
                value * weight
                for value, weight
                in engagement_components
            )
            / total_weight
        )

    else:

        engagement = None


    # =====================================================
    # IMPORTANT LIMITATIONS
    # =====================================================
    #
    # Haar cascades cannot reliably determine:
    #
    # - true eye contact
    # - body posture
    # - hand gestures
    #
    # Therefore posture and gesture remain unavailable
    # rather than inventing scores.
    # =====================================================

    posture = None
    gesture_score = None


    # =====================================================
    # RETURN
    # =====================================================

    return {

        "analysis_type": analysis_type,

        "frames": total_frames,

        "faces": face_frames,

        "visibility": visibility,

        "face_visibility": visibility,

        "brightness": brightness,

        "face_centering": face_centering,

        "head_stability": head_stability,

        "engagement": engagement,

        "eye_contact": eye_contact,

        "smile": smile,

        "posture": posture,

        "gesture_score": gesture_score,

        "vision_available": True,

        "eye_contact_available":
            eye_contact_available,

        "posture_available": False,

        "gesture_available": False,

        "face_detection_reliable":
            face_detection_reliable,
    }