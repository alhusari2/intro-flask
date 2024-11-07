from flask import Flask, render_template

app = Flask(__name__)

@app.route('/conditional-statement/')
def render_data_structure():
    company = "Apple"
    return render_template('conditional_statement.html', company=company)