from flask import Flask, request, jsonify, Response, url_for, make_response
from flask_cors import CORS, cross_origin
from models import categoriesAnimal, paginationProduct, productsCategory, paginationProductsCategory, \
    productsFiltred, dataReview, detailsProductDB, checkUserInDB, allOrdersUser
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


# Категории животных

@app.route('/categories', methods=['GET'])
@cross_origin()
def allCategoryForAnimal():
    try:
        result_function = categoriesAnimal()
        objects_list = []
        for row in result_function:
            d = {}
            d['id_animal'] = row[0]
            d['id_category'] = row[1]
            d['name_category'] = row[2]
            d['url_image_category'] = row[3]
            objects_list.append(d)
        return jsonify({'result': objects_list})
    except Exception as error:
        error_string = str(error)
        print(error_string)
        return error_string


# Пагинация контента
@app.route('/paginationcontent', methods=['GET'])
@cross_origin()
def paginationContent():
    try:
        limit = request.args.get('limit')
        page = request.args.get('numberpage')
        rows, count_row = paginationProduct(limit, page)
        objects_list = []
        for row in rows:
            tmp_row = {}
            tmp_row['id_category'] = row[0]
            tmp_row['id_product'] = row[1]
            tmp_row['name_product'] = row[2]
            tmp_row['price_product'] = row[3]
            tmp_row['description_product'] = row[4]
            tmp_row['url_image_product'] = row[5]
            objects_list.append(tmp_row)
        count_page = count_row[0][0] / int(limit)
        # print(ceil(count_page))
        return jsonify({'result':
                            {'product': objects_list, 'count_page': ceil(count_page)}
                        })
    except Exception as error:
        error_string = str(error)
        print(error_string)
        return error_string


# Товары 1 категории
@app.route('/productsonecategory', methods=['GET'])
@cross_origin()
def allProductsOnCategory():
    try:
        animal = request.args.get('animal')
        category = request.args.get('category')
        rows = productsCategory(animal, category)
        objects_list = []
        for row in rows:
            tmp_row = {}
            tmp_row['id_animal'] = row[0]
            tmp_row['id_category'] = row[1]
            tmp_row['id_product'] = row[2]
            tmp_row['name_product'] = row[3]
            tmp_row['price_product'] = row[4]
            tmp_row['url_image_product'] = row[5]
            objects_list.append(tmp_row)
        if objects_list == 0:
            return jsonify({'success': False, 'result': 'not available'})
        else:
            return jsonify({'result': {'product': objects_list}})

    except Exception as error:
        error_string = str(error)
        print(error_string)
        return error_string


# Пагинация товаров 1 категории
@app.route('/paginationproductsonecategory', methods=['GET'])
@cross_origin()
def paginationProducts():
    try:
        limit = request.args.get('limit')
        page = request.args.get('numberpage')
        animal = request.args.get('animal')
        category = request.args.get('category')
        if animal == "undefined" or category == "undefined":
            return jsonify({'status': False, 'message': 'animal="undefined" or category="animal"'})
        rows, count_row = paginationProductsCategory(limit, page, animal, category)
        objects_list = []
        for row in rows:
            tmp_row = {}
            tmp_row['id_animal'] = row[0]
            tmp_row['id_category'] = row[1]
            tmp_row['id_product'] = row[2]
            tmp_row['name_product'] = row[3]
            tmp_row['price_product'] = row[4]
            tmp_row['url_image_product'] = row[5]
            objects_list.append(tmp_row)
        count_page = count_row[0][0] / int(limit)
        return jsonify({'result':
                            {'product': objects_list, 'count_page': ceil(count_page)}
                        })
    except Exception as error:
        error_string = str(error)
        print(error_string)
        return error_string


# Фильтр товара по параметрам
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
            tmp_row['id_category'] = row[0]
            tmp_row['id_product'] = row[1]
            tmp_row['name_product'] = row[2]
            tmp_row['price_product'] = row[3]
            tmp_row['description_product'] = row[4]
            tmp_row['url_image_product'] = row[5]
            objects_list.append(tmp_row)
        return jsonify({'result': objects_list})
    except Exception as error:
        error_string = str(error)
        print(error_string)
        return error_string


