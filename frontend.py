"""
MIT License

Copyright (c) 2024 Aryan Kumar Sinha

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

# Import necessary modules from Flask and other dependencies
from flask import Flask, request, send_from_directory, redirect, url_for, jsonify, render_template
import threading
from backend import main as backend_main

# Initialize the Flask application
app = Flask(__name__)

@app.route('/')
def index():
    """
    Route for the home page.
    
    Returns:
    str: Rendered HTML template for the index page.
    """
    return render_template('index.html')

@app.route('/start_download', methods=['POST'])
def start_download():
    """
    Route to handle the start of the download process.
    
    This function expects a JSON payload with 'usernames' and 'interval_hours'.
    It starts the download process in a separate thread to avoid blocking the main application.
    
    Returns:
    tuple: A JSON response indicating success and an HTTP status code.
    """
    # Extract data from the JSON request
    data = request.json
    usernames = data['usernames']
    interval_hours = data['interval_hours']
    
    # Start the download process in a separate thread
    # This allows the web server to continue handling other requests
    thread = threading.Thread(target=backend_main, args=(usernames, interval_hours))
    thread.start()
    
    # Return a success message to the client
    return jsonify({"message": "Download started successfully"}), 200

# Run the Flask application if this script is executed directly
if __name__ == '__main__':
    # Start the Flask development server
    # Debug mode is set to True, which is useful for development but should be set to False in production
    app.run(debug=True)
