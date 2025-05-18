# we're importing the website folder into the main. thats why it's important to have main outside of the folder
from website import create_app
app = create_app()
# only if we run the main.py file will this line be executed. this runs the web server.

if __name__ == '__main__':
    app.run(debug=True)
