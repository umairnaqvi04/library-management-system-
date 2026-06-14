import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta
import json

# Page Config
st.set_page_config(page_title="Library Management System", layout="wide", initial_sidebar_state="expanded")

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 20px;
    }
    .header {
        color: #1f77b4;
        font-size: 28px;
        font-weight: bold;
        margin-bottom: 20px;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .success-message {
        background-color: #d4edda;
        padding: 12px;
        border-radius: 5px;
        color: #155724;
        margin: 10px 0;
    }
    .error-message {
        background-color: #f8d7da;
        padding: 12px;
        border-radius: 5px;
        color: #721c24;
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'books' not in st.session_state:
    st.session_state.books = [
        {'book_id': 1, 'title': 'Database Systems', 'author': 'Henry Korth', 'isbn': 'ISBN-001', 'copies': 5, 'available': 3},
        {'book_id': 2, 'title': 'Web Development', 'author': 'Jon Ducket', 'isbn': 'ISBN-002', 'copies': 4, 'available': 2},
        {'book_id': 3, 'title': 'Data Science Fundamentals', 'author': 'Joel Grus', 'isbn': 'ISBN-003', 'copies': 3, 'available': 1},
        {'book_id': 4, 'title': 'System Design Interview', 'author': 'Alex Yu', 'isbn': 'ISBN-004', 'copies': 6, 'available': 4},
        {'book_id': 5, 'title': 'Clean Code', 'author': 'Robert Martin', 'isbn': 'ISBN-005', 'copies': 5, 'available': 2},
    ]

if 'members' not in st.session_state:
    st.session_state.members = [
        {'member_id': 'M001', 'name': 'Ali Hassan', 'email': 'ali@example.com', 'phone': '0333-1234567', 'join_date': '2023-01-15'},
        {'member_id': 'M002', 'name': 'Fatima Khan', 'email': 'fatima@example.com', 'phone': '0300-9876543', 'join_date': '2023-03-20'},
        {'member_id': 'M003', 'name': 'Ahmed Malik', 'email': 'ahmed@example.com', 'phone': '0321-5555555', 'join_date': '2023-05-10'},
    ]

if 'transactions' not in st.session_state:
    st.session_state.transactions = [
        {'txn_id': 'TXN001', 'member': 'Ali Hassan', 'book': 'Database Systems', 'type': 'Issue', 'date': '2024-01-10', 'status': 'Active'},
        {'txn_id': 'TXN002', 'member': 'Fatima Khan', 'book': 'Web Development', 'type': 'Return', 'date': '2024-01-09', 'status': 'Completed'},
    ]

if 'fines' not in st.session_state:
    st.session_state.fines = [
        {'fine_id': 'F001', 'member': 'Ali Hassan', 'reason': 'Late Return', 'amount': 500, 'status': 'Pending'},
    ]

# Sidebar
st.sidebar.title("📚 Library Management System")
st.sidebar.write("---")

page = st.sidebar.radio("Choose Section:", 
    options=[
        "📊 Dashboard",
        "📖 Books Management",
        "👥 Members Management",
        "🔄 Issue & Return",
        "💰 Fines Management",
        "📈 Reports"
    ]
)

st.sidebar.write("---")
st.sidebar.info("System v1.0 | All data stored locally")

# ============================================
# PAGE 1: DASHBOARD
# ============================================
if page == "📊 Dashboard":
    st.markdown('<div class="header">Dashboard</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📕 Total Books", len(st.session_state.books))
    
    with col2:
        st.metric("👤 Total Members", len(st.session_state.members))
    
    with col3:
        st.metric("📤 Issued Books", len([t for t in st.session_state.transactions if t['type'] == 'Issue']))
    
    with col4:
        st.metric("💵 Total Fines", f"₨{sum([f['amount'] for f in st.session_state.fines])}")
    
    st.write("---")
    
    # Recent Books
    st.subheader("📚 Recent Books")
    books_df = pd.DataFrame(st.session_state.books)
    st.dataframe(books_df[['title', 'author', 'copies', 'available']], use_container_width=True, hide_index=True)
    
    st.write("---")
    
    # Recent Members
    st.subheader("👥 Recent Members")
    members_df = pd.DataFrame(st.session_state.members)
    st.dataframe(members_df[['name', 'email', 'phone']], use_container_width=True, hide_index=True)
    
    st.write("---")
    
    # Recent Transactions
    st.subheader("🔄 Recent Transactions")
    txn_df = pd.DataFrame(st.session_state.transactions)
    st.dataframe(txn_df[['txn_id', 'member', 'book', 'type', 'status']], use_container_width=True, hide_index=True)

# ============================================
# PAGE 2: BOOKS MANAGEMENT
# ============================================
elif page == "📖 Books Management":
    st.markdown('<div class="header">Books Management</div>', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["View Books", "Add New Book"])
    
    with tab1:
        st.subheader("All Books in Library")
        books_df = pd.DataFrame(st.session_state.books)
        st.dataframe(books_df, use_container_width=True, hide_index=True)
        
        # Search functionality
        st.write("---")
        search_title = st.text_input("🔍 Search by book title:")
        if search_title:
            filtered_books = [b for b in st.session_state.books if search_title.lower() in b['title'].lower()]
            st.dataframe(pd.DataFrame(filtered_books), use_container_width=True, hide_index=True)
    
    with tab2:
        st.subheader("➕ Add New Book")
        
        with st.form("add_book_form"):
            title = st.text_input("Book Title", placeholder="Enter book title")
            author = st.text_input("Author", placeholder="Enter author name")
            isbn = st.text_input("ISBN", placeholder="Enter ISBN")
            copies = st.number_input("Total Copies", min_value=1, value=1)
            available = st.number_input("Available Copies", min_value=0, value=1)
            
            submitted = st.form_submit_button("✅ Add Book", use_container_width=True)
            
            if submitted and title and author and isbn:
                new_book = {
                    'book_id': len(st.session_state.books) + 1,
                    'title': title,
                    'author': author,
                    'isbn': isbn,
                    'copies': copies,
                    'available': available
                }
                st.session_state.books.append(new_book)
                st.markdown('<div class="success-message">✅ Book added successfully!</div>', unsafe_allow_html=True)
                st.rerun()
            elif submitted:
                st.markdown('<div class="error-message">❌ Please fill in all fields</div>', unsafe_allow_html=True)

# ============================================
# PAGE 3: MEMBERS MANAGEMENT
# ============================================
elif page == "👥 Members Management":
    st.markdown('<div class="header">Members Management</div>', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["View Members", "Add New Member"])
    
    with tab1:
        st.subheader("All Members")
        members_df = pd.DataFrame(st.session_state.members)
        st.dataframe(members_df, use_container_width=True, hide_index=True)
        
        # Search functionality
        st.write("---")
        search_name = st.text_input("🔍 Search by member name:")
        if search_name:
            filtered_members = [m for m in st.session_state.members if search_name.lower() in m['name'].lower()]
            st.dataframe(pd.DataFrame(filtered_members), use_container_width=True, hide_index=True)
    
    with tab2:
        st.subheader("➕ Add New Member")
        
        with st.form("add_member_form"):
            name = st.text_input("Member Name", placeholder="Enter full name")
            email = st.text_input("Email", placeholder="Enter email address")
            phone = st.text_input("Phone", placeholder="Enter phone number")
            
            submitted = st.form_submit_button("✅ Add Member", use_container_width=True)
            
            if submitted and name and email and phone:
                new_member = {
                    'member_id': f"M{str(len(st.session_state.members) + 1).zfill(3)}",
                    'name': name,
                    'email': email,
                    'phone': phone,
                    'join_date': datetime.now().strftime('%Y-%m-%d')
                }
                st.session_state.members.append(new_member)
                st.markdown('<div class="success-message">✅ Member added successfully!</div>', unsafe_allow_html=True)
                st.rerun()
            elif submitted:
                st.markdown('<div class="error-message">❌ Please fill in all fields</div>', unsafe_allow_html=True)

# ============================================
# PAGE 4: ISSUE & RETURN
# ============================================
elif page == "🔄 Issue & Return":
    st.markdown('<div class="header">Book Issue & Return</div>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["Issue Book", "Return Book", "Transaction History"])
    
    with tab1:
        st.subheader("📥 Issue New Book")
        
        with st.form("issue_book_form"):
            member_names = [m['name'] for m in st.session_state.members]
            selected_member = st.selectbox("Select Member", member_names)
            
            book_titles = [b['title'] for b in st.session_state.books]
            selected_book = st.selectbox("Select Book", book_titles)
            
            submitted = st.form_submit_button("✅ Issue Book", use_container_width=True)
            
            if submitted:
                member = next((m for m in st.session_state.members if m['name'] == selected_member), None)
                book = next((b for b in st.session_state.books if b['title'] == selected_book), None)
                
                if member and book and book['available'] > 0:
                    # Create transaction
                    new_txn = {
                        'txn_id': f"TXN{str(len(st.session_state.transactions) + 1).zfill(3)}",
                        'member': selected_member,
                        'book': selected_book,
                        'type': 'Issue',
                        'date': datetime.now().strftime('%Y-%m-%d'),
                        'status': 'Active'
                    }
                    st.session_state.transactions.append(new_txn)
                    
                    # Update available copies
                    book['available'] -= 1
                    
                    st.markdown('<div class="success-message">✅ Book issued successfully!</div>', unsafe_allow_html=True)
                    st.rerun()
                elif book and book['available'] == 0:
                    st.markdown('<div class="error-message">❌ Book not available</div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="error-message">❌ Invalid selection</div>', unsafe_allow_html=True)
    
    with tab2:
        st.subheader("📤 Return Book")
        
        active_txns = [t for t in st.session_state.transactions if t['status'] == 'Active']
        
        if active_txns:
            txn_display = [f"{t['txn_id']} - {t['member']} ({t['book']})" for t in active_txns]
            selected_txn = st.selectbox("Select Transaction to Return", txn_display)
            
            if st.button("✅ Return Book", use_container_width=True):
                txn_id = selected_txn.split(" - ")[0]
                transaction = next((t for t in st.session_state.transactions if t['txn_id'] == txn_id), None)
                
                if transaction:
                    # Update transaction
                    transaction['type'] = 'Return'
                    transaction['status'] = 'Completed'
                    
                    # Update available copies
                    book = next((b for b in st.session_state.books if b['title'] == transaction['book']), None)
                    if book:
                        book['available'] += 1
                    
                    st.markdown('<div class="success-message">✅ Book returned successfully!</div>', unsafe_allow_html=True)
                    st.rerun()
        else:
            st.info("No active issues to return")
    
    with tab3:
        st.subheader("Transaction History")
        txn_df = pd.DataFrame(st.session_state.transactions)
        st.dataframe(txn_df, use_container_width=True, hide_index=True)

# ============================================
# PAGE 5: FINES MANAGEMENT
# ============================================
elif page == "💰 Fines Management":
    st.markdown('<div class="header">Fines & Penalties</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Fines", f"₨{sum([f['amount'] for f in st.session_state.fines])}")
    
    with col2:
        paid = sum([f['amount'] for f in st.session_state.fines if f['status'] == 'Paid'])
        st.metric("Paid Fines", f"₨{paid}")
    
    with col3:
        pending = sum([f['amount'] for f in st.session_state.fines if f['status'] == 'Pending'])
        st.metric("Pending Fines", f"₨{pending}")
    
    st.write("---")
    
    tab1, tab2 = st.tabs(["View Fines", "Pay Fine"])
    
    with tab1:
        st.subheader("All Fines")
        fines_df = pd.DataFrame(st.session_state.fines)
        st.dataframe(fines_df, use_container_width=True, hide_index=True)
    
    with tab2:
        st.subheader("Pay Fine")
        
        pending_fines = [f for f in st.session_state.fines if f['status'] == 'Pending']
        
        if pending_fines:
            fine_display = [f"{f['fine_id']} - {f['member']} (₨{f['amount']})" for f in pending_fines]
            selected_fine = st.selectbox("Select Fine to Pay", fine_display)
            
            if st.button("💳 Mark as Paid", use_container_width=True):
                fine_id = selected_fine.split(" - ")[0]
                fine = next((f for f in st.session_state.fines if f['fine_id'] == fine_id), None)
                
                if fine:
                    fine['status'] = 'Paid'
                    st.markdown('<div class="success-message">✅ Fine payment recorded!</div>', unsafe_allow_html=True)
                    st.rerun()
        else:
            st.info("No pending fines")

# ============================================
# PAGE 6: REPORTS
# ============================================
elif page == "📈 Reports":
    st.markdown('<div class="header">Reports & Analytics</div>', unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["Inventory Report", "Member Report", "Fine Report", "Transaction Report"])
    
    with tab1:
        st.subheader("Inventory Report")
        inventory = pd.DataFrame(st.session_state.books)
        st.dataframe(inventory, use_container_width=True, hide_index=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Books", len(st.session_state.books))
        with col2:
            total_available = sum([b['available'] for b in st.session_state.books])
            st.metric("Total Available", total_available)
    
    with tab2:
        st.subheader("Member Report")
        members = pd.DataFrame(st.session_state.members)
        st.dataframe(members, use_container_width=True, hide_index=True)
        st.metric("Total Members", len(st.session_state.members))
    
    with tab3:
        st.subheader("Fine Collection Report")
        fines = pd.DataFrame(st.session_state.fines)
        st.dataframe(fines, use_container_width=True, hide_index=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Fines", f"₨{sum([f['amount'] for f in st.session_state.fines])}")
        with col2:
            st.metric("Paid", f"₨{sum([f['amount'] for f in st.session_state.fines if f['status'] == 'Paid'])}")
        with col3:
            st.metric("Pending", f"₨{sum([f['amount'] for f in st.session_state.fines if f['status'] == 'Pending'])}")
    
    with tab4:
        st.subheader("Transaction Report")
        txns = pd.DataFrame(st.session_state.transactions)
        st.dataframe(txns, use_container_width=True, hide_index=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Transactions", len(st.session_state.transactions))
        with col2:
            active = len([t for t in st.session_state.transactions if t['status'] == 'Active'])
            st.metric("Active Issues", active)

# Footer
st.write("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
<p>📚 Library Management System | Built with Streamlit</p>
<p>Version 1.0 | All data stored locally in session</p>
</div>
""", unsafe_allow_html=True)
