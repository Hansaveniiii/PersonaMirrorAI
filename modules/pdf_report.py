from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import os

def generate_pdf(result):

    os.makedirs("reports", exist_ok=True)

    filename = "reports/PersonaMirror_Report.pdf"

    doc = SimpleDocTemplate(filename)
    styles = getSampleStyleSheet()

    story = []

    story.append(Paragraph("<b>PersonaMirror AI Report</b>", styles["Title"]))

    story.append(Paragraph(f"Confidence: {result['confidence']}%", styles["Normal"]))
    story.append(Paragraph(f"Leadership: {result['leadership']}%", styles["Normal"]))
    story.append(Paragraph(f"Eye Contact: {result['eye_contact']}%", styles["Normal"]))
    story.append(Paragraph(f"Emotion: {result['emotion']}", styles["Normal"]))
    story.append(Paragraph(f"Speech Speed: {result['speech']} WPM", styles["Normal"]))
    story.append(Paragraph(f"Visibility: {result['visibility']}%", styles["Normal"]))

    story.append(Paragraph("<br/><b>Transcript</b>", styles["Heading2"]))
    story.append(Paragraph(result["transcript"], styles["Normal"]))

    doc.build(story)

    return filename