# 🚀 LIBRARY MANAGEMENT SYSTEM - SETUP & RUN GUIDE

## ERROR FIX - Complete Solution

The error "Cannot connect to API" happens when:
- ❌ Flask backend is not running
- ❌ Streamlit is trying to connect but backend is offline
- ❌ Database is not properly configured

**Solution: Use Streamlit with built-in data (NO API NEEDED)**

---

## ⚡ QUICK START (5 Minutes)

### Step 1: Download Files
```
- streamlit_app.py    ← Streamlit frontend (with built-in data)
- flask_app.py        ← Optional Flask backend
- requirements.txt    ← Python libraries
```

### Step 2: Install Python Libraries
```bash
pip install streamlit pandas requests flask flask-cors python-dotenv mysql-connector-python
```

### Step 3: Run Streamlit App (NO BACKEND NEEDED)
```bash
streamlit run streamlit_app.py
```

✅ **Done! App opens in browser at** `http://localhost:8501`

---

## 📋 DETAILED INSTALLATION

### Prerequisites
- **Python 3.9+** installed
- **pip** package manager
- Any web browser

### Installation Steps

#### Step 1: Install Python (if not already installed)

**Windows:**
1. Download: https://www.python.org/downloads/
2. Run installer
3. ✅ Check "Add Python to PATH"
4. Click "Install Now"

**Mac/Linux:**
```bash
# Mac
brew install python3

# Linux (Ubuntu)
sudo apt-get install python3 python3-pip
```

Verify installation:
```bash
python --version
pip --version
```

#### Step 2: Create Project Folder
```bash
# Create folder
mkdir LibraryManagementSystem
cd LibraryManagementSystem

# Create subfolders
mkdir app database
```

#### Step 3: Create requirements.txt
Save this as `requirements.txt`:
```
streamlit==1.28.0
pandas==2.0.0
requests==2.31.0
flask==2.3.0
flask-cors==4.0.0
python-dotenv==1.0.0
mysql-connector-python==8.1.0
```

#### Step 4: Install Dependencies
```bash
pip install -r requirements.txt
```

#### Step 5: Copy Python Files
- Copy `streamlit_app.py` to your folder
- Copy `flask_app.py` to your folder (optional)

#### Step 6: Run Streamlit Application
```bash
streamlit run streamlit_app.py
```

✅ **Your app is now running!**

Browser opens automatically at: `http://localhost:8501`

---

## 🎯 WHAT YOU CAN DO NOW

✅ View Dashboard with stats  
✅ Add books to catalog  
✅ Register new members  
✅ Issue books to members  
✅ Return books (auto-calculate fines)  
✅ Manage fines  
✅ Generate reports  
✅ Search functionality  

**All data is stored in your computer's memory!**

---

## 🗄️ (OPTIONAL) Setup with MySQL Database

If you want to use a real database:

### Step 1: Install MySQL

**Windows:**
1. Download: https://dev.mysql.com/downloads/mysql/
2. Run installer
3. Choose setup type: "Developer Default"
4. Follow installation wizard

**Mac:**
```bash
brew install mysql
brew services start mysql
mysql -u root
```

**Linux (Ubuntu):**
```bash
sudo apt-get install mysql-server
sudo mysql_secure_installation
mysql -u root -p
```

### Step 2: Create Database and Tables

Open MySQL Command Line:
```bash
mysql -u root -p
# Enter password
```

Run these commands:
```sql
-- Create database
CREATE DATABASE library_management;
USE library_management;

-- Books Table
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

-- Members Table
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

-- Transactions Table
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

-- Fines Table
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

EXIT;
```

### Step 3: Create .env File

Create `.env` file in your folder:
```
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=library_management
```

Replace `your_mysql_password` with your MySQL password.

### Step 4: Run Flask Backend (Terminal 1)
```bash
python flask_app.py
```

You should see:
```
==================================================
Library Management System - Flask Backend
==================================================
Starting server on http://localhost:5000
==================================================
```

### Step 5: Run Streamlit (Terminal 2)
```bash
streamlit run streamlit_app.py
```

Now both are running:
- **Streamlit UI**: http://localhost:8501
- **Flask API**: http://localhost:5000

---

## 🔧 TROUBLESHOOTING

### Problem: "streamlit: command not found"
**Solution:**
```bash
pip install streamlit
# or
python -m streamlit run streamlit_app.py
```

### Problem: "ModuleNotFoundError: No module named 'streamlit'"
**Solution:**
```bash
pip install -r requirements.txt
```

