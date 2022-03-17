import os

from flask_app.flask_app import app
from flask_app.routes.route_browser import routes_browser
from flask_app.routes.route_api import routes_api


FLASK_APP = app

routes_browser(app)
routes_api(app)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
