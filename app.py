from flask import Flask, request, jsonify, render_template
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# MySQL database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Punia@1503',
    'database': 'tax_details'
}

def get_db_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        if conn.is_connected():
            return conn
    except Error as e:
        print(f"Error: {e}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/payments', methods=['GET'])
def get_payments():
    """Fetch all payment records."""
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM payments')
        payments = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(payments)
    return jsonify({'error': 'Database connection failed'}), 500

@app.route('/api/payments/<int:id>', methods=['GET'])
def get_payment_by_id(id):
    """Fetch a single payment record by ID."""
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM payments WHERE id = %s', (id,))
        payment = cursor.fetchone()
        cursor.close()
        conn.close()
        if payment:
            return jsonify(payment)
        return jsonify({'error': 'Payment not found'}), 404
    return jsonify({'error': 'Database connection failed'}), 500

@app.route('/api/payments', methods=['POST'])
def add_payment():
    """Add a new payment record."""
    data = request.get_json()
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO payments (company, amount, payment_date, status, due_date) VALUES (%s, %s, %s, %s, %s)',
            (data['company'], data['amount'], data.get('payment_date'), data['status'], data['due_date'])
        )
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Payment added successfully'}), 201
    return jsonify({'error': 'Database connection failed'}), 500

@app.route('/api/payments/<int:id>', methods=['PUT'])
def update_payment(id):
    """Update an existing payment record."""
    data = request.get_json()
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute(
            'UPDATE payments SET company = %s, amount = %s, payment_date = %s, status = %s, due_date = %s WHERE id = %s',
            (data['company'], data['amount'], data.get('payment_date'), data['status'], data['due_date'], id)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Payment updated successfully'})
    return jsonify({'error': 'Database connection failed'}), 500

@app.route('/api/payments/<int:id>', methods=['DELETE'])
def delete_payment(id):
    """Delete a payment record by ID."""
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM payments WHERE id = %s', (id,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Payment deleted successfully'})
    return jsonify({'error': 'Database connection failed'}), 500

@app.route('/api/payments/due/<due_date>', methods=['GET'])
def get_payments_by_due_date(due_date):
    """Fetch all payment records by a specific due date."""
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM payments WHERE due_date = %s', (due_date,))
        payments = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(payments)
    return jsonify({'error': 'Database connection failed'}), 500

@app.route('/api/payments/clear', methods=['DELETE'])
def clear_payments():
    """Delete all payment records."""
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM payments')
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'All payments deleted successfully'})
    return jsonify({'error': 'Database connection failed'}), 500

if __name__ == '__main__':
    app.run(debug=True)
