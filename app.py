from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

# MySQL database connection
def get_db_connection():
    connection = mysql.connector.connect(
        host='db',  # This is the name of the service in Docker Compose
        user='root',
        password='password',
        database='crud_db'
    )
    return connection

# CRUD operations

@app.route('/items', methods=['GET'])
def get_items():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute('SELECT * FROM items')
    items = cursor.fetchall()
    connection.close()
    return jsonify(items)

@app.route('/item', methods=['POST'])
def create_item():
    new_item = request.get_json()
    name = new_item['name']
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('INSERT INTO items (name) VALUES (%s)', (name,))
    connection.commit()
    connection.close()
    return jsonify(new_item), 201

@app.route('/item/<int:id>', methods=['PUT'])
def update_item(id):
    updated_item = request.get_json()
    name = updated_item['name']
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('UPDATE items SET name = %s WHERE id = %s', (name, id))
    connection.commit()
    connection.close()
    return jsonify(updated_item)

@app.route('/item/<int:id>', methods=['DELETE'])
def delete_item(id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('DELETE FROM items WHERE id = %s', (id,))
    connection.commit()
    connection.close()
    return '', 204

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',port=5000)
