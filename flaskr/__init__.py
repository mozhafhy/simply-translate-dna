from flask import Flask
from flask_cors import CORS

def create_app():
  # create and configure the app
  app = Flask(__name__)
  CORS(app=app)

  # a simple endpoint that says hello
  @app.route('/')
  def hello():
      return 'Hello, World!'
    
  from flaskr import resource
  app.register_blueprint(resource.bp)

  return app
