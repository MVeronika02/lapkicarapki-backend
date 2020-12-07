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
    str_query = """select product_id, reviewer_name, numbers_of_stars, text_review, to_char(review_date, 'dd.mm.YYYY')
                        from reviews
                        where product_id = {id}
                        order by product_id
                        limit {limit} offset {limit} * ({offset} -1)
                        """.format(id=id, offset=offset, limit=limit)
    cursor.execute(str_query)
    records = cursor.fetchall()
    cursor.close()
    cursor = CONECTIONPG.cursor()
    str_tmp_count = """select count(*) from reviews where product_id = {id}""".format(id=id)
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
    str_query = """select id, user_name, user_phone, user_email, user_password
                            from users
                            where user_name = '{name}' and user_password = '{password}'
                            """.format(name=jwt_name, password=jwt_password)
    cursor.execute(str_query)
    records = cursor.fetchall()
    cursor.close()
    print(records)
    return records


# def userDb()


