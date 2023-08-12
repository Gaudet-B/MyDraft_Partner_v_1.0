from draft_app import app
from draft_app.controllers import users, players, soup, api

if __name__ == "__main__":
    app.run(debug=True)