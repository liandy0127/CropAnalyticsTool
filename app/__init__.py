print("Initializing Flask app")
from flask import Flask
import psycopg2
from psycopg2 import OperationalError

# Initialize Flask application
app = Flask(__name__)

# Configuration settings for the database
app.config['DB_NAME'] = "crops"
app.config['DB_USER'] = "postgres"
app.config['DB_PASSWORD'] = "160320"
app.config['DB_HOST'] = "localhost"
app.config['DB_PORT'] = "5432"

# Function to create a database connection
def get_db_conn():
    try:
        conn = psycopg2.connect(
            dbname=app.config['DB_NAME'],
            user=app.config['DB_USER'],
            password=app.config['DB_PASSWORD'],
            host=app.config['DB_HOST'],
            port=app.config['DB_PORT']
        )
        return conn
    except OperationalError as e:
        print(f"Error: {e}")
        return None

# Import routes after app initialization to avoid circular import issues
print("Importing routes")
from app import routes

# Example route for testing the database connection
@app.route('/test_db')
def test_db():
    conn = get_db_conn()
    if conn:
        return "Database connection successful!"
    else:
        return "Failed to connect to the database."

# Running the Flask application (for standalone runs)
if __name__ == "__main__":
    app.run(debug=True)
