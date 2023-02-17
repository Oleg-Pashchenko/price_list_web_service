import json

from flask import Flask, redirect, render_template, request, jsonify
from datetime import datetime

import logic
from db import get_suppliers, delete_supplier, add_supplier, get_all_categories
import db

app = Flask(__name__, template_folder="templates")
app.config['WTF_CSRF_ENABLED'] = False


@app.route('/')
def index():
    return redirect('/sources')


@app.route('/sources', methods=['GET'])
def sources():
    sources_v = get_suppliers()
    defaults = json.load(open('defaults.json'))
    return render_template('sources.html', sources=sources_v, defaults=defaults)


@app.route('/sources/defaults', methods=['POST'])
def sources_defaults_post():
    string_number = request.form['string_number']
    col_name = request.form['col_name']
    col_price = request.form['col_price']
    with open('defaults.json', 'w', encoding='UTF-8') as defaults:
        defaults.write(json.dumps({'string_number': string_number, 'column_name': col_name, 'column_price': col_price}))
    defaults.close()
    return redirect('/sources')


@app.route("/sources/edit", methods=['POST'])
def edit_source():
    supplier_name = request.form['supplier-name']
    suppliers = get_suppliers()
    if supplier_name in suppliers:
        delete_supplier(supplier_name)
    else:
        add_supplier(supplier_name)
    return redirect("/sources")


@app.route('/item-category', methods=['GET'])
def item_category():
    categories = get_all_categories()
    return render_template('item_category.html', categories=categories)


@app.route('/item-category/add', methods=["POST"])
def add_category():
    name = request.form['name']
    logic.add_category(name)
    return redirect('/item-category')


@app.route('/item-category/edit', methods=["POST"])
def edit_category():
    old_name = request.form['old-name']
    new_name = request.form['new-name']
    logic.change_category(old_name, new_name)
    return redirect('/item-category')


@app.route('/item-category/delete', methods=["POST"])
def delete_category():
    delete_name = request.form['delete-name']
    logic.delete_category(delete_name)
    return redirect('/item-category')


@app.route('/item-category/edit-order', methods=["POST"])
def edit_order():
    to_update = []
    for idx, category in enumerate(request.form):
        to_update.append({'name': category, 'order_index': idx + 1})

    logic.change_order(to_update)
    return redirect('/item-category')


@app.route('/items', methods=['GET'])
def items():
    return render_template('items.html')


@app.route('/import', methods=['GET'])
def import_items():
    current_date = str(datetime.now().strftime("%Y-%m-%d"))
    suppliers = get_suppliers()
    string_number = json.load(open('defaults.json'))['string_number']
    supplier_col = json.load(open('defaults.json'))['column_name']
    price_col = json.load(open('defaults.json'))['column_price']
    return render_template('import.html', suppliers=suppliers, current_date=current_date,
                           string_number=string_number, supplier_col=supplier_col, price_col=price_col)


@app.route('/import/preview', methods=['POST'])
def import_preview():
    try:
        row = int(request.form.get('string_number'))
        col1 = request.form.get('supplier_col')
        col2 = request.form.get('price_col')
        file = request.files['fileUpload']
        file.save('import.xlsx')
        data, preview = logic.load_from_excel(row, col1, col2)

        return '<tr class="new-row"><td>{}</td><td>{}</td></tr>'.format(data[0][0], data[0][1])
    except:
        return "Ошибка загрузки данных. Вероятно, вы указали неправильные параметры."

@app.route('/import', methods=['POST'])
def import_items_post():
    row = int(request.form.get('string_number'))
    col1 = request.form.get('supplier_col')
    col2 = request.form.get('price_col')
    date = request.form.get('selectDate')
    supplier = request.form.get('selectSupplier')
    file = request.files['fileUpload']
    file.save('import.xlsx')
    data, preview = logic.load_from_excel(row, col1, col2)
    db.write_items(data, date, supplier)
    return redirect('/import')


@app.route('/prices', methods=['GET'])
def prices():
    return render_template('prices.html')


"""

@app.route('/download')
def download():
    # path to the file to be downloaded
    filepath = '/path/to/file.txt'

    # send the file as an attachment to the client
    return send_file(filepath, as_attachment=True)
    """
if __name__ == '__main__':
    app.run(debug=True, port=5000, use_reloader=False)
