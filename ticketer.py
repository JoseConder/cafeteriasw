from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph
from barcode import generate
from barcode.writer import ImageWriter
from dbconfig import *
import os
def generar_ticket(id_orden):
    ordenes = pedidos_collection
    orden = ordenes.find_one({'_id': id_orden})
    if not orden:
        return 'Orden no encontrada'

    nombre_cliente = orden.get('nombre', 'Nombre no disponible')

    # Crear un nuevo archivo PDF
    # Ruta de la carpeta donde se guardarán los tickets
    carpeta_tickets = "tickets"

    # Crear la carpeta si no existe
    os.makedirs(carpeta_tickets, exist_ok=True)
    pdf_filename = f"tickets/ticket_orden_{id_orden}.pdf"
    c = canvas.Canvas(pdf_filename, pagesize=letter)

    # Configurar estilos de texto
    styles = getSampleStyleSheet()
    header_style = styles["Heading3"]
    body_style = styles["BodyText"]
    total_style = ParagraphStyle('Total', fontSize=14, fontName='Helvetica-Bold')

    # Escribir en el archivo PDF
    y = 750
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(150, y, "Ticket de venta")
    y -= 30

    header = Paragraph(f"Orden: {orden['numero_pedido']}", header_style)
    w, h = header.wrap(400, 400)
    header.drawOn(c, 100, y)
    y -= h + 10

    c.setFont("Helvetica", 12)
    c.drawString(100, y, f"Cliente: {nombre_cliente}")
    y -= 20

    total = 0
    for producto in orden['productos']:
        subtotal = producto['precio'] * producto['cantidad']
        total += subtotal

        p = Paragraph(f"<b>{producto['producto_nombre']}</b>", body_style)
        w, h = p.wrap(400, 400)
        p.drawOn(c, 100, y)
        y -= h + 5

        c.drawString(100, y, f"Cantidad: {producto['cantidad']}")
        y -= 15
        c.drawString(100, y, f"Precio: ${producto['precio']:.2f}")
        y -= 15
        c.drawString(100, y, f"Subtotal: ${subtotal:.2f}")
        y -= 20

    total_paragraph = Paragraph(f"Total: ${total:.2f}", total_style)
    w, h = total_paragraph.wrap(400, 400)
    total_paragraph.drawOn(c, 100, y)
    y -= h + 20

    # Guardar y cerrar el archivo PDF en la carpeta /tickets
    c.save()
    return f"Ticket generado: {pdf_filename}"