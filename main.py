# we're importing the website folder into the main. thats why it's important to have main outside of the folder
import os
from website import create_app
app = create_app()
from main import app
application = app

# only if we run the main.py file will this line be executed. this runs the web server.

if __name__ == '__main__':
    import socket

    preferred_port = int(os.environ.get('PORT', 5001))
    selected_port = preferred_port

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            sock.bind(('127.0.0.1', selected_port))
        except OSError:
            sock.bind(('127.0.0.1', 0))
            selected_port = sock.getsockname()[1]

    print(f"Starting app on port {selected_port}.")
    app.run(debug=True, port=selected_port)
