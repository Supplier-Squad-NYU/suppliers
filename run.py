from service import app
from service.supplier import db
import atexit


def OnExitApp():
    db.drop_all()
    db.session.close()
    db.engine.dispose()
    print("Exit Supplier Serivce")


atexit.register(OnExitApp)
app.config["DEBUG"] = True

if __name__ == "__main__":
    app.run(host="0.0.0.0")
