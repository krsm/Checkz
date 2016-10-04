from flask import Flask, render_template
app = Flask(__name__)


@app.route('/<number>')
def hello(number):
    number
    number1 = number*2
    return render_template("Teste.html", number=number, number1=number1)

if __name__ == "__main__":
    app.run(debug=True)