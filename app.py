from flask import Flask, request, jsonify, redirect, url_for
from flask_cors import CORS, cross_origin
from models import categoriesAnimal, productsFiltred, paginationProduct, dataReview,\
    detailsProductDB, categoriesOneAnimal
from psycopg2 import *
from math import ceil
import json

# import collections
app = Flask(__name__)
CORS(app)

# POSTGRES = {
#     'user': 'postgres',
#     'pw': 'postgres',
#     'db': 'postgres',
#     'host': 'localhost',
#     'port': '5433',
# }

CONN = connect(dbname='postgres', user='postgres',
               password='postgres', host='localhost', port=5433)


# app.config['DEBUG'] = True


@app.route('/categories', methods=['GET'])
@cross_origin()
def allCategoryForAnimal():
    try:
        result_function = categoriesAnimal()
        objects_list = []
        for row in result_function:
            d = {}
            d['idAnimal'] = row[0]
            d['idCategory'] = row[1]
            d['nameCategory'] = row[2]
            objects_list.append(d)
        return jsonify({'result': objects_list})
    except Exception as error:
        error_string = str(error)
        print(error_string)
        return error_string


@app.route('/categoryanimal', methods=['GET', 'POST'])
@cross_origin()
def allCategoryOneAnimal():
    try:
        id = request.args.get('id')
        result_function = categoriesOneAnimal(id)
        objects_list = []
        for row in result_function:
            d = {}
            d['idAnimal'] = row[0]
            d['idCategory'] = row[1]
            d['nameCategory'] = row[2]
            objects_list.append(d)
        return jsonify({'result': objects_list})
    except Exception as error:
        error_string = str(error)
        print(error_string)
        return error_string



@app.route('/paginationcontent', methods=['GET'])
@cross_origin()
def paginationContent():
    try:
        limit = request.args.get('limit')
        page = request.args.get('numberpage')
        rows, count_row = paginationProduct(limit, page)
        objects_list = []
        print(rows)
        print(count_row[0][0])
        for row in rows:
            tmp_row = {}
            tmp_row['idCategory'] = row[0]
            tmp_row['idProduct'] = row[1]
            tmp_row['nameProduct'] = row[2]
            tmp_row['priceProduct'] = row[3]
            tmp_row['descriptionProduct'] = row[4]
            tmp_row['urlImageProduct'] = row[5]
            objects_list.append(tmp_row)
        count_page = count_row[0][0] / int(limit)
        print(ceil(count_page))
        return jsonify({'result':
                            {'product': objects_list, 'count_page': ceil(count_page)}
                        })
    except Exception as error:
        error_string = str(error)
        print(error_string)
        return error_string


@app.route('/products', methods=['GET'])
@cross_origin()
def allProductsFiltred():
    try:
        value_min = request.args.get('valueMin')
        value_max = request.args.get('valueMax')
        limit = request.args.get('limit')
        page = request.args.get('numberpage')
        result_function = productsFiltred(value_min, value_max, limit, page)
        objects_list = []
        for row in result_function:
            tmp_row = {}
            tmp_row['idCategory'] = row[0]
            tmp_row['idProduct'] = row[1]
            tmp_row['nameProduct'] = row[2]
            tmp_row['priceProduct'] = row[3]
            tmp_row['descriptionProduct'] = row[4]
            tmp_row['urlImageProduct'] = row[5]
            objects_list.append(tmp_row)
        return jsonify({'result': objects_list})
    except Exception as error:
        error_string = str(error)
        print(error_string)
        return error_string


@app.route('/detailsproduct', methods=['GET'])
@cross_origin()
def detailsProduct():
    try:
        id = request.args.get('id')
        result_function = detailsProductDB(id)
        objects_list = []
        for row in result_function:
            tmp_row = {}
            tmp_row['idCategory'] = row[0]
            tmp_row['idProduct'] = row[1]
            tmp_row['nameProduct'] = row[2]
            tmp_row['priceProduct'] = row[3]
            tmp_row['descriptionProduct'] = row[4]
            tmp_row['urlImageProduct'] = row[5]
            objects_list.append(tmp_row)
        return jsonify({'result': objects_list})
    except Exception as error:
        error_string = str(error)
        print(error_string)
        return error_string


@app.route('/reviews', methods=['POST'])
def create_review():
    try:
      if request.method == 'POST':
        info_product = request.get_json()
        cursor = CONN.cursor()
        cursor.execute("""INSERT INTO public.reviews(
	                            product_id, reviewer_name, numbers_of_stars, text_review)
	                            VALUES (%(product_id)s, %(name_reviewer)s, %(stars_product)s, %(text_review)s);""",
                           info_product)
        CONN.commit()
        cursor.close()
        return jsonify("sucess")
    except Exception as error:
        error_string = str(error)
        print(error_string)
        return error_string


@app.route('/inforeviews', methods=['GET'])
def info_review():
    id = request.args.get('productid')
    offset = request.args.get('offset')
    limit = request.args.get('limit')
    result_function = dataReview(id, offset, limit)
    objects_list = []
    for row in result_function:
        tmp_dict = {}
        tmp_dict['product_id'] = row[0]
        tmp_dict['reviewer_name'] = row[1]
        tmp_dict['numbers_of_stars'] = row[2]
        tmp_dict['text_review'] = row[3]
        tmp_dict['review_date'] = row[4]
        objects_list.append(tmp_dict)
    return jsonify({'result': objects_list})


if __name__ == '__main__':
    app.run()
