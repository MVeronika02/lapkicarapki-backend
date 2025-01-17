from config import CONECTIONPG


def categoriesAnimal():
    cursor = CONECTIONPG.cursor()
    cursor.execute("""select id_animal, id_category, name_category, url_category_image
                from categories_for_animals""")
    records = cursor.fetchall()
    cursor.close()
    return records


def paginationProduct(limit, page):
    cursor = CONECTIONPG.cursor()
    str_query = """select id_category, id_product, name_product, price_product, description_product, url_image_product 
                        from products_for_animals
                        order by id_product
                        limit {limit} offset {limit} * ({page} -1)
                         """.format(limit=limit, page=page)
    cursor.execute(str_query)
    records = cursor.fetchall()
    cursor.close()
    cursor = CONECTIONPG.cursor()
    str_query_count = """select count(*) from products_for_animals"""
    cursor.execute(str_query_count)
    count = cursor.fetchall()
    cursor.close()
    return records, count


def productsCategory(animal, category):
    cursor = CONECTIONPG.cursor()
    str_query = """select id_animal, id_category, id_product, name_product, price_product, url_image_product 
                            from products_for_animals
                            WHERE id_animal = {animal} and id_category = {category}
                             """.format(animal=animal, category=category)
    cursor.execute(str_query)
    records = cursor.fetchall()
    print(records, 'rec')
    cursor.close()
    return records


def paginationProductsCategory(limit, page, animal, category):
    cursor = CONECTIONPG.cursor()
    str_query = """select id_animal, id_category, id_product, name_product, price_product, url_image_product
                        from products_for_animals
                        where id_animal = {animal} and id_category = {category}
                        order by id_product
                        limit {limit} offset {limit} * ({page} -1)
                         """.format(limit=limit, page=page, animal=animal, category=category)
    cursor.execute(str_query)
    records = cursor.fetchall()
    cursor.close()
    cursor = CONECTIONPG.cursor()
    str_query_count = """select count(*) from products_for_animals
                            where id_animal = {animal} and id_category = {category}
                            """.format(animal=animal, category=category)
    cursor.execute(str_query_count)
    count = cursor.fetchall()
    cursor.close()
    return records, count


def productsFiltred(value_min, value_max, limit, page):
    cursor = CONECTIONPG.cursor()
    str_query = """select id_category, id_product, name_product, price_product, description_product, url_image_product 
                    from products_for_animals
                    WHERE price_product BETWEEN {_value_min} and {_value_max}
                    order by id_product
                    limit {limit} offset {limit} * ({page} -1)
                     """.format(_value_min=value_min, _value_max=value_max, limit=limit, page=page)
    cursor.execute(str_query)
    records = cursor.fetchall()
    cursor.close()
    return records


def detailsProductDB(id):
    cursor = CONECTIONPG.cursor()
    str_query = """select id_category, id_product, name_product, price_product, description_product, url_image_product 
                        from products_for_animals
                        WHERE id_product = {id}
                         """.format(id=id)
    cursor.execute(str_query)
    records = cursor.fetchall()
    cursor.close()
    return records


def dataReview(id, offset, limit):
    cursor = CONECTIONPG.cursor()
    str_query = """select id_product, reviewer_name, numbers_of_stars, text_review, to_char(review_date, 'dd.mm.YYYY')
                        from reviews
                        where id_product = {id}
                        order by id_product
                        limit {limit} offset {limit} * ({offset} -1)
                        """.format(id=id, offset=offset, limit=limit)
    cursor.execute(str_query)
    records = cursor.fetchall()
    cursor.close()
    cursor = CONECTIONPG.cursor()
    str_tmp_count = """select count(*) from reviews where id_product = {id}""".format(id=id)
    cursor.execute(str_tmp_count)
    count = cursor.fetchall()
    cursor.close()
    return records, count


def checkUserInfoDB(input_name, input_password):
    cursor = CONECTIONPG.cursor()
    str_query = """select id, user_name, user_phone, user_email, user_password
                                from users
                                where user_name = '{name}' and user_password = '{password}'
                                """.format(name=input_name, password=input_password)
    cursor.execute(str_query)
    records = cursor.fetchall()
    cursor.close()
    print(records)
    return records


def checkUserInDB(jwt_name, jwt_password):
    cursor = CONECTIONPG.cursor()
    str_query = """select id, user_name, user_email, user_password
                            from users
                            where user_name = '{name}' and user_password = '{password}'
                            """.format(name=jwt_name, password=jwt_password)
    cursor.execute(str_query)
    records = cursor.fetchall()
    cursor.close()
    print(records)
    return records


def allOrdersUser(idUser, offset, limit):
    cursor = CONECTIONPG.cursor()
    str_query = """select
                        id_order,
                        delivery_date,
                        name_delivery_type,
                        name_payment_method,
                        id_shop_point,
                        name_shop,
                        address_shop,
                        working_hours,
                        user_city,
                        count_product,
                        total_price_products
                    from orders as o
                    join order_delivery as od
                    on od.id_delivery_type = o.id_delivery_type
                    join payment_methods as pm
                    on pm.id_payment_method = o.id_payment_method
                    join shops_point as sp
                    on sp.id_shop_point = o.id_shop
                    where o.id_user = {id}
                    order by o.id_user
                    limit {limit} offset {limit} * ({offset} -1)""".format(id=idUser, offset=offset, limit=limit)
    cursor.execute(str_query)
    records = cursor.fetchall()
    cursor.close()
    cursor = CONECTIONPG.cursor()
    str_tmp_count = """select count(*) from orders where id_user = {id}""".format(id=idUser)
    cursor.execute(str_tmp_count)
    count = cursor.fetchall()
    cursor.close()
    return records, count

# def userDb()
