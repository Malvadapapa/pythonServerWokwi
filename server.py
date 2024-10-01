from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
CORS(app)  # Habilita CORS en todas las rutas

# Configuración de conexión a MySQL
config = {
    'user': 'root',
    'password': 'redcros62',
    'host': 'localhost',
    'database': 'chat_db'
}

def get_db_connection():
    try:
        cnx = mysql.connector.connect(**config)
        return cnx, cnx.cursor()
    except Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None, None

# Ruta para registrar dispositivo (usuario) con alias
@app.route('/registrar-dispositivo', methods=['POST'])
def registrar_dispositivo():
    dispositivo_id = request.json.get('dispositivo_id')
    alias = request.json.get('alias')
    cnx, cursor = get_db_connection()
    if cnx is None or cursor is None:
        return jsonify({'error': 'Error al conectar a la base de datos'}), 500

    try:
        cursor.execute("INSERT INTO usuarios (dispositivo_id, alias) VALUES (%s, %s)", (dispositivo_id, alias))
        cnx.commit()
    except Error as e:
        return jsonify({'error': f'Error al registrar el dispositivo: {e}'}), 500
    finally:
        cursor.close()
        cnx.close()
    
    return jsonify({'mensaje': 'Dispositivo registrado correctamente'})

# Ruta para obtener la lista de dispositivos disponibles
@app.route('/dispositivos', methods=['GET'])
def obtener_dispositivos():
    cnx, cursor = get_db_connection()
    if cnx is None or cursor is None:
        return jsonify({'error': 'Error al conectar a la base de datos'}), 500

    try:
        cursor.execute("SELECT dispositivo_id, alias FROM usuarios")
        dispositivos = cursor.fetchall()
    except Error as e:
        return jsonify({'error': f'Error al obtener dispositivos: {e}'}), 500
    finally:
        cursor.close()
        cnx.close()
    
    return jsonify({'dispositivos': dispositivos})

# Ruta para crear una conversación
@app.route('/crear-conversacion', methods=['POST'])
def crear_conversacion():
    dispositivo_id1 = request.json.get('dispositivo_id1')
    dispositivo_id2 = request.json.get('dispositivo_id2')
    cnx, cursor = get_db_connection()
    if cnx is None or cursor is None:
        return jsonify({'error': 'Error al conectar a la base de datos'}), 500

    try:
        cursor.execute("SELECT id FROM usuarios WHERE dispositivo_id = %s", (dispositivo_id1,))
        usuario1 = cursor.fetchone()
        if usuario1 is None:
            return jsonify({'error': 'Usuario 1 no encontrado'}), 404
        usuario1_id = usuario1[0]
        
        cursor.execute("SELECT id FROM usuarios WHERE dispositivo_id = %s", (dispositivo_id2,))
        usuario2 = cursor.fetchone()
        if usuario2 is None:
            return jsonify({'error': 'Usuario 2 no encontrado'}), 404
        usuario2_id = usuario2[0]
        
        cursor.execute("INSERT INTO conversaciones (usuario1_id, usuario2_id) VALUES (%s, %s)", (usuario1_id, usuario2_id))
        cnx.commit()
        conversacion_id = cursor.lastrowid
    except Error as e:
        return jsonify({'error': f'Error al crear la conversación: {e}'}), 500
    finally:
        cursor.close()
        cnx.close()
    
    return jsonify({'conversacion_id': conversacion_id})

# Ruta para enviar mensaje
@app.route('/enviar-mensaje', methods=['POST'])
def enviar_mensaje():
    dispositivo_id = request.json.get('dispositivo_id')
    conversacion_id = request.json.get('conversacion_id')
    mensaje = request.json.get('mensaje')
    cnx, cursor = get_db_connection()
    if cnx is None or cursor is None:
        return jsonify({'error': 'Error al conectar a la base de datos'}), 500

    try:
        cursor.execute("SELECT id FROM usuarios WHERE dispositivo_id = %s", (dispositivo_id,))
        usuario = cursor.fetchone()
        if usuario is None:
            return jsonify({'error': 'Usuario no encontrado'}), 404
        usuario_id = usuario[0]
        
        cursor.execute("SELECT id FROM conversaciones WHERE id = %s", (conversacion_id,))
        if cursor.fetchone() is None:
            return jsonify({'error': 'Conversación no encontrada'}), 404
        
        cursor.execute("INSERT INTO mensajes (conversacion_id, usuario_id, mensaje) VALUES (%s, %s, %s)", (conversacion_id, usuario_id, mensaje))
        cnx.commit()
    except Error as e:
        return jsonify({'error': f'Error al enviar el mensaje: {e}'}), 500
    finally:
        cursor.close()
        cnx.close()
    
    return jsonify({'mensaje': 'Mensaje enviado correctamente'})

# Ruta para obtener mensajes de una conversación
@app.route('/obtener-conversacion', methods=['GET'])
def obtener_conversacion():
    conversacion_id = request.args.get('conversacion_id')
    cnx, cursor = get_db_connection()
    if cnx is None or cursor is None:
        return jsonify({'error': 'Error al conectar a la base de datos'}), 500

    try:
        cursor.execute("SELECT id FROM conversaciones WHERE id = %s", (conversacion_id,))
        if cursor.fetchone() is None:
            return jsonify({'error': 'Conversación no encontrada'}), 404
        
        cursor.execute("SELECT usuario_id, mensaje, fecha FROM mensajes WHERE conversacion_id = %s ORDER BY fecha ASC", (conversacion_id,))
        mensajes = cursor.fetchall()
    except Error as e:
        return jsonify({'error': f'Error al obtener la conversación: {e}'}), 500
    finally:
        cursor.close()
        cnx.close()
    
    return jsonify({'mensajes': mensajes})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)