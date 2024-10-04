import psycopg2
import os
from flask import Flask, request, jsonify

# Configurar las variables de entorno directamente en el código
os.environ['DATABASE_URL'] = "postgresql://postgres:wYbvcCbojqRcJFlTaDFRwsNMlfEMTMZp@junction.proxy.rlwy.net:22133/railway"

app = Flask(__name__)

DATABASE_URL = os.getenv('DATABASE_URL')

def connect_db():
    conn = psycopg2.connect(DATABASE_URL)
    return conn

# Endpoint GET para devolver datos
@app.route('/get_data', methods=['GET'])
def get_data():
    conn = None
    cursor = None
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM led_log")  # Cambia 'led_log' por el nombre de tu tabla
        rows = cursor.fetchall()
        data = [{'id': row[0], 'timestamp': row[1], 'led_status': row[2]} for row in rows]
        return jsonify(data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# Endpoint POST para insertar datos
@app.route('/add_data', methods=['POST'])
def add_data():
    conn = None
    cursor = None
    try:
        conn = connect_db()
        cursor = conn.cursor()
        led_status = request.json.get('led_status')
        cursor.execute("INSERT INTO led_log (timestamp, led_status) VALUES (NOW(), %s)", (led_status,))
        conn.commit()
        return jsonify({'message': 'Se guardo la informacion correctamente correctamente'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

# Endpoint GET para devolver datos
@app.route('/get_data', methods=['GET'])
def get_data():
    conn = None
    cursor = None
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM led_log")  # Cambia 'led_log' por el nombre de tu tabla
        rows = cursor.fetchall()
        data = [{'id': row[0], 'timestamp': row[1], 'led_status': row[2]} for row in rows]
        return jsonify(data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# Endpoint POST para insertar datos
@app.route('/add_data', methods=['POST'])
def add_data():
    conn = None
    cursor = None
    try:
        conn = connect_db()
        cursor = conn.cursor()
        led_status = request.json.get('led_status')
        cursor.execute("INSERT INTO led_log (timestamp, led_status) VALUES (NOW(), %s)", (led_status,))
        conn.commit()
        return jsonify({'message': 'Se guardo la informacion correctamente correctamente'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
