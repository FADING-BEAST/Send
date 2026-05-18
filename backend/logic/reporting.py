import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

def generate_student_report(student, analysis, records, factors):
    """Generates a PDF report for an individual student."""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []

    # Title
    elements.append(Paragraph(f"Academic Risk Profile: {student.name}", styles['Title']))
    elements.append(Spacer(1, 12))

    # Bio Info
    elements.append(Paragraph(f"<b>Student ID:</b> {student.student_id}", styles['Normal']))
    elements.append(Paragraph(f"<b>Level:</b> {student.level}", styles['Normal']))
    elements.append(Paragraph(f"<b>Risk Category:</b> {analysis.risk_category if analysis else 'Low'}", styles['Normal']))
    elements.append(Spacer(1, 12))

    # Risk Factors
    elements.append(Paragraph("<b>Identified Risk Factors:</b>", styles['Heading3']))
    if factors:
        for f in factors:
            elements.append(Paragraph(f"• {f}", styles['Normal']))
    else:
        elements.append(Paragraph("No significant risk factors identified.", styles['Normal']))
    elements.append(Spacer(1, 20))

    # Academic History Table
    elements.append(Paragraph("<b>Academic History:</b>", styles['Heading3']))
    data = [['Session', 'Sem', 'Course', 'Grade', 'Score']]
    for r in records:
        data.append([r['session'], r['semester'], r['code'], r['grade'], r['score']])

    t = Table(data)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(t)
    
    # Build PDF
    doc.build(elements)
    
    buffer.seek(0)
    return buffer


def generate_cohort_report():
    """Generates a cohort-level risk summary PDF."""
    from backend.models import Student, RiskAnalysis
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph("Cohort Academic Risk Summary Report", styles['Title']))
    elements.append(Spacer(1, 8))

    high = RiskAnalysis.query.filter_by(risk_category='High').count()
    med = RiskAnalysis.query.filter_by(risk_category='Medium').count()
    low = RiskAnalysis.query.filter_by(risk_category='Low').count()
    total = Student.query.count()

    elements.append(Paragraph(f"<b>Total Students:</b> {total}", styles['Normal']))
    elements.append(Paragraph(f"<b>High Risk:</b> {high}", styles['Normal']))
    elements.append(Paragraph(f"<b>Medium Risk:</b> {med}", styles['Normal']))
    elements.append(Paragraph(f"<b>Low Risk / Clear:</b> {low}", styles['Normal']))
    elements.append(Spacer(1, 20))

    elements.append(Paragraph("<b>High-Risk Student Register</b>", styles['Heading3']))
    high_analyses = RiskAnalysis.query.filter_by(risk_category='High').all()
    data = [['Student ID', 'Name', 'Risk Score']]
    for a in high_analyses:
        s = Student.query.get(a.student_db_id)
        if s:
            data.append([s.student_id, s.name, f"{a.risk_score:.2f}"])

    t = Table(data)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.red),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lightyellow),
    ]))
    elements.append(t)
    doc.build(elements)
    buffer.seek(0)
    return buffer
