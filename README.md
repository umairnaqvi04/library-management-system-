## 📚 LIBRARY MANAGEMENT SYSTEM
## Complete Step-by-Step Implementation Guide

---

## PHASE 1: PROJECT SETUP (Week 1)

### Step 1: Create Project Folder Structure
```
LibraryManagementSystem/
├── backend/           (Server-side code)
├── frontend/          (User interface)
├── database/          (Database files)
├── documentation/     (Project docs)
└── README.md
```

**How to do it:**
1. Open Command Prompt / Terminal
2. Create main folder:
```bash
mkdir LibraryManagementSystem
cd LibraryManagementSystem
```

3. Create subfolders:
```bash
mkdir backend frontend database documentation
```

---

### Step 2: Install Required Software

**A. Install Python (for Backend)**
- Download: https://www.python.org/downloads/
- Select Python 3.9+
- ✅ Check "Add Python to PATH"
- Click Install

**B. Install Node.js (Alternative Backend)**
- Download: https://nodejs.org/
- Install the LTS version

**C. Install MySQL/PostgreSQL (Database)**
- MySQL: https://www.mysql.com/downloads/
- OR PostgreSQL: https://www.postgresql.org/download/

**D. Install Code Editor**
- VS Code: https://code.visualstudio.com/
- Open Command Prompt: type `code` to verify

**E. Install Git (Version Control)**
- Download: https://git-scm.com/

---

### Step 3: Create Virtual Environment (Python)
```bash
cd backend
python -m venv venv

# Activate virtual environment
# For Windows:
venv\Scripts\activate

# For Mac/Linux:
source venv/bin/activate
```

---

## PHASE 2: DATABASE SETUP (Week 2)

### Step 4: Create Database

**A. Open MySQL Command Line**
```bash
mysql -u root -p
# Enter password
```

**B. Create Database and Tables**
```sql
-- Create database
CREATE DATABASE library_management;
USE library_management;

-- BOOKS TABLE
CREATE TABLE books (
    book_id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(255),
    isbn VARCHAR(20) UNIQUE,
    total_copies INT,
    available_copies INT,
    published_year YEAR,
    category VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- MEMBERS TABLE
CREATE TABLE members (
    member_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE,
    phone VARCHAR(15),
    address TEXT,
    membership_date DATE,
    status VARCHAR(20) DEFAULT 'Active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- TRANSACTIONS TABLE
CREATE TABLE transactions (
    transaction_id INT PRIMARY KEY AUTO_INCREMENT,
    member_id INT,
    book_id INT,
    issue_date DATE,
    return_date DATE,
    due_date DATE,
    status VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (member_id) REFERENCES members(member_id),
    FOREIGN KEY (book_id) REFERENCES books(book_id)
);

-- FINES TABLE
CREATE TABLE fines (
    fine_id INT PRIMARY KEY AUTO_INCREMENT,
    member_id INT,
    transaction_id INT,
    fine_amount DECIMAL(10, 2),
    reason VARCHAR(255),
    fine_date DATE,
    status VARCHAR(20) DEFAULT 'Pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (member_id) REFERENCES members(member_id),
    FOREIGN KEY (transaction_id) REFERENCES transactions(transaction_id)
);

-- USER TABLE (Login)
CREATE TABLE users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert Sample Data
INSERT INTO books (title, author, isbn, total_copies, available_copies, published_year, category) VALUES
('Database Systems', 'Henry Korth', 'ISBN-001', 5, 3, 2015, 'Computer Science'),
('Web Development', 'Jon Ducket', 'ISBN-002', 4, 2, 2018, 'Web'),
('Data Science Fundamentals', 'Joel Grus', 'ISBN-003', 3, 1, 2020, 'Science'),
('System Design Interview', 'Alex Yu', 'ISBN-004', 6, 4, 2021, 'Technology');

INSERT INTO members (name, email, phone, membership_date) VALUES
('Ali Hassan', 'ali@example.com', '03001234567', '2023-01-15'),
('Fatima Khan', 'fatima@example.com', '03009876543', '2023-03-20'),
('Ahmed Malik', 'ahmed@example.com', '03215555555', '2023-05-10');

INSERT INTO users (username, password, role) VALUES
('admin', 'admin123', 'Admin'),
('librarian', 'lib123', 'Librarian');
```

---

## PHASE 3: BACKEND DEVELOPMENT (Week 3-4)

### Step 5: Create Flask Backend

**A. Install Flask and Dependencies**
```bash
cd backend
pip install flask flask-cors flask-mysql python-dotenv
```

