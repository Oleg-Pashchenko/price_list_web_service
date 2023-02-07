import json

from flask import Flask, redirect, render_template

app = Flask(__name__, template_folder="templates")


@app.route('/')
def index():
    return redirect('/sources')


@app.route('/sources', methods=['GET'])
def sources():
    sources_v = ['OOO fdsfsd', 'OOOO vxcdfvdfv', 'OOO fdsfsd', 'OOOO vxcdfvdfv']
    defaults = json.load(open('defaults.json'))
    return render_template('sources.html', sources=sources_v, defaults=defaults)


@app.route('/item-category', methods=['GET'])
def item_category():
    return render_template('item_category.html')


@app.route('/items', methods=['GET'])
def items():
    return render_template('items.html')


@app.route('/import', methods=['GET'])
def import_items():
    return render_template('import.html')


@app.route('/prices', methods=['GET'])
def prices():
    return render_template('prices.html')


if __name__ == '__main__':
    app.run(debug=True, port=5000, use_reloader=False)
