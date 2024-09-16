from app import app
from utils.db import db
from utils.ma import ma

with app.app_context():
    db.create_all()
    ma.init_app(app)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")  