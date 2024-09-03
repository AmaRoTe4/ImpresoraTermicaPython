import os
import platform
import tempfile
from datetime import datetime

# Comandos ESC/POS para corte de papel y manejo de imágenes
CUT_PAPER_FULL = b'\x1D\x56\x00'

def get_os():
    return platform.system()

def print_ticket(client_name, address, products, total_price, timestamp=None, numero=0, mensaje="Gracias por su compra!!!"):
    try:
        ticket_content = generate_ticket(client_name, address, products, total_price, timestamp, numero, mensaje)
        if ticket_content:
            print_ticket_via_default_printer(ticket_content)
            return "Comanda impresa correctamente", 200
        else:
            return "Error al generar el ticket", 400
    except Exception as e:
        return f"Error al imprimir: {str(e)}", 500

def generate_ticket(client_name, address, products, total_price, timestamp=None, numero=0, mensaje="Gracias por su compra!!!"):
    timestamp = timestamp or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ticket_content = "----- INESITA -----"
    ticket_content += f"N° Ticket: {numero}\n"
    ticket_content += f"Hora: {timestamp}\n"
    ticket_content += f"Cliente: {client_name}\n"
    ticket_content += f"Dirección: {address}\n\n"
    
    ticket_content += "Productos:\n"
    for product in products:
        ticket_content += f"{product['amount']}x {product['name']} - ${product['price']:.2f}\n"
    
    ticket_content += f"\nTotal: ${total_price:.2f}\n"
    ticket_content += mensaje

    ticket_content += "\n\n.....................\n\n\n\n"
    ticket_content += f"Cliente: {client_name}\n"
    ticket_content += f"Dirección: {address}\n\n"
    ticket_content += f"N° Ticket: {numero} - TOTAL ${total_price:.2f}\n\n\n"

    ticket_bytes = ticket_content.encode('cp437')
    ticket_bytes += CUT_PAPER_FULL

    return ticket_bytes

def print_ticket_via_default_printer(ticket_content):
    os_name = get_os()
    
    with tempfile.NamedTemporaryFile(delete=False, suffix='.bin') as temp_file:
        temp_file.write(ticket_content)
        temp_file_path = temp_file.name
    
    if os_name == 'Windows':
        os.system(f'print /D:"<printer_name>" {temp_file_path}')  # Reemplaza <printer_name> con el nombre de tu impresora
    elif os_name == 'Linux':
        os.system(f'lp {temp_file_path}')
    
    os.remove(temp_file_path)