**B. Create app.py file**
```python
from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)

# Database Connection
def get_db_connection():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='your_password',
        database='library_management'
    )
    return connection

# ============ BOOKS ENDPOINTS ============

# Get all books
@app.route('/api/books', methods=['GET'])
def get_books():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM books')
        books = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(books)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Add new book
@app.route('/api/books', methods=['POST'])
def add_book():
    try:
        data = request.json
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO books (title, author, isbn, total_copies, available_copies, published_year, category)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        ''', (data['title'], data['author'], data['isbn'], data['total_copies'], 
              data['available_copies'], data['published_year'], data['category']))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Book added successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============ MEMBERS ENDPOINTS ============

# Get all members
@app.route('/api/members', methods=['GET'])
def get_members():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM members')
        members = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(members)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Add new member
@app.route('/api/members', methods=['POST'])
def add_member():
    try:
        data = request.json
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO members (name, email, phone, address, membership_date)
            VALUES (%s, %s, %s, %s, %s)
        ''', (data['name'], data['email'], data['phone'], data['address'], datetime.now().date()))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Member added successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============ TRANSACTIONS ENDPOINTS ============

# Issue book
@app.route('/api/issue-book', methods=['POST'])
def issue_book():
    try:
        data = request.json
        conn = get_db_connection()
        cursor = conn.cursor()
        
        issue_date = datetime.now().date()
        due_date = issue_date + timedelta(days=14)  # 2 weeks
        
        cursor.execute('''
            INSERT INTO transactions (member_id, book_id, issue_date, due_date, status)
            VALUES (%s, %s, %s, %s, 'Active')
        ''', (data['member_id'], data['book_id'], issue_date, due_date))
        
        # Update available copies
        cursor.execute('''
            UPDATE books SET available_copies = available_copies - 1
            WHERE book_id = %s
        ''', (data['book_id'],))
        
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Book issued successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Return book
@app.route('/api/return-book/<int:transaction_id>', methods=['PUT'])
def return_book(transaction_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Get transaction details
        cursor.execute('SELECT * FROM transactions WHERE transaction_id = %s', (transaction_id,))
        transaction = cursor.fetchone()
        
        return_date = datetime.now().date()
        fine_amount = 0
        
        # Calculate fine if overdue
        if return_date > transaction['due_date']:
            days_overdue = (return_date - transaction['due_date']).days
            fine_amount = days_overdue * 10  # 10 per day
            
            # Add fine record
            cursor.execute('''
                INSERT INTO fines (member_id, transaction_id, fine_amount, reason, fine_date)
                VALUES (%s, %s, %s, 'Late Return', %s)
            ''', (transaction['member_id'], transaction_id, fine_amount, return_date))
        
        # Update transaction
        cursor.execute('''
            UPDATE transactions SET return_date = %s, status = 'Completed'
            WHERE transaction_id = %s
        ''', (return_date, transaction_id))
        
        # Update available copies
        cursor.execute('''
            UPDATE books SET available_copies = available_copies + 1
            WHERE book_id = %s
        ''', (transaction['book_id'],))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({'message': 'Book returned', 'fine': fine_amount}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============ FINES ENDPOINTS ============

# Get all fines
@app.route('/api/fines', methods=['GET'])
def get_fines():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('''
            SELECT f.*, m.name FROM fines f
            JOIN members m ON f.member_id = m.member_id
        ''')
        fines = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(fines)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============ REPORTS ENDPOINTS ============

# Inventory report
@app.route('/api/reports/inventory', methods=['GET'])
def inventory_report():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('''
            SELECT title, author, total_copies, available_copies,
                   (total_copies - available_copies) as issued
            FROM books
        ''')
        report = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(report)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Dashboard stats
@app.route('/api/dashboard/stats', methods=['GET'])
def dashboard_stats():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute('SELECT COUNT(*) as total FROM books')
        total_books = cursor.fetchone()['total']
        
        cursor.execute('SELECT COUNT(*) as total FROM members WHERE status = "Active"')
        active_members = cursor.fetchone()['total']
        
        cursor.execute('SELECT COUNT(*) as total FROM transactions WHERE status = "Active"')
        issued_books = cursor.fetchone()['total']
        
        cursor.execute('SELECT SUM(fine_amount) as total FROM fines WHERE status = "Pending"')
        pending_fines = cursor.fetchone()['total'] or 0
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'total_books': total_books,
            'active_members': active_members,
            'issued_books': issued_books,
            'pending_fines': pending_fines
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

**C. Create .env file (for passwords)**
```
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=library_management
```

**D. Run the backend**
```bash
python app.py
```

---

## PHASE 4: FRONTEND DEVELOPMENT (Week 4-5)

### Step 6: Create React Frontend

**A. Create React App**
```bash
cd frontend
npx create-react-app .
```

**B. Install dependencies**
```bash
npm install axios react-router-dom
```

**C. Create main components**

**File: src/components/Dashboard.js**
```javascript
import React, { useState, useEffect } from 'react';
import axios from 'axios';

