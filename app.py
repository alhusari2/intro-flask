# from flask import Flask, render_template, request

# app = Flask(__name__)


# @app.route('/')
# def fancy():
#     return render_template('first_page.html')

# @app.route('/FancyName', methods=['POST'])
# def fancy_name():
#     if request.method == 'POST':
#         name = request.form['name'] #harus sama ['name'] dengan yang ada di first_page.html pada bagian input name="name"   <input type="name" name="name" required>
#         return render_template('second_page.html', name=name)

    
# if __name__ == '__main__':
#     app.run(debug=True)


# beda codingan sama yang di atas
import datetime
from flask import Flask, render_template, request

app = Flask(__name__)

entries = []

@app.route('/', methods=['GET', 'POST'])
def fancy():
    if request.method == "POST":
        entry_content = request.form.get("content")
        formated_data = datetime.datetime.today().strftime("%Y-%m-%d")
        entries.append((entry_content, formated_data))
    return render_template('home.html', entries=entries)


    
if __name__ == '__main__':
    app.run(debug=True)