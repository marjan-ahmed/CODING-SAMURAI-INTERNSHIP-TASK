import sqlite3
import hashlib

def setup_database():
    """Initialize the database with tables and sample data"""
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create articles table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            author_id INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (author_id) REFERENCES users (id)
        )
    ''')
    
    # Create a sample user
    sample_password = hashlib.sha256('password123'.encode()).hexdigest()
    cursor.execute('''
        INSERT OR IGNORE INTO users (username, email, password_hash)
        VALUES (?, ?, ?)
    ''', ('demo_user', 'demo@example.com', sample_password))
    
    # Get the user ID
    cursor.execute('SELECT id FROM users WHERE username = ?', ('demo_user',))
    user_id = cursor.fetchone()[0]
    
    # Create sample articles
    sample_articles = [
        {
            'title': 'Welcome to My Blog',
            'content': '''Welcome to my personal blog! This is my first post where I'll be sharing my thoughts, experiences, and insights on various topics.

I'm excited to start this journey of writing and connecting with readers who share similar interests. You can expect posts about technology, programming, life experiences, and much more.

Feel free to register and create your own posts to join the conversation!'''
        },
        {
            'title': 'Getting Started with Flask and Next.js',
            'content': '''In this post, I want to share my experience building a full-stack application using Flask as the backend and Next.js as the frontend.

The combination of these two technologies provides a powerful foundation for building modern web applications. Flask offers simplicity and flexibility for the API, while Next.js provides an excellent developer experience for the frontend.

Key benefits of this stack:
- Fast development cycle
- Great performance
- Excellent developer tools
- Strong community support

I'll be writing more detailed tutorials about specific aspects of this stack in future posts.'''
        }
    ]
    
    for article in sample_articles:
        cursor.execute('''
            INSERT OR IGNORE INTO articles (title, content, author_id)
            VALUES (?, ?, ?)
        ''', (article['title'], article['content'], user_id))
    
    conn.commit()
    conn.close()
    print("Database setup completed successfully!")
    print("Sample user created: username='demo_user', password='password123'")

if __name__ == '__main__':
    setup_database()
