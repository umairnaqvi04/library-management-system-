from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# Database Configuration
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'library_management')
}

def get_db_connection():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except mysql.connector.Error as err:
        print(f"Database Error: {err}")
        return None

# ============================================
# TEST ENDPOINT
# ============================================
@app.route('/api/test', methods=['GET'])
def test():
    return jsonify({'message': 'Backend is running successfully!', 'status': 'success'})

# ============================================
# BOOKS ENDPOINTS
# ============================================

@app.route('/api/books', methods=['GET'])
def get_books():
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500
        
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM books')
        books = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(books), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/books', methods=['POST'])
def add_book():
    try:
        data = request.json
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500
        
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO books (title, author, isbn, total_copies, available_copies, published_year, category)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        ''', (data['title'], data['author'], data['isbn'], data['total_copies'], 
              data['available_copies'], data['published_year'], data['category']))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Book added successfully', 'status': 'success'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500
        
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM books WHERE book_id = %s', (book_id,))
        book = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if book:
            return jsonify(book), 200
        return jsonify({'error': 'Book not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    try:
        data = request.json
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500
        
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE books SET title=%s, author=%s, available_copies=%s
            WHERE book_id=%s
        ''', (data['title'], data['author'], data['available_copies'], book_id))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Book updated successfully', 'status': 'success'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============================================
# MEMBERS ENDPOINTS
# ============================================

@app.route('/api/members', methods=['GET'])
def get_members():
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500
        
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM members')
        members = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(members), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/members', methods=['POST'])
def add_member():
    try:
        data = request.json
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500
        
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO members (name, email, phone, address, membership_date, status)
            VALUES (%s, %s, %s, %s, %s, %s)
        ''', (data['name'], data['email'], data['phone'], data.get('address', ''), 
              datetime.now().date(), 'Active'))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Member added successfully', 'status': 'success'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/members/<int:member_id>', methods=['GET'])
def get_member(member_id):
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500
        
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM members WHERE member_id = %s', (member_id,))
        member = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if member:
            return jsonify(member), 200
        return jsonify({'error': 'Member not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============================================
# TRANSACTIONS ENDPOINTS
# ============================================

@app.route('/api/issue-book', methods=['POST'])
def issue_book():
    try:
        data = request.json
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500
        
        cursor = conn.cursor()
        
        issue_date = datetime.now().date()
        due_date = issue_date + timedelta(days=14)  # 2 weeks
        
        cursor.execute('''
            INSERT INTO transactions (member_id, book_id, issue_date, due_date, status)
            VALUES (%s, %s, %s, %s, 'Active')
        ''', (data['member_id'], data['book_id'], issue_date, due_date))
        
        cursor.execute('''
            UPDATE books SET available_copies = available_copies - 1
            WHERE book_id = %s
        ''', (data['book_id'],))
        
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Book issued successfully', 'status': 'success'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/return-book/<int:transaction_id>', methods=['PUT'])
def return_book(transaction_id):
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500
        
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute('SELECT * FROM transactions WHERE transaction_id = %s', (transaction_id,))
        transaction = cursor.fetchone()
        
        if not transaction:
            return jsonify({'error': 'Transaction not found'}), 404
        
        return_date = datetime.now().date()
        fine_amount = 0
        
        # Calculate fine if overdue
        if return_date > transaction['due_date']:
            days_overdue = (return_date - transaction['due_date']).days
            fine_amount = days_overdue * 10  # 10 per day
            
            cursor.execute('''
                INSERT INTO fines (member_id, transaction_id, fine_amount, reason, fine_date, status)
                VALUES (%s, %s, %s, 'Late Return', %s, 'Pending')
            ''', (transaction['member_id'], transaction_id, fine_amount, return_date))
        
        cursor.execute('''
            UPDATE transactions SET return_date = %s, status = 'Completed'
            WHERE transaction_id = %s
        ''', (return_date, transaction_id))
        
        cursor.execute('''
            UPDATE books SET available_copies = available_copies + 1
            WHERE book_id = %s
        ''', (transaction['book_id'],))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({
            'message': 'Book returned successfully',
            'fine': fine_amount,
            'status': 'success'
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/transactions', methods=['GET'])
def get_transactions():
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500
        
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM transactions')
        transactions = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(transactions), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============================================
# FINES ENDPOINTS
# ============================================

@app.route('/api/fines', methods=['GET'])
def get_fines():
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500
        
        cursor = conn.cursor(dictionary=True)
        cursor.execute('''
            SELECT f.*, m.name as member_name FROM fines f
            JOIN members m ON f.member_id = m.member_id
        ''')
        fines = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(fines), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/fines/<int:fine_id>', methods=['PUT'])
def pay_fine(fine_id):
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500
        
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE fines SET status = 'Paid'
            WHERE fine_id = %s
        ''', (fine_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Fine payment recorded', 'status': 'success'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============================================
# REPORTS ENDPOINTS
# ============================================

@app.route('/api/reports/inventory', methods=['GET'])
def inventory_report():
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500
        
        cursor = conn.cursor(dictionary=True)
        cursor.execute('''
            SELECT title, author, total_copies, available_copies,
                   (total_copies - available_copies) as issued
            FROM books
        ''')
        report = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(report), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/dashboard/stats', methods=['GET'])
def dashboard_stats():
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500
        
        cursor = conn.cursor(dictionary=True)
        
        # Total books
        cursor.execute('SELECT COUNT(*) as total FROM books')
        total_books = cursor.fetchone()['total']
        
        # Active members
        cursor.execute('SELECT COUNT(*) as total FROM members WHERE status = "Active"')
        active_members = cursor.fetchone()['total']
        
        # Issued books
        cursor.execute('SELECT COUNT(*) as total FROM transactions WHERE status = "Active"')
        issued_books = cursor.fetchone()['total']
        
        # Pending fines
        cursor.execute('SELECT COALESCE(SUM(fine_amount), 0) as total FROM fines WHERE status = "Pending"')
        pending_fines = cursor.fetchone()['total']
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'total_books': total_books,
            'active_members': active_members,
            'issued_books': issued_books,
            'pending_fines': pending_fines,
            'status': 'success'
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============================================
# ERROR HANDLERS
# ============================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    print("=" * 50)
    print("Library Management System - Flask Backend")
    print("=" * 50)
    print("Starting server on http://localhost:5000")
    print("API Documentation: http://localhost:5000/api/docs")
    print("=" * 50)
    app.run(debug=True, port=5000, host='0.0.0.0')
