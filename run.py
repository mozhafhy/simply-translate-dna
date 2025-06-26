import waitress
from flaskr import create_app

app = create_app()
waitress.serve(app, host="0.0.0.0", port=5000)
