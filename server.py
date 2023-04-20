from app import app
from app.controllers import login
from app.controllers import sightings

app.secret_key = "york"

if __name__ =="__main__":
    app.run(debug=True)