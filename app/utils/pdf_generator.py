import io
import os
import base64
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from reportlab.graphics.barcode import code128
from PIL import Image
from django.conf import settings

def generate_ticket_pdf(booking, event_tickets):
    """
    Generates a premium PDF byte stream containing the tickets for a booking,
    designed to match the "Your E-Tickets" UI modal.
    """
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Design System Colors
    PRIMARY_GREEN = colors.HexColor("#145c47")
    TEXT_DARK = colors.HexColor("#0f172a")
    TEXT_LIGHT = colors.HexColor("#64748b")
    BG_LIGHT = colors.HexColor("#f1f5f9")
    DIVIDER_COLOR = colors.HexColor("#e2e8f0")
    WHITE = colors.white

    # Card Dimensions
    CARD_W = 4.8 * inch
    CARD_H = 7.8 * inch
    CARD_X = (width - CARD_W) / 2
    CARD_Y = (height - CARD_H) / 2

    for idx, ticket in enumerate(event_tickets):
        if idx > 0:
            p.showPage()

        # --- 1. Background & Border ---
        p.saveState()
        # Subtle "Shadow"
        p.setStrokeColor(colors.transparent)
        p.setFillColor(colors.black, alpha=0.05)
        p.roundRect(CARD_X + 2, CARD_Y - 2, CARD_W, CARD_H, 20, stroke=0, fill=1)
        
        # Main Card
        p.setStrokeColor(DIVIDER_COLOR)
        p.setLineWidth(1)
        p.setFillColor(WHITE)
        p.roundRect(CARD_X, CARD_Y, CARD_W, CARD_H, 20, stroke=1, fill=1)
        p.restoreState()

        # --- 2. Header Image ---
        img_h = 3.0 * inch
        p.saveState()
        # Clip top section
        clip_path = p.beginPath()
        clip_path.roundRect(CARD_X, CARD_Y + CARD_H - img_h, CARD_W, img_h, 20)
        p.clipPath(clip_path, stroke=0)
        
        img_path = None
        event_img_field = getattr(booking.event, 'image', None)
        if event_img_field:
            full_path = os.path.join(settings.MEDIA_ROOT, str(event_img_field))
            if os.path.exists(full_path):
                img_path = full_path
        
        if img_path:
            # Draw image with crop-center simulation
            p.drawImage(img_path, CARD_X, CARD_Y + CARD_H - img_h, width=CARD_W, height=img_h, preserveAspectRatio=True, anchor='c')
        else:
            p.setFillColor(PRIMARY_GREEN)
            p.rect(CARD_X, CARD_Y + CARD_H - img_h, CARD_W, img_h, stroke=0, fill=1)

        # Bottom Gradient Overlay
        p.saveState()
        for i in range(100):
            p.setFillColor(colors.black, alpha=(i/100.0) * 0.8)
            p.rect(CARD_X, CARD_Y + CARD_H - img_h, CARD_W, (img_h/2) * (1 - i/100.0), stroke=0, fill=1)
        p.restoreState()

        # Event Name (White)
        p.setFillColor(WHITE)
        p.setFont("Helvetica-Bold", 26)
        # Handle long names
        name = booking.event.event_name
        if len(name) > 25:
            p.setFont("Helvetica-Bold", 20)
        p.drawString(CARD_X + 0.35 * inch, CARD_Y + CARD_H - img_h + 0.5 * inch, name)
        p.restoreState()

        # --- 3. Price Badge ---
        p.saveState()
        badge_w = 0.9 * inch
        badge_h = 0.45 * inch
        badge_x = CARD_X + CARD_W - badge_w - 0.35 * inch
        badge_y = CARD_Y + CARD_H - img_h + 0.7 * inch
        p.setFillColor(WHITE)
        p.roundRect(badge_x, badge_y, badge_w, badge_h, 12, stroke=0, fill=1)
        
        p.setFillColor(TEXT_DARK)
        p.setFont("Helvetica-Bold", 7)
        p.drawCentredString(badge_x + badge_w/2, badge_y + 0.3 * inch, "PRICE")
        p.setFont("Helvetica-Bold", 14)
        p.drawCentredString(badge_x + badge_w/2, badge_y + 0.1 * inch, f"${booking.total_amount}")
        p.restoreState()

        # --- 4. Info Section (White Area) ---
        grid_y = CARD_Y + CARD_H - img_h - 0.6 * inch
        
        def draw_field(p, x, y, label, value, align='left'):
            p.saveState()
            p.setFont("Helvetica-Bold", 9)
            p.setFillColor(TEXT_LIGHT)
            if align == 'left':
                p.drawString(x, y, label.upper())
                p.setFont("Helvetica-Bold", 13)
                p.setFillColor(TEXT_DARK)
                p.drawString(x, y - 0.22 * inch, str(value))
            else:
                p.drawRightString(x, y, label.upper())
                p.setFont("Helvetica-Bold", 13)
                p.setFillColor(TEXT_DARK)
                p.drawRightString(x, y - 0.22 * inch, str(value))
            p.restoreState()

        # Row 1
        date_str = booking.event.event_date.strftime("%d %b %Y") if booking.event.event_date else "TBA"
        draw_field(p, CARD_X + 0.4 * inch, grid_y, "Date & Time", date_str)
        
        venue_name = booking.event.venue.name if booking.event.venue else "TBA"
        draw_field(p, CARD_X + CARD_W - 0.4 * inch, grid_y, "Location", venue_name, align='right')
        
        # Row 2
        grid_y -= 0.75 * inch
        draw_field(p, CARD_X + 0.4 * inch, grid_y, "Gate / Section", "Gate G4 / Sec B")
        
        t_type = booking.ticket.ticket_type if booking.ticket else "VIP"
        draw_field(p, CARD_X + CARD_W - 0.4 * inch, grid_y, "Seat Number", f"{t_type}-ROW-12 / 42", align='right')

        # --- 5. Barcode ---
        grid_y -= 1.1 * inch
        p.saveState()
        barcode = code128.Code128(ticket.ticket_code, barHeight=0.55*inch, barWidth=1.3)
        barcode.drawOn(p, CARD_X + (CARD_W - barcode.width)/2, grid_y)
        
        p.setFont("Courier-Bold", 10)
        p.setFillColor(TEXT_LIGHT)
        p.drawCentredString(CARD_X + CARD_W/2, grid_y - 0.18 * inch, f"TICKET CODE: {ticket.ticket_code}")
        p.restoreState()

        # --- 6. Notches & Divider ---
        grid_y -= 0.5 * inch
        p.saveState()
        p.setDash(4, 3)
        p.setStrokeColor(DIVIDER_COLOR)
        p.line(CARD_X + 0.5 * inch, grid_y, CARD_X + CARD_W - 0.5 * inch, grid_y)
        
        # Side Notches
        p.setFillColor(WHITE)
        p.circle(CARD_X, grid_y, 0.18 * inch, stroke=1, fill=1)
        p.circle(CARD_X + CARD_W, grid_y, 0.18 * inch, stroke=1, fill=1)
        p.restoreState()



    p.save()
    buffer.seek(0)
    return buffer
