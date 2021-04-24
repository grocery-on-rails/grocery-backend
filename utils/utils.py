def extract_basic_info(products, isAdmin=False):
    # If isAdmin is True, category and stock info will be retained
    basic_products = []
    is_iterable = True
    if not isinstance(products, list):
        products = [products]
        is_iterable = False
    for product in products:
        product_basic = {}
        try:
            product_basic['_id'] = product['_id']
            product_basic['name'] = product['name']
            product_basic['price'] = product['price']
            product_basic['discount'] = product['discount']
            product_basic['stock'] = int(product['stock'])
            if(len(product['image_list']) > 0):
                product_basic['image'] = product['image_list'][0]
            else:
                product_basic['image'] = None
            if isAdmin:
                product_basic['subcategory'] = product['subcategory']
        except KeyError:
            print("Failed to locate the correct key in the dicionary.")
            exit(1)
        basic_products.append(product_basic)
    return basic_products if is_iterable else basic_products[0]

def wrap_category_info(categories):
    category_info = []
    for category in categories:
        categrory_dict = {}
        categrory_dict['title'] = category['category']
        categrory_dict['content'] = []
        for subcat in category['subcategory']:
            categrory_dict['content'].append({'title': subcat, 'image': 'https://via.placeholder.com/100'})
        category_info.append(categrory_dict)
    return category_info
