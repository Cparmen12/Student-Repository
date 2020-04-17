from flask import Flask, render_template

app: Flask = Flask(__name__)

@app.route('/Hello')

def hello() -> str: 
    return "hello emily, thanks for the food" 

@app.route('/sample_template')
def template_demo()-> str:
    return render_template('parameters.html',
                            my_header="My Stevens Respoitory",
                            my_param = "My custom parameter")


app.run(debug=True)    