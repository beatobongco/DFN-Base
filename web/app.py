from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
  app.logger.debug("This is a debug message.")
  return "Hello !!!@!"

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=1337, debug=True)
