from flask import Flask, render_template
app = Flask(__name__)

@app.route("/map/")
def hello():
    return render_template('siginin.html')

if __name__ == "__main__":
    app.run(debug=True)