from flask import Flask, render_template

app = Flask(__name__)

class Galilemons:
    def __init__(self, first, second, third, fourth):
        self.first = first
        self.second = second
        self.third = third
        self.fourth = fourth
    


@app.route('/expressions/')
def hello():
    # header1 
    movies = ['The big boss', 'The big short', 'The big lebowski']
    car = {
        'brand': 'Toyota',
        'model': 'Corolla',
        'year': 2009
    }
    moon = Galilemons('Io', 'Europa', 'gany', 'callist')

    #using kwargs
    kwargs = {
        'movies': movies,
        'car': car,
        'moons': moon
    }
    return render_template('data_structures.html', **kwargs)

if __name__ == '__main__':
    app.run(debug=True)