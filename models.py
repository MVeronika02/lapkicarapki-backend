from config import CONECTIONPG


def categoriesAnimal():
    cursor = CONECTIONPG.cursor()
    cursor.execute("""select idAnimal, idCategory, nameCategory
                from category_for_animals""")
    records = cursor.fetchall()
    cursor.close()
    return records


def categoriesOneAnimal(id):
    cursor = CONECTIONPG.cursor()
    cursor.execute("""select idAnimal, idCategory, nameCategory
                    from category_for_animals
                    where idAnimal = {id}
                    """).format(id=id)
    records = cursor.fetchall()
    cursor.close()
    return records


def productsFiltred(value_min, value_max, limit, page):
    cursor = CONECTIONPG.cursor()
    str_query = """select idCategory, idProduct, nameProduct, priceProduct, descriptionProduct, urlImageProduct 
                    from products_for_animals
                    WHERE priceProduct BETWEEN {_value_min} and {_value_max}
                    order by idProduct
                    limit {limit} offset {limit} * ({page} -1)
                     """.format(_value_min=value_min, _value_max=value_max, limit=limit, page=page)
    cursor.execute(str_query)
    records = cursor.fetchall()
    cursor.close()
    return records


def detailsProductDB(id):
    cursor = CONECTIONPG.cursor()
    str_query = """select idCategory, idProduct, nameProduct, priceProduct, descriptionProduct, urlImageProduct 
                        from products_for_animals
                        WHERE idProduct = {id}
                         """.format(id=id)
    cursor.execute(str_query)
    records = cursor.fetchall()
    cursor.close()
    return records


def paginationProduct(limit, page):
    cursor = CONECTIONPG.cursor()
    str_query = """select idCategory, idProduct, nameProduct, priceProduct, descriptionProduct, urlImageProduct 
                        from products_for_animals
                        order by idProduct
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
    print(records)
    return records