# Детали товара
@app.route('/detailsproduct', methods=['GET'])
@cross_origin()
def detailsProduct():
    try:
        id = request.args.get('id')
        result_function = detailsProductDB(id)
        objects_list = []
        for row in result_function:
            tmp_row = {}
            tmp_row['id_category'] = row[0]
            tmp_row['id_product'] = row[1]
            tmp_row['name_product'] = row[2]
            tmp_row['price_product'] = row[3]
            tmp_row['description_product'] = row[4]
            tmp_row['url_image_product'] = row[5]
            objects_list.append(tmp_row)
        return jsonify({'result': objects_list})
    except Exception as error:
        error_string = str(error)
        print(error_string)
        return error_string


# Оставить отзыв о товаре
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
            return jsonify('success')
    except Exception as error:
        error_string = str(error)
        print(error_string)
        return error_string


# Просмотр отзывов о товаре
@app.route('/inforeviews', methods=['GET'])
def info_review():
    id = request.args.get('productid')
    offset = request.args.get('offset')
    limit = request.args.get('limit')
    result_function, count_tmp = dataReview(id, offset, limit)
    objects_list = []
    for row in result_function:
        tmp_dict = {}
        tmp_dict['product_id'] = row[0]
        tmp_dict['reviewer_name'] = row[1]
        tmp_dict['numbers_of_stars'] = row[2]
        tmp_dict['text_review'] = row[3]
        tmp_dict['review_date'] = row[4]
        objects_list.append(tmp_dict)
    count_page = count_tmp[0][0] / int(limit)
    return jsonify({'result': objects_list, 'count_page': ceil(count_page)})


# Регистрация на сайте
@app.route('/registration', methods=['POST'])
def registration_user():
    try:
        user_data = request.get_json()
        login = user_data['login']
        print(login, 'login')
        cursor = CONN.cursor()
        # TODO: добавить логин с фронта;
        query_str = """SELECT count(*) FROM users
                          WHERE user_name = '{login}';""".format(login=login)
        cursor.execute(query_str)
        records = cursor.fetchall()
        # TODO: правильно записать значение count из бд
        if records[0][0] == 0:
            # query_insert = """INSERT INTO users(user_name, user_phone, user_email, user_password)
            #                     VALUES (%(login)s, %(tel)s, %(email)s, %(password)s)
            #                     """, user_data
            query_insert = """INSERT INTO users(user_name, user_phone, user_email, user_password)
                                VALUES ('{login}', '{tel}', '{email}', '{password}')
                            """.format(login=user_data['login'], tel=user_data['tel'],
                                       email=user_data['email'], password=user_data['password'])
            cursor.execute(query_insert)
        else:
            return jsonify({'error': 'user exist', 'success': False, 'confirm': True})
        CONN.commit()
        cursor.close()
        return jsonify({'success': True, 'confirm': False})
    except Exception as error:
        error_string = str(error)
        print(error_string)
        return error_string


# Вход в личный кабинет
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
        list_user_data['user_phone'] = row[2]
        list_user_data['user_password'] = row[3]
        list_user_data['user_email'] = row[4]
    if len(list_user_data) == 0:
        return jsonify({'success': False, 'result': 'user not exist', 'Elapse_time': 0})
    else:
        timeLimit = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)  # set limit for user
        payload = {'user_name': input_name, 'user_password': input_password, 'exp': timeLimit}
        # Generate token
        token = jwt.encode(payload, SECRET_KEY)
        return jsonify({'success': True, 'result': list_user_data, 'token': token.decode("UTF-8"),
                        'Elapse_time': f'{timeLimit}'})


@app.route('/check_access', methods=['GET'])
def checkToken():
    token_passed = request.headers.get('TOKEN', default=None)
    if token_passed == 'undefined' or token_passed is None or token_passed == '':
        return jsonify({'success': False, 'message': 'you are not verified'})
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
    return jsonify({'success': True, 'message': 'You Are verified'})


