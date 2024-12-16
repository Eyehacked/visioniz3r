import sqlite3
import os

def export_sqlite_to_html(db_file, output_html_file):
    """
    Export an SQLite3 database to an HTML file with tables.
    :param db_file: Path to the SQLite3 database file
    :param output_html_file: Path to the output HTML file
    """
    if not os.path.exists(db_file):
        print(f"Error: Database file '{db_file}' does not exist.")
        return

    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        # Retrieve all table names in the database
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        if not tables:
            print("No tables found in the database.")
            return

        # Start building the HTML content
        html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SQLite Database Export</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
        }
        table {
            border-collapse: collapse;
            width: 100%;
            margin-bottom: 30px;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }
        th {
            background-color: #f4f4f4;
        }
        h2 {
            color: #333;
        }
    </style>
</head>
<body>
    <h1>SQLite Database Export</h1>
"""

        # Loop through each table and export its data
        for table_name in tables:
            table_name = table_name[0]
            html_content += f"<h2>Table: {table_name}</h2>"
            html_content += "<table>"

            # Get table data
            cursor.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()

            # Get column names
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = [info[1] for info in cursor.fetchall()]

            # Create the table headers
            html_content += "<thead><tr>"
            for column in columns:
                html_content += f"<th>{column}</th>"
            html_content += "</tr></thead><tbody>"

            # Populate the table rows
            for row in rows:
                html_content += "<tr>"
                for cell in row:
                    html_content += f"<td>{cell}</td>"
                html_content += "</tr>"

            html_content += "</tbody></table>"

        # Close the HTML structure
        html_content += """
</body>
</html>
"""

        # Write the HTML content to a file
        with open(output_html_file, "w", encoding="utf-8") as html_file:
            html_file.write(html_content)
        
        print(f"Export successful! HTML file saved as '{output_html_file}'")
    
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    
    finally:
        # Close the database connection
        if conn:
            conn.close()


# Example usage
if __name__ == "__main__":
    # Path to your SQLite database file
    database_file = "assets.db"
    # Output HTML file
    output_file = "database_export.html"
    export_sqlite_to_html(database_file, output_file)
