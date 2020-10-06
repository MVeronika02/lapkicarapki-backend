from flask import Flask, request, jsonify, redirect, url_for
from flask_cors import CORS, cross_origin
from models import categoriesAnimal, productsFiltred, paginationProduct, dataReview,\
    detailsProductDB, categoriesOneAnimal, checkUserInDB
from psycopg2 import *
from math import ceil
import json
import jwt
import datetime

SECRET_KEY = "hkBxrbZ9Td4QEwgRewV6gZSVH4q78vBia4GBYuqd09SsiMsIjH"

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


@app.route('/registration', methods=['POST'])
def record_user():
    try:
        user_info = request.get_json()
        cursor = CONN.cursor()
        cursor.execute("""INSERT INTO public.users(
    	                            id, user_name, user_phone, user_email, user_password)
    	                            VALUES (%(product_id)s, %(name_reviewer)s, %(stars_product)s, %(text_review)s);""",
                   user_info)
        CONN.commit()
        cursor.close()
        return jsonify("sucess")
    except Exception as error:
        error_string = str(error)
        print(error_string)
        return error_string


@app.route('/user', methods=['GET'])
@cross_origin()
def loginCheckFunction():
    input_name = request.args.get('login')
    input_password = request.args.get('password')
    user_data_from_db = checkUserInDB(input_name, input_password)
    list_user_data = {}
    for row in user_data_from_db:
        list_user_data['id'] = row[0]
        list_user_data['user_name'] = row[1]
        list_user_data['user_password'] = row[2]
        list_user_data['user_email'] = row[3]
    if len(list_user_data) == 0:
        return jsonify({"success": False, "result": 'user not exist', "Elapse_time": 0})
    else:
        timeLimit = datetime.datetime.utcnow() + datetime.timedelta(minutes=30) #set limit for user
        payload = {"user_name": input_name, "user_password": input_password, "exp": timeLimit}
        # Generate token
        token = jwt.encode(payload, SECRET_KEY)
        return jsonify({"success": True, "result": list_user_data, "token": token.decode("UTF-8"),
                        "Elapse_time": f"{timeLimit}"})


@app.route('/check_access', methods=['GET'])
def checkToken():
    token_passed = request.headers.get('TOKEN', default=None)
    if token_passed == "undefined" or token_passed is None or token_passed == "":
        return jsonify({"success": False, "message": "you are not verified"})
    data = jwt.decode(token_passed, SECRET_KEY, algorithms=['HS256'])
    jwt_name = data['user_name']
    jwt_password = data['user_password']
    answer_check_user = checkUserInDB(jwt_name, jwt_password)
    list_info_user = {}
    for row in answer_check_user:
        list_info_user['id'] = row[0]
        list_info_user['user_name'] = row[1]
        list_info_user['user_password'] = row[2]
    if len(list_info_user) == 0:
        return jsonify({'result': "not exist user"})
    return jsonify({"success": True, "message": "You Are verified"})


if __name__ == '__main__':
    app.run(debug=True)
