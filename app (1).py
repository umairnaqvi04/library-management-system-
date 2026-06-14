import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# =================== CONFIG ===================
API_URL = "http://localhost:5000/api"

st.set_page_config(
    page_title="📚 Library Management System",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =================== STYLING ===================
st.markdown("""
<style>
    .main {
        background-color: #f5f5f5;
    }
    .stButton button {
        background-color: #4CAF50;
        color: white;
        border-radius: 8px;
        padding: 10px 20px;
    }
    .stButton button:hover {
        background-color: #45a049;
    }
    h1 {
        color: #1f77b4;
        text-align: center;
    }
    h2 {
        color: #ff7f0e;
        border-bottom: 2px solid #ff7f0e;
        padding-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# =================== HELPER FUNCTIONS ===================

def fetch_books():
    """Fetch all books"""
    try:
        response = requests.get(f"{API_URL}/books")
        return response.json() if response.status_code == 200 else []
    except:
        st.error("❌ Cannot connect to API. Make sure it's running on port 5000")
        return []

def fetch_members():
    """Fetch all members"""
    try:
        response = requests.get(f"{API_URL}/members")
        return response.json() if response.status_code == 200 else []
    except:
        st.error("❌ Cannot connect to API")
        return []

def fetch_issues():
    """Fetch all issue records"""
    try:
        response = requests.get(f"{API_URL}/issues")
        return response.json() if response.status_code == 200 else []
    except:
        st.error("❌ Cannot connect to API")
        return []

def fetch_stats():
    """Fetch system stats"""
    try:
        response = requests.get(f"{API_URL}/stats")
        return response.json() if response.status_code == 200 else {}
    except:
        return {}

# =================== HEADER ===================
st.markdown("# 📚 Library Management System")
st.markdown("**Professional Library Management Dashboard**")
st.markdown("---")

# =================== SIDEBAR NAVIGATION ===================
with st.sidebar:
    st.markdown("## 🔧 Navigation")
    page = st.radio(
        "Choose Section:",
        [
            "📊 Dashboard",
            "📖 Books Management",
            "👥 Members Management",
            "🔄 Issue & Return",
            "💰 Fines Management",
            "📈 Reports"
        ]
    )

# =================== PAGE: DASHBOARD ===================
if page == "📊 Dashboard":
    st.header("Dashboard Overview")
    
    stats = fetch_stats()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="📕 Total Books",
            value=stats.get('total_books', 0)
        )
    
    with col2:
        st.metric(
            label="👤 Total Members",
            value=stats.get('total_members', 0)
        )
    
    with col3:
        st.metric(
            label="📤 Issued Books",
            value=stats.get('issued_books', 0)
        )
    
    with col4:
        st.metric(
            label="💵 Total Fines",
            value=f"Rs. {stats.get('total_fines', 0)}"
        )
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📚 Recent Books")
        books = fetch_books()
        if books:
            df = pd.DataFrame(books)
            st.dataframe(df[['book_id', 'title', 'author', 'status']], use_container_width=True)
        else:
            st.info("No books in database")
    
    with col2:
        st.subheader("👥 Recent Members")
        members = fetch_members()
        if members:
            df = pd.DataFrame(members)
            st.dataframe(df[['member_id', 'name', 'role', 'department']], use_container_width=True)
        else:
            st.info("No members in database")

# =================== PAGE: BOOKS MANAGEMENT ===================
elif page == "📖 Books Management":
    st.header("Books Management")
    
    tab1, tab2, tab3 = st.tabs(["Add Book", "View Books", "Search & Delete"])
    
    # TAB 1: Add Book
    with tab1:
        st.subheader("➕ Add New Book")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            title = st.text_input("📕 Book Title", placeholder="Enter book title")
        
        with col2:
            author = st.text_input("✍️ Author Name", placeholder="Enter author name")
        
        with col3:
            category = st.selectbox(
                "📂 Category",
                ["Programming", "Database", "CS", "AI", "Web", "Mobile", "Other"]
            )
        
        if st.button("✅ Add Book", key="add_book"):
            if title and author:
                try:
                    response = requests.post(
                        f"{API_URL}/books",
                        json={"title": title, "author": author, "category": category}
                    )
                    if response.status_code == 201:
                        st.success("✔ Book Added Successfully!")
                        st.balloons()
                    else:
                        st.error("❌ Failed to add book")
                except:
                    st.error("❌ Cannot connect to API")
            else:
                st.warning("⚠️ Please fill all fields")
    
    # TAB 2: View Books
    with tab2:
        st.subheader("📚 All Books")
        
        books = fetch_books()
        if books:
            df = pd.DataFrame(books)
            st.dataframe(df, use_container_width=True)
            
            st.write(f"**Total Books: {len(books)}**")
        else:
            st.info("📭 No books in database")
    
    # TAB 3: Search & Delete
    with tab3:
        st.subheader("🔍 Search Books")
        
        search_term = st.text_input("Search by title or author:")
        
        if search_term:
            try:
                response = requests.get(f"{API_URL}/books/search/{search_term}")
                results = response.json() if response.status_code == 200 else []
                
                if results:
                    df = pd.DataFrame(results)
                    st.dataframe(df, use_container_width=True)
                    
                    st.subheader("🗑️ Delete Book")
                    book_id = st.number_input("Enter Book ID to delete:", min_value=1)
                    
                    if st.button("Delete Book"):
                        try:
                            response = requests.delete(f"{API_URL}/books/{book_id}")
                            if response.status_code == 200:
                                st.success("✔ Book Deleted!")
                            else:
                                st.error("❌ Book not found")
                        except:
                            st.error("❌ Cannot connect to API")
                else:
                    st.info("📭 No books found")
            except:
                st.error("❌ Cannot connect to API")

# =================== PAGE: MEMBERS MANAGEMENT ===================
elif page == "👥 Members Management":
    st.header("Members Management")
    
    tab1, tab2 = st.tabs(["Add Member", "View Members"])
    
    # TAB 1: Add Member
    with tab1:
        st.subheader("➕ Add New Member")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            name = st.text_input("👤 Member Name", placeholder="Enter member name")
        
        with col2:
            role = st.selectbox("Role", ["Student", "Faculty", "Librarian", "Admin"])
        
        with col3:
            department = st.text_input("🏢 Department", placeholder="e.g., CS, IT, Admin")
        
        if st.button("✅ Add Member", key="add_member"):
            if name and department:
                try:
                    response = requests.post(
                        f"{API_URL}/members",
                        json={"name": name, "role": role, "department": department}
                    )
                    if response.status_code == 201:
                        st.success("✔ Member Added Successfully!")
                        st.balloons()
                    else:
                        st.error("❌ Failed to add member")
                except:
                    st.error("❌ Cannot connect to API")
            else:
                st.warning("⚠️ Please fill all fields")
    
    # TAB 2: View Members
    with tab2:
        st.subheader("👥 All Members")
        
        members = fetch_members()
        if members:
            df = pd.DataFrame(members)
            st.dataframe(df, use_container_width=True)
            
            st.write(f"**Total Members: {len(members)}**")
        else:
            st.info("📭 No members in database")

# =================== PAGE: ISSUE & RETURN ===================
elif page == "🔄 Issue & Return":
    st.header("Issue & Return Books")
    
    tab1, tab2 = st.tabs(["Issue Book", "Return Book"])
    
    # TAB 1: Issue Book
    with tab1:
        st.subheader("📤 Issue Book to Member")
        
        books = fetch_books()
        members = fetch_members()
        
        if books and members:
            col1, col2 = st.columns(2)
            
            with col1:
                available_books = [b for b in books if b['status'] == 'Available']
                book_options = {f"{b['title']} by {b['author']}": b['book_id'] for b in available_books}
                
                selected_book = st.selectbox("Select Book:", list(book_options.keys()))
                book_id = book_options[selected_book]
            
            with col2:
                member_options = {m['name']: m['member_id'] for m in members}
                selected_member = st.selectbox("Select Member:", list(member_options.keys()))
                member_id = member_options[selected_member]
            
            if st.button("✅ Issue Book", key="issue_book"):
                try:
                    response = requests.post(
                        f"{API_URL}/issue",
                        json={"book_id": book_id, "member_id": member_id}
                    )
                    if response.status_code == 201:
                        st.success("✔ Book Issued Successfully!")
                        st.info("📖 Return due in 7 days")
                        st.balloons()
                    else:
                        st.error("❌ Failed to issue book")
                except:
                    st.error("❌ Cannot connect to API")
        else:
            st.warning("⚠️ Add books and members first")
    
    # TAB 2: Return Book
    with tab2:
        st.subheader("📥 Return Book")
        
        issues = fetch_issues()
        issued_records = [i for i in issues if i['status'] == 'Issued']
        
        if issued_records:
            issue_options = {
                f"Book ID {i['book_id']} - Member ID {i['member_id']}": i['issue_id'] 
                for i in issued_records
            }
            
            selected_issue = st.selectbox("Select Issue Record:", list(issue_options.keys()))
            issue_id = issue_options[selected_issue]
            
            if st.button("✅ Return Book", key="return_book"):
                try:
                    response = requests.post(f"{API_URL}/return/{issue_id}")
                    if response.status_code == 200:
                        st.success("✔ Book Returned Successfully!")
                        st.balloons()
                    else:
                        st.error("❌ Failed to return book")
                except:
                    st.error("❌ Cannot connect to API")
        else:
            st.info("📭 No issued books to return")

# =================== PAGE: FINES MANAGEMENT ===================
elif page == "💰 Fines Management":
    st.header("Fines Management")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("💾 Calculate Fine")
        
        issue_id = st.number_input("Enter Issue ID:", min_value=1)
        
        if st.button("Calculate Fine", key="calc_fine"):
            try:
                response = requests.post(f"{API_URL}/calculate-fine/{issue_id}")
                if response.status_code == 200:
                    data = response.json()
                    if data.get('fine', 0) > 0:
                        st.warning(f"⚠️ Fine: Rs. {data['fine']}")
                        st.info(f"Days Late: {data['days_late']}")
                    else:
                        st.success("✔ No fine for this book")
                else:
                    st.error("❌ Issue not found")
            except:
                st.error("❌ Cannot connect to API")
    
    with col2:
        st.subheader("📋 Member Fines")
        
        member_id = st.number_input("Enter Member ID:", min_value=1, key="fine_member")
        
        if st.button("View Fines", key="view_fines"):
            try:
                response = requests.get(f"{API_URL}/fines/{member_id}")
                if response.status_code == 200:
                    data = response.json()
                    if data['fines']:
                        df = pd.DataFrame(data['fines'])
                        st.dataframe(df, use_container_width=True)
                        st.metric("Total Fine", f"Rs. {data['total']}")
                    else:
                        st.success("✔ No fines for this member")
                else:
                    st.error("❌ Member not found")
            except:
                st.error("❌ Cannot connect to API")

# =================== PAGE: REPORTS ===================
elif page == "📈 Reports":
    st.header("System Reports")
    
    st.subheader("📊 System Statistics")
    
    stats = fetch_stats()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Total Books", stats.get('total_books', 0))
        st.metric("Total Members", stats.get('total_members', 0))
    
    with col2:
        st.metric("Issued Books", stats.get('issued_books', 0))
        st.metric("Returned Books", stats.get('returned_books', 0))
    
    st.markdown("---")
    
    st.subheader("📚 All Books Report")
    books = fetch_books()
    if books:
        df = pd.DataFrame(books)
        st.dataframe(df, use_container_width=True)
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            status_counts = df['status'].value_counts()
            st.bar_chart(status_counts)
        
        with col2:
            category_counts = df['category'].value_counts()
            st.bar_chart(category_counts)

# =================== FOOTER ===================
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
    <small>📚 Library Management System | Built with Streamlit & Flask</small>
</div>
""", unsafe_allow_html=True)
