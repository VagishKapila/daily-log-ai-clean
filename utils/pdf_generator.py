from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph
import os
from datetime import datetime
from PIL import Image
import io

def compress_image(image_path, max_size=(1024, 1024)):
    img = Image.open(image_path)
    img.thumbnail(max_size)
    compressed_io = io.BytesIO()
    img.save(compressed_io, format='JPEG', quality=70)
    compressed_io.seek(0)
    return compressed_io

def draw_text_block(c, x, y, text, title="", font_size=12, max_width=500):
    styles = getSampleStyleSheet()
    style = styles['Normal']
    style.fontSize = font_size
    if title:
        c.setFont("Helvetica-Bold", font_size + 1)
        c.drawString(x, y, title)
        y -= 16
    para = Paragraph(text.replace("\n", "<br/>"), style)
    w, h = para.wrap(max_width, 100)
    para.drawOn(c, x, y - h)
    return y - h - 10

def create_daily_log_pdf(output_path, data, image_paths, logo_path=None):
    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4
    margin = 40
    y = height - margin

    # Logo
    if logo_path and os.path.exists(logo_path):
        logo = ImageReader(logo_path)
        c.drawImage(logo, width - 120, height - 80, width=80, preserveAspectRatio=True)

    c.setFont("Helvetica-Bold", 16)
    c.setFillColor(colors.HexColor("#1E90FF"))
    c.drawString(margin, y, "DAILY LOG")
    y -= 40

    c.setFillColor(colors.black)
    c.setFont("Helvetica", 10)
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.drawString(margin, y, f"Date: {date_str}")
    y -= 20

    if data:
        y = draw_text_block(c, margin, y, data.get("crew_notes", ""), "Crew Notes", 11)
        y = draw_text_block(c, margin, y, data.get("work_done", ""), "Work Done", 11)
        y = draw_text_block(c, margin, y, data.get("safety_notes", ""), "Safety Notes", 11)
        y = draw_text_block(c, margin, y, data.get("weather", ""), "Weather", 11)
        y = draw_text_block(c, margin, y, data.get("equipment", ""), "Equipment Used", 11)

    c.setFillColor(colors.grey)
    c.setFont("Helvetica-Oblique", 8)
    c.drawRightString(width - margin, margin, "Powered by Nails & Notes")

    c.showPage()

    # Page 2 – Photos
    c.setFont("Helvetica-Bold", 14)
    c.drawString(margin, height - margin, "Job Site Photos")

    if image_paths:
        x_offset = margin
        y_offset = height - 80
        img_width = (width - 3 * margin) / 2
        img_height = img_width * 0.75

        for idx, path in enumerate(image_paths):
            compressed = compress_image(path)
            img = ImageReader(compressed)
            c.drawImage(img, x_offset, y_offset - img_height, width=img_width, height=img_height)

            if (idx + 1) % 2 == 0:
                x_offset = margin
                y_offset -= img_height + 20
                if y_offset < margin + img_height:
                    c.showPage()
                    y_offset = height - margin - 40
                    c.setFont("Helvetica-Bold", 14)
                    c.drawString(margin, height - margin, "Job Site Photos Continued")
            else:
                x_offset += img_width + margin

    c.showPage()

    # Page 3 – AI/AR placeholder
    c.setFont("Helvetica-Bold", 14)
    c.drawString(margin, height - margin, "AI/AR Analysis & Material Insights")
    c.setFont("Helvetica", 11)
    c.drawString(margin, height - margin - 30, "📌 This page will include future overlays from AR and AI captioning models.")

    c.save()