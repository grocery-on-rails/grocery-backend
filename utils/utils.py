def extract_basic_info(products):
    basic_products = []
    for product in products:
        product_basic = {}
        try:
            product_basic['_id'] = product['_id']
            product_basic['name'] = product['name']
            product_basic['price'] = product['price']
            product_basic['image'] = product['image_list'][0]
        except KeyError:
            print("Failed to locate the correct key in the dicionary.")
            exit(1)
        basic_products.append(product_basic)
    return basic_products