### Problem: Port 8501 already in use
**Solution:**
```bash
streamlit run streamlit_app.py --server.port=8502
```

### Problem: "Cannot connect to API"
**Solution:** You don't need the API! The Streamlit app has built-in data.
- If you want to use API, make sure Flask backend is running on port 5000

### Problem: MySQL connection failed
**Solution:**
```bash
# Check MySQL is running
mysql -u root -p
# If error, restart MySQL service

# Windows
net stop MySQL80
net start MySQL80

# Mac
brew services restart mysql

# Linux
sudo service mysql restart
```

### Problem: "Access denied for user 'root'"
**Solution:**
1. Check your password is correct in `.env` file
2. Reset MySQL password:
```bash
mysql -u root
ALTER USER 'root'@'localhost' IDENTIFIED BY 'newpassword';
FLUSH PRIVILEGES;
```

---

## 📊 TESTING THE APPLICATION

### Test 1: Dashboard
1. Open http://localhost:8501
2. Click "📊 Dashboard"
3. Should see 4 metrics cards
4. ✅ PASS if data displays

### Test 2: Add Book
1. Go to "📖 Books Management"
2. Click "Add New Book" tab
3. Fill in form:
   - Title: "My Test Book"
   - Author: "Test Author"
   - ISBN: "TEST-001"
   - Copies: 5
4. Click "✅ Add Book"
5. ✅ PASS if success message appears

### Test 3: Add Member
1. Go to "👥 Members Management"
2. Click "Add New Member" tab
3. Fill in form:
   - Name: "Test Member"
   - Email: "test@example.com"
   - Phone: "0300-1234567"
4. Click "✅ Add Member"
5. ✅ PASS if success message appears

### Test 4: Issue Book
1. Go to "🔄 Issue & Return"
2. Click "Issue Book" tab
3. Select member and book
4. Click "✅ Issue Book"
5. ✅ PASS if book issued successfully

### Test 5: Reports
1. Go to "📈 Reports"
2. Click different report tabs
3. ✅ PASS if data displays correctly

---

## 🌐 DEPLOYMENT

### Deploy to Streamlit Cloud (Free!)

1. **Create GitHub Account**
   - Go to https://github.com/
   - Sign up and create account

2. **Create Repository**
   - Create new repo called "library-management"
   - Upload `streamlit_app.py` and `requirements.txt`

3. **Deploy**
   - Go to https://streamlit.io/cloud
   - Click "New app"
   - Select your GitHub repo
   - Main file: `streamlit_app.py`
   - Click "Deploy"

✅ Your app is now live on the internet!

---

## 📱 ACCESSING YOUR APP

**Local Access:**
- Streamlit: http://localhost:8501
- Flask API: http://localhost:5000

**From Other Computers (same network):**
- Find your computer's IP: 
  ```bash
  # Windows
  ipconfig
  
  # Mac/Linux
  ifconfig
  ```
- Access: `http://YOUR_IP:8501`

**Online (after deployment):**
- Streamlit Cloud gives you a public URL

---

## 🎓 NEXT STEPS

### Option 1: Continue with Streamlit (Easiest)
✅ Use `streamlit_app.py` as is  
✅ All data stored in session  
✅ Deploy to Streamlit Cloud  

### Option 2: Add Flask Backend
✅ Use `flask_app.py` for API  
✅ Connect to MySQL database  
✅ More scalable for production  

### Option 3: Add Frontend UI
✅ Create React app  
✅ Connect to Flask API  
✅ Custom design and features  

---

## 📚 USEFUL COMMANDS

```bash
# Install packages
pip install streamlit

# Run Streamlit
streamlit run streamlit_app.py

# Run Flask
python flask_app.py

# MySQL
mysql -u root -p

# Check Python version
python --version

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate

# Deactivate virtual environment
deactivate
```

---

## 💡 TIPS

1. **Save your work** - Git commit regularly
2. **Keep requirements.txt updated** - `pip freeze > requirements.txt`
3. **Use .env for passwords** - Never commit password to GitHub
4. **Test locally first** - Before deploying online
5. **Check logs** - If something breaks, check terminal output

---

## ✅ YOU'RE READY!

Your Library Management System is ready to use!

**Quick Summary:**
- ✅ Streamlit app with built-in data (ready now)
- ✅ Optional Flask backend for database
- ✅ Can be deployed online for free
- ✅ Fully functional with all features

**Next: Run the app!**
```bash
streamlit run streamlit_app.py
```

---

**Questions? Check the error message carefully - it usually tells you what's wrong! 🔍**
