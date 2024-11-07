from flask import Flask, render_template

app = Flask(__name__)

@app.route('/expressions/')
def hello():
    # header1 
    ur_name = 'Botak licin'
    my_name = 'John Doe'

    # header2
    orange_ammount = 3
    apple_ammount = 5

    # header3
    first_name = 'Donald'
    second_name = 'Trump'

    # cara cepet pakai dictionary
    kwargs = {
        'ur_name': ur_name,
        'my_name': my_name,
        'orange_ammount': orange_ammount,
        'apple_ammount': apple_ammount,
        'first_name': first_name,
        'second_name': second_name
    }
    return render_template('jinja_expression.html', **kwargs)

if __name__ == '__main__':
    app.run(debug=True)