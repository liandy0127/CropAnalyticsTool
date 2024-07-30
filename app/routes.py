from flask import request, render_template, jsonify
from app.utils import get_table_names, export_table_to_csv, get_db_conn
from app import app

@app.route('/')
def index():
    tables = get_table_names()
    return render_template('index.html', tables=tables)

@app.route('/soil')
def soil():
    return render_template('soil.html')

@app.route('/weather')
def weather():
    return render_template('weather.html')

@app.route('/export_table', methods=['POST'])
def export_table():
    table_name = request.form['table_name']
    export_path = request.form['export_path']
    
    if not table_name or not export_path:
        return "Please provide both table name and export path", 400
    
    try:
        export_file_path = export_table_to_csv(table_name, export_path)
        return f"Table {table_name} exported to {export_file_path}", 200
    except Exception as e:
        return str(e), 500

@app.route('/soil_data', methods=['GET'])
def soil_data():
    conn = get_db_conn()
    year = request.args.get('year')
    query = 'SELECT * FROM crops.soil_tests'
    if year:
        query += ' WHERE date_part(\'year\', dateOFREPORT) = %s'
        cur = conn.cursor()
        cur.execute(query, (year,))
    else:
        cur = conn.cursor()
        cur.execute(query)
    rows = cur.fetchall()
    columns = [desc[0] for desc in cur.description]
    conn.close()

    soil_data = [dict(zip(columns, row)) for row in rows]
    print("Fetched Data: ", soil_data)  # Debugging: Print fetched data
    return jsonify(soil_data)

@app.route('/weather_data', methods=['GET'])
def weather_data():
    conn = get_db_conn()
    month = request.args.get('month')
    query = 'SELECT * FROM crops.weather_reports'
    if month:
        query += ' WHERE date_part(\'month\', date) = %s'
        cur = conn.cursor()
        cur.execute(query, (month,))
    else:
        cur = conn.cursor()
        cur.execute(query)
    rows = cur.fetchall()
    columns = [desc[0] for desc in cur.description]
    conn.close()

    weather_data = [dict(zip(columns, row)) for row in rows]
    print("Fetched Data: ", weather_data)  # Debugging: Print fetched data
    return jsonify(weather_data)

@app.route('/get_columns', methods=['GET'])
def get_columns():
    conn = get_db_conn()
    query = "SELECT column_name FROM information_schema.columns WHERE table_name = 'soil_tests' AND table_schema = 'crops'"
    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    columns = [row[0] for row in rows]
    conn.close()

    print("Fetched Columns: ", columns)  # Debugging: Print fetched columns
    return jsonify(columns)

@app.route('/get_weather_columns', methods=['GET'])
def get_weather_columns():
    conn = get_db_conn()
    query = "SELECT column_name FROM information_schema.columns WHERE table_name = 'weather_reports' AND table_schema = 'crops'"
    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    columns = [row[0] for row in rows]
    conn.close()

    print("Fetched Weather Columns: ", columns)  # Debugging: Print fetched columns
    return jsonify(columns)
