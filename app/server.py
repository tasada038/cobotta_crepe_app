from web_app import app

if __name__ == '__main__':
    # Start Web App
    app.run(debug=True, use_reloader=False, use_debugger=False, host = 'localhost', port=5073, threaded=True)