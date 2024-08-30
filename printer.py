import os
import platform
import tempfile
from datetime import datetime

# Comandos ESC/POS para corte de papel
CUT_PAPER_FULL = b'\x1D\x56\x00'

def get_os():
    return platform.system()

def print_ticket(client_name, address, products, total_price, timestamp=None, numero=0):
    try:
        ticket_content = generate_ticket(client_name, address, products, total_price, timestamp, numero)
        if ticket_content:
            print_ticket_via_default_printer(ticket_content)
            return "Comanda impresa correctamente", 200
        else:
            return "Error al generar el ticket", 400
    except Exception as e:
        return f"Error al imprimir: {str(e)}", 500

def generate_ticket(client_name, address, products, total_price, timestamp=None, numero=0):
    timestamp = timestamp or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ticket_content = f"** COMANDA **\n"
    ticket_content += f"N° Ticket: {numero}\n"
    ticket_content += f"Hora: {timestamp}\n"
    ticket_content += f"Cliente: {client_name}\n"
    ticket_content += f"Dirección: {address}\n\n"
    
    ticket_content += "Productos:\n"
    for product in products:
        ticket_content += f"{product['amount']}x {product['name']} - ${product['price']:.2f}\n"
    
    ticket_content += f"\nTotal: ${total_price:.2f}\n"
    ticket_content += "Gracias por su compra"

    ticket_content += "\n\n.....................\n\n\n\n"
    ticket_content += f"Cliente: {client_name}\n"
    ticket_content += f"Dirección: {address}\n\n"
    ticket_content += f"N° Ticket: {numero} - TOTAL ${total_price:.2f}\n\n\n"

    # Convertir el contenido del ticket a bytes y agregar el comando de corte
    ticket_bytes = ticket_content.encode('cp437')  # Usar cp437 para una codificación alternativa
    
    # Agregar comando de corte
    ticket_bytes += CUT_PAPER_FULL

    return ticket_bytes

def print_ticket_via_default_printer(ticket_content):
    os_name = get_os()
    
    # Guardar el contenido del ticket en un archivo temporal
    with tempfile.NamedTemporaryFile(delete=False, suffix='.bin') as temp_file:
        temp_file.write(ticket_content)
        temp_file_path = temp_file.name
    
    if os_name == 'Windows':
        # Enviar el archivo a la impresora en Windows
        os.system(f'lp {temp_file_path}')  # Windows tiene que tener configurado el comando lp o similar
    elif os_name == 'Linux':
        # Enviar el archivo a la impresora en Linux
        os.system(f'lp {temp_file_path}')
    
    # Eliminar el archivo temporal después de imprimir
    os.remove(temp_file_path)