# #Сохранение заказа в БД
@app.route('/placeorder', methods=['POST'])
def placeOrder():
    try:
        info_order = request.get_json()
        cursor = CONN.cursor()
        print(info_order['products'])
        if info_order['delivery']['street'] == '':
            query_insert = """INSERT INTO public.orders(
                                                user_name, user_surname, user_phone, user_email, user_city,
                                                delivery_type, shop_point_id, street, house, flat, delivery_date,
                                                payment_type, total_price_products, count_product, id_user)
                                     VALUES ('{name}', '{surname}', '{phone}', '{email}', '{city}', '{deliveryType}',
                                     '{shopId}', NULL, NULL, NULL, NULL, '{paymentType}', '{totalPrice}',
                                     '{countProducts}', '{idUser}')
                                RETURNING id_order
                                    """.format(name=info_order['user_name'], surname=info_order['user_surname'],
                                               phone=info_order['user_phone'], email=info_order['user_email'],
                                               city=info_order['user_city'], deliveryType=info_order['delivery_type'],
                                               shopId=info_order['shop_point_id'],
                                               paymentType=info_order['payment_type'],
                                               totalPrice=info_order['total_price'],
                                               countProducts=info_order['count_products'], idUser=info_order['id_user'])
        else:
            query_insert = """INSERT INTO public.orders(
                                    user_name, user_surname, user_phone, user_email, user_city, delivery_type,
                                    shop_point_id, street, house, flat, payment_type, total_price_products,
                                    count_product id_user)
                         VALUES ('{name}', '{surname}', '{phone}', '{email}', '{city}', '{deliveryType}', '{shopId}',
                                '{street}', '{house}', '{flat}', '{paymentType}', '{totalPrice}', '{countProducts}',
                                '{idUser}')
                        RETURNING id_order
                        """.format(name=info_order['user_name'], surname=info_order['user_surname'],
                                   phone=info_order['user_phone'], email=info_order['user_email'],
                                   city=info_order['user_city'], deliveryType=info_order['delivery_type'],
                                   shopId=info_order['shop_point_id'], street=info_order['delivery']['street'],
                                   house=info_order['delivery']['house'], flat=info_order['delivery']['flat'],
                                   paymentType=info_order['payment_type'], totalPrice=info_order['total_price'],
                                   countProducts=info_order['count_products'], idUser=info_order['id_user'])
        cursor.execute(query_insert)
        id_of_new_row = cursor.fetchone()[0]
        for product in info_order['products']:
            query_order_products = """INSERT INTO public.order_products(id_order_m, id_product_m)
                                                VALUES ({order}, {product})
                                """.format(order=id_of_new_row, product=product['id_product'])
            cursor.execute(query_order_products)
        if query_insert == 0:
            return jsonify({'success': False})

        CONN.commit()
        cursor.close()
        return jsonify({'success': True})

    except Exception as error:
        error_string = str(error)
        print(error_string, '4444')
        return error_string


# Зфбираем заказы в БД
@app.route('/myorders', methods=['GET'])
def getOrders():
    try:
        id = request.args.get('id')
        ordersDB = allOrdersUser(id)
        orders_list = []
        cursor = CONN.cursor()
        for row in ordersDB:
            dTmp = {
                'id_order': row[0],
                'delivery_date': row[1],
                'delivery_type': row[2],
                'shop_point_id': row[3],
                'payment_type': row[4],
                'user_city': row[5],
                'count_product': row[6],
                'total_price_products': row[7],
                'product': [],
            }
            query_shop = """select * from shops_point
                          where id_shops_point = {id}""".format(id=dTmp['shop_point_id'])
            cursor.execute(query_shop)
            records = cursor.fetchall()
            for row in records:
                dTmp['name_shop'] = row[1]
                dTmp['adress_shop'] = row[2]
                dTmp['working_hours'] = row[3]

            query_id = """select id_product_m from order_products
                                      where id_order_m = {id}""".format(id=dTmp['id_order'])
            cursor.execute(query_id)
            product_ids = cursor.fetchall()

            idProduct = 0
            for i in product_ids:
                for j in i:
                    idProduct = j
                    query_product = """select id_product, name_product, price_product, url_image_product
                                    from products_for_animals
                                    where id_product = {id}""".format(id=idProduct)
                    cursor.execute(query_product)
                    productInfo = cursor.fetchall()
                    for row in productInfo:
                        infoTmp = {}
                        print(row)
                        infoTmp['name_product'] = row[1]
                        infoTmp['price_product'] = row[2]
                        infoTmp['url_image_product'] = row[3]
                        dTmp['product'].append(infoTmp)
            orders_list.append(dTmp)
        print(orders_list, ' orderlist')
        CONN.commit()
        cursor.close()
        return jsonify({'result': orders_list})
    except Exception as error:
        error_string = str(error)
        print(error_string)
        return error_string


if __name__ == '__main__':
    app.run(debug=True, port="5000")
