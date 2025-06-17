from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import hashlib
import jwt
import datetime
from functools import wraps
import os

app = Flask(__name__)
CORS(app, origins=['http://localhost:3000'], supports_credentials=True)

@app.before_request
def log_request_info():
    print(f"Request: {request.method} {request.url}")
    print(f"Headers: {dict(request.headers)}")
    if request.is_json:
        print(f"JSON Body: {request.get_json()}")

# Secret key for JWT tokens
app.config['SECRET_KEY'] = 'your-secret-key-change-this-in-production'

# Database initialization
def init_db():
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
    
    conn.commit()
    conn.close()

# Initialize database on startup
init_db()

@app.route('/')
def home():
    return jsonify({
        'message': 'Personal Blog API is running!',
        'version': '1.0.0',
        'endpoints': {
            'auth': ['/api/auth/register', '/api/auth/login'],
            'articles': ['/api/articles', '/api/articles/<id>']
        }
    })

@app.route('/api/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.datetime.utcnow().isoformat(),
        'database': 'connected'
    })

@app.route('/api/test', methods=['GET', 'POST'])
def test_endpoint():
    if request.method == 'POST':
        data = request.get_json()
        return jsonify({
            'message': 'POST request received successfully',
            'data_received': data,
            'method': request.method
        })
    else:
        return jsonify({
            'message': 'GET request received successfully',
            'method': request.method
        })

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, password_hash):
    return hashlib.sha256(password.encode()).hexdigest() == password_hash

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        
        try:
            token = token.split(' ')[1]  # Remove 'Bearer ' prefix
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user_id = data['user_id']
        except:
            return jsonify({'message': 'Token is invalid'}), 401
        
        return f(current_user_id, *args, **kwargs)
    return decorated

@app.route('/api/auth/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'message': 'No data provided'}), 400
            
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        
        if not username or not email or not password:
            return jsonify({'message': 'Missing required fields'}), 400
        
        conn = sqlite3.connect('blog.db')
        cursor = conn.cursor()
        
        # Check if user already exists
        cursor.execute('SELECT id FROM users WHERE username = ? OR email = ?', (username, email))
        if cursor.fetchone():
            conn.close()
            return jsonify({'message': 'Username or email already exists'}), 400
        
        # Create new user
        password_hash = hash_password(password)
        cursor.execute(
            'INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)',
            (username, email, password_hash)
        )
        conn.commit()
        conn.close()
        
        return jsonify({'message': 'User created successfully'}), 201
        
    except Exception as e:
        return jsonify({'message': f'Registration failed: {str(e)}'}), 500

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'message': 'Missing username or password'}), 400
    
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT id, username, email, password_hash FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()
    
    if not user or not verify_password(password, user[3]):
        return jsonify({'message': 'Invalid credentials'}), 401
    
    # Generate JWT token - handle different PyJWT versions
    try:
        token = jwt.encode({
            'user_id': user[0],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7)
        }, app.config['SECRET_KEY'], algorithm='HS256')
        
        # Handle different PyJWT versions
        if isinstance(token, bytes):
            token = token.decode('utf-8')
            
    except Exception as e:
        return jsonify({'message': 'Token generation failed'}), 500
    
    return jsonify({
        'token': token,
        'user': {
            'id': user[0],
            'username': user[1],
            'email': user[2]
        }
    }), 200

@app.route('/api/articles', methods=['GET'])
def get_articles():
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT a.id, a.title, a.content, u.username, a.created_at
        FROM articles a
        JOIN users u ON a.author_id = u.id
        ORDER BY a.created_at DESC
    ''')
    
    articles = []
    for row in cursor.fetchall():
        articles.append({
            'id': row[0],
            'title': row[1],
            'content': row[2],
            'author': row[3],
            'created_at': row[4]
        })
    
    conn.close()
    return jsonify({'articles': articles}), 200

@app.route('/api/articles/<int:article_id>', methods=['GET'])
def get_article(article_id):
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT a.id, a.title, a.content, u.username, a.author_id, a.created_at
        FROM articles a
        JOIN users u ON a.author_id = u.id
        WHERE a.id = ?
    ''', (article_id,))
    
    article = cursor.fetchone()
    conn.close()
    
    if not article:
        return jsonify({'message': 'Article not found'}), 404
    
    return jsonify({
        'article': {
            'id': article[0],
            'title': article[1],
            'content': article[2],
            'author': article[3],
            'author_id': article[4],
            'created_at': article[5]
        }
    }), 200

@app.route('/api/articles', methods=['POST'])
@token_required
def create_article(current_user_id):
    data = request.get_json()
    title = data.get('title')
    content = data.get('content')
    
    if not title or not content:
        return jsonify({'message': 'Title and content are required'}), 400
    
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    
    cursor.execute(
        'INSERT INTO articles (title, content, author_id) VALUES (?, ?, ?)',
        (title, content, current_user_id)
    )
    
    article_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return jsonify({
        'message': 'Article created successfully',
        'article_id': article_id
    }), 201

@app.route('/api/articles/<int:article_id>', methods=['PUT'])
@token_required
def update_article(current_user_id, article_id):
    data = request.get_json()
    title = data.get('title')
    content = data.get('content')
    
    if not title or not content:
        return jsonify({'message': 'Title and content are required'}), 400
    
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    
    # Check if article exists and user is the author
    cursor.execute('SELECT author_id FROM articles WHERE id = ?', (article_id,))
    article = cursor.fetchone()
    
    if not article:
        conn.close()
        return jsonify({'message': 'Article not found'}), 404
    
    if article[0] != current_user_id:
        conn.close()
        return jsonify({'message': 'Unauthorized'}), 403
    
    # Update article
    cursor.execute(
        'UPDATE articles SET title = ?, content = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?',
        (title, content, article_id)
    )
    
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Article updated successfully'}), 200

@app.route('/api/articles/<int:article_id>', methods=['DELETE'])
@token_required
def delete_article(current_user_id, article_id):
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    
    # Check if article exists and user is the author
    cursor.execute('SELECT author_id FROM articles WHERE id = ?', (article_id,))
    article = cursor.fetchone()
    
    if not article:
        conn.close()
        return jsonify({'message': 'Article not found'}), 404
    
    if article[0] != current_user_id:
        conn.close()
        return jsonify({'message': 'Unauthorized'}), 403
    
    # Delete article
    cursor.execute('DELETE FROM articles WHERE id = ?', (article_id,))
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Article deleted successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5328)