function Dashboard() {
  const [stats, setStats] = useState({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchStats();
  }, []);

  const fetchStats = async () => {
    try {
      const response = await axios.get('http://localhost:5000/api/dashboard/stats');
      setStats(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching stats:', error);
      setLoading(false);
    }
  };

  if (loading) return <div>Loading...</div>;

  return (
    <div style={{ padding: '2rem' }}>
      <h1>Dashboard</h1>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '20px' }}>
        <div style={{ border: '1px solid #ddd', padding: '20px', borderRadius: '8px' }}>
          <p>Total Books</p>
          <h2>{stats.total_books}</h2>
        </div>
        <div style={{ border: '1px solid #ddd', padding: '20px', borderRadius: '8px' }}>
          <p>Active Members</p>
          <h2>{stats.active_members}</h2>
        </div>
        <div style={{ border: '1px solid #ddd', padding: '20px', borderRadius: '8px' }}>
          <p>Issued Books</p>
          <h2>{stats.issued_books}</h2>
        </div>
        <div style={{ border: '1px solid #ddd', padding: '20px', borderRadius: '8px' }}>
          <p>Pending Fines</p>
          <h2>₨{stats.pending_fines}</h2>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
```

**D. Update src/App.js**
```javascript
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Dashboard from './components/Dashboard';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Dashboard />} />
      </Routes>
    </Router>
  );
}

export default App;
```

**E. Run frontend**
```bash
npm start
```

---

## PHASE 5: INTEGRATION & TESTING (Week 5-6)

### Step 7: Connect Frontend to Backend

**Update src/config/api.js:**
```javascript
import axios from 'axios';

const API_URL = 'http://localhost:5000/api';

export const getBooks = () => axios.get(`${API_URL}/books`);
export const addBook = (book) => axios.post(`${API_URL}/books`, book);
export const getMembers = () => axios.get(`${API_URL}/members`);
export const addMember = (member) => axios.post(`${API_URL}/members`, member);
export const issueBook = (data) => axios.post(`${API_URL}/issue-book`, data);
export const returnBook = (transactionId) => axios.put(`${API_URL}/return-book/${transactionId}`);
export const getFines = () => axios.get(`${API_URL}/fines`);
export const getDashboardStats = () => axios.get(`${API_URL}/dashboard/stats`);
```

### Step 8: Testing

**Test Checklist:**
- [ ] Backend API running on port 5000
- [ ] Frontend running on port 3000
- [ ] Can fetch books from API
- [ ] Can add new members
- [ ] Can issue books
- [ ] Can return books
- [ ] Fine calculation working
- [ ] All database operations working

**Manual Testing:**
1. Open browser: http://localhost:3000
2. Go to Books section - should see all books
3. Try adding a member
4. Try issuing a book
5. Check if fine calculates automatically

---

## PHASE 6: DEPLOYMENT (Week 6)

### Step 9: Deploy Backend to Heroku

**A. Create account on Heroku**
- Visit: https://www.heroku.com/
- Sign up and create app

**B. Install Heroku CLI**
```bash
# Download: https://devcenter.heroku.com/articles/heroku-cli
heroku login
```

**C. Deploy**
```bash
cd backend
heroku create your-app-name
git push heroku main
```

### Step 10: Deploy Frontend to Vercel

**A. Create account on Vercel**
- Visit: https://vercel.com/
- Sign up with GitHub

**B. Deploy**
```bash
cd frontend
npm run build
vercel
```

---

## QUICK START CHECKLIST

### Day 1-2: Setup
- [ ] Install Python, Node.js, MySQL
- [ ] Create folder structure
- [ ] Setup virtual environment

### Day 3: Database
- [ ] Create MySQL database
- [ ] Create all tables
- [ ] Insert sample data
- [ ] Test connections

### Day 4-5: Backend
- [ ] Install Flask dependencies
- [ ] Create all API endpoints
- [ ] Test each API with Postman
- [ ] Fix any errors

### Day 6-7: Frontend
- [ ] Create React app
- [ ] Build all components
- [ ] Connect to APIs
- [ ] Test all features

### Day 8: Final Testing
- [ ] Test all operations
- [ ] Fix bugs
- [ ] Document features

---

## USEFUL COMMANDS

**Python/Flask:**
```bash
pip install -r requirements.txt
python app.py
```

**Node/React:**
```bash
npm install
npm start
npm run build
```

**MySQL:**
```bash
mysql -u root -p
SHOW DATABASES;
USE library_management;
SHOW TABLES;
SELECT * FROM books;
```

**Git:**
```bash
git init
git add .
git commit -m "Initial commit"
git push origin main
```

---

## TEAM ROLES

| Name | Role | Responsibility |
|------|------|---|
| Ahmed Ali | Database & Backend | Create API, Database Design |
| Fatima Khan | Frontend & UI | Create UI, Connect APIs |
| Hassan Tariq | Testing & QA | Test all features, Find bugs |

---

## TROUBLESHOOTING

**Issue:** "Cannot connect to database"
- Solution: Check MySQL is running, verify username/password in .env

**Issue:** "CORS error"
- Solution: Add `CORS(app)` in Flask backend

**Issue:** "Module not found"
- Solution: Run `pip install -r requirements.txt` or `npm install`

**Issue:** "Port already in use"
- Solution: Change port in app.py: `app.run(port=5001)`

---

**Good Luck! 🚀**
Contact: Proceed step by step and test after each phase.
