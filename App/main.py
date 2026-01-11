from App import app
from App import db



if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # create tables
    app.run(debug=True)