from flask import request, jsonify
from utils.printer import print_ticket

def create_routes(app):
    @app.route("/print_ticket", methods=["POST"])
    def handle_print_ticket():
        try:
            data = request.get_json()

            if not data or 'client_name' not in data or 'address' not in data or 'products' not in data or 'total_price' not in data:
                return jsonify({"error": "Formato JSON inválido o datos faltantes"}), 400
            
            client_name = data['client_name']
            address = data['address']
            products = data['products']
            total_price = data['total_price']
            numero = data.get('numero', 0)
            timestamp = data.get('timestamp', 'No se proporcionó hora')
            mensaje = data.get('mensaje', "Gracias por su compra!!!")

            if not isinstance(products, list) or not all(isinstance(product, dict) and 'name' in product and 'amount' in product and 'price' in product for product in products):
                return jsonify({"error": "Formato de productos inválido"}), 400

            response_message, status_code = print_ticket(client_name, address, products, total_price, timestamp, numero, mensaje)
            return jsonify({"message": response_message}), status_code

        except Exception as e:
            return jsonify({"error": str(e)}), 500
