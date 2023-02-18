import json

from flask import Flask, redirect, render_template, request, jsonify, send_file
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
    db.add_category(name)
    return redirect('/item-category')


@app.route('/item-category/edit', methods=["POST"])
def edit_category():
    old_name = request.form['old-name']
    new_name = request.form['new-name']
    db.change_category(old_name, new_name)
    return redirect('/item-category')


@app.route('/item-category/delete', methods=["POST"])
def delete_category():
    delete_name = request.form['delete-name']
    db.delete_category(delete_name)
    return redirect('/item-category')


@app.route('/item-category/edit-order', methods=["POST"])
def edit_order():
    to_update = []
    for idx, category in enumerate(request.form):
        to_update.append({'name': category, 'order_index': idx + 1})

    db.change_order(to_update)
    return redirect('/item-category')


@app.route('/items', methods=['GET'])
def items():
    categories = db.get_all_categories()
    products = db.get_all_items()
    print(items)
    return render_template('items.html', categories=categories, products=products)


# TODO: FROM THIS
@app.route('/items/add', methods=["POST"])
def add_item():
    name = request.form.get('item-add-name')
    category = request.form.get('item-add-category')
    synonyms = request.form.get('item-add-synonyms')
    db.create_new_item(name, category, synonyms)
    return redirect('/items')


@app.route('/items/import-items', methods=["POST"])
def import_items_items():
    name = request.form.get('import_name')
    category = request.form.get('import_category')
    file = request.files['fileUpload_items']
    file.save('import-items.xlsx')
    data, _ = logic.load_from_excel(0, name, category, 'import-items.xlsx')
    for i in data:
        db.write_import_items(i[0], i[1])
    return redirect('/items')


@app.route('/items/import-synonims', methods=["POST"])
def import_synonims():
    idx = request.form.get('import_id')
    synonyms = request.form.get('import_synonyms')
    file = request.files['fileUpload_synonyms']
    file.save('import-synonims.xlsx')
    data, _ = logic.load_from_excel(0, idx, synonyms, 'import-synonims.xlsx')
    for i in data:
        db.write_import_synonyms(i[0], i[1])
    return redirect('/items')


@app.route('/items/export-items', methods=["POST"])
def export_items():
    logic.load_to_excel()
    return send_file('export.xlsx', as_attachment=True)



@app.route('/items/edit-items', methods=["POST"])
def edit_item():
    edit_product = request.form.get('edit-products')
    edit_category = request.form.get('edit-categories')
    edit_synonyms = request.form.get('edit-synonyms')
    print(edit_product, edit_category, edit_synonyms)
    db.edit_item(edit_product, edit_synonyms, edit_category)
    print('yes')
    return redirect('/items')


@app.route('/items/delete-item', methods=["POST"])
def delete_item():
    delete_item_v = request.form.get('delete-item')
    db.delete_item(delete_item_v)
    return redirect('/items')


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
    categories = db.get_all_categories()
    products = db.get_items()
    return render_template('prices.html', categories=categories, products=products)


@app.route('/prices/export', methods=['GET'])
def prices_export():
    logic.load_to_excel()
    return send_file('export.xlsx', as_attachment=True)



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000, use_reloader=False)
