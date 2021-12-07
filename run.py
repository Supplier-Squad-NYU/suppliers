import atexit
from service import app
from service.supplier import db


def on_exit_app():
    """ Exit Supplier Service. """
    db.drop_all()
    db.session.close()
    db.engine.dispose()
    print("Exit Supplier Serivce")


atexit.register(on_exit_app)
app.config["DEBUG"] = True

if __name__ == "__main__":
    app.run(host="0.0.0.0")
