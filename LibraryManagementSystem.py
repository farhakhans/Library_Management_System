import streamlit as st
import sqlite3

# Database Initialization
def init_db():
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS books (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL,
                        author TEXT NOT NULL,
                        year INTEGER NOT NULL)''')
    conn.commit()
    conn.close()

# Add Book
def add_book(title, author, year):
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO books (title, author, year) VALUES (?, ?, ?)", (title, author, year))
    conn.commit()
    conn.close()

# Fetch Books
def get_books():
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    conn.close()
    return books

# Search Books
def search_books(query):
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books WHERE title LIKE ? OR author LIKE ?", (f"%{query}%", f"%{query}%"))
    books = cursor.fetchall()
    conn.close()
    return books

# Delete Book
def delete_book(book_id):
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM books WHERE id=?", (book_id,))
    conn.commit()
    conn.close()

# Update Book
def update_book(book_id, title, author, year):
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE books SET title=?, author=?, year=? WHERE id=?", (title, author, year, book_id))
    conn.commit()
    conn.close()


st.markdown("### Created by Farhana Ahsan")
# Title
st.title("📚 Library Management System")


# Sidebar with School-Themed GIF
st.sidebar.image("https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExMmRwdXJocGJyeWc3NXdlcmIyNGlpd3E4eHkxMWtjM2lienJ4YWZsbiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/SzydfQlBpsh92VJbvM/giphy.gif", use_container_width=True)
menu = ["Add Book", "View Books", "Search Books", "Update Book", "Delete Book", "Exit"]
choice = st.sidebar.radio("Navigation", menu)

init_db()

if choice == "Add Book":
    st.subheader("📚 Add a New Book")
    title = st.text_input("Book Title")
    author = st.text_input("Author Name")
    year = st.number_input("Publication Year", min_value=1000, max_value=9999, step=1)
    if st.button("Add Book"):
        if title and author and year:
            add_book(title, author, year)
            st.success(f"✅ Book '{title}' added successfully!")
        else:
            st.error("⚠️ All fields are required!")

elif choice == "View Books":
    st.subheader("📖 Library Books")
    books = get_books()
    if books:
        for book in books:
            st.markdown(f"**📖 {book[1]}** by *{book[2]}* (Published: {book[3]})")
            st.write("---")
    else:
        st.warning("⚠️ No books found!")

elif choice == "Search Books":
    st.subheader("🔎 Search for a Book")
    query = st.text_input("Enter book title or author name")
    if st.button("Search"):
        results = search_books(query)
        if results:
            for book in results:
                st.markdown(f"**📖 {book[1]}** by *{book[2]}* (Published: {book[3]})")
                st.write("---")
        else:
            st.warning("⚠️ No matching books found!")

elif choice == "Update Book":
    st.subheader("✏️ Update Book Details")
    books = get_books()
    book_dict = {f"{book[1]} by {book[2]} ({book[3]})": book[0] for book in books}
    selected_book = st.selectbox("Select Book", list(book_dict.keys()))
    if selected_book:
        book_id = book_dict[selected_book]
        new_title = st.text_input("New Title", value=selected_book.split(" by ")[0])
        new_author = st.text_input("New Author", value=selected_book.split(" by ")[1].split(" (")[0])
        new_year = st.number_input("New Year", value=int(selected_book.split("(")[1][:-1]))
        if st.button("Update Book"):
            update_book(book_id, new_title, new_author, new_year)
            st.success("✅ Book updated successfully!")

elif choice == "Delete Book":
    st.subheader("🗑️ Delete a Book")
    books = get_books()
    book_dict = {f"{book[1]} by {book[2]} ({book[3]})": book[0] for book in books}
    selected_book = st.selectbox("Select Book to Delete", list(book_dict.keys()))
    if st.button("Delete Book", help="⚠️ This action is irreversible!"):
        delete_book(book_dict[selected_book])
        st.warning("🗑️ Book deleted successfully!")

elif choice == "Exit":
    st.success("👋 Thank you for using the Library Management System!")
