from my_app import app
from my_app.controllers import user_controller, sighting_controller

if __name__ == "__main__":
    app.run(debug=True)