from flask import request, jsonify
from printer import print_ticket

def create_routes(app):
    @app.route("/print_ticket", methods=["POST"])
    def handle_print_ticket():
        try:
            # Obtener los datos JSON de la solicitud
            data = request.get_json()

            if not data or 'client_name' not in data or 'address' not in data or 'products' not in data or 'total_price' not in data:
                return jsonify({"error": "Formato JSON inválido o datos faltantes"}), 400

            client_name = data['client_name']
            address = data['address']
            products = data['products']  # Lista de productos en formato [{"name": "producto", "price": 10.00}, ...]
            total_price = data['total_price']
            timestamp = data.get('timestamp', 'No se proporcionó hora')  # Hora opcional

            # Llamar a la función para imprimir el ticket
            response_message, status_code = print_ticket(client_name, address, products, total_price, timestamp)
            return jsonify({"message": response_message}), status_code

        except Exception as e:
            return jsonify({"error": str(e)}), 500
