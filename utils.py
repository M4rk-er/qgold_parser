import web_requests

IMAGE_URL = 'https://images.jewelers.services/qgrepo/'
VIDE0_URL = 'https://images.jewelers.services/0/Videos/'
ADJUSTABLE_URL = 'https://jewelers.services/productcore/api/pd/'


def generate_family_ring_links(ring):
    rings_data = []
    family = ring.get('Family')
    product_detail = family.get('ProductDetails')
    for product in product_detail:
        style = product.get('Style')
        if style:
            link = web_requests.generate_link_for_ring(style)
            rings_data.append(link)
    return rings_data


def generate_ring_links(ring):
    rings_data = []
    sizes = ring.get('Sizes')
    for ring in sizes:
        ring_style = ring.get('Style')
        if ring_style:
            link = web_requests.generate_link_for_ring(ring_style)
            rings_data.append(link)
    return rings_data


def generate_list_links_stone(rings):
    all_api_links = []
    all_rings = rings['IndexedProducts']['Results']
    for ring in all_rings:
        is_famaly = ring.get('IsFamily')

        if is_famaly:
            family_id = ring['FamilyId']
            link = web_requests.generate_family_link_for_ring(family_id)
            all_api_links.append(link)
        else:
            style = ring['Style']
            link = web_requests.generate_link_for_ring(style)
            all_api_links.append(link)

    return all_api_links


def generate_links_list_adjustable(data):
    links_list = []
    results = data.get('IndexedProducts', {}).get('Results')
    for product in results:
        descr = product.get('URLDescription')
        style = product.get('Style')
        url = f'{ADJUSTABLE_URL}{descr}/{style}'
        links_list.append(web_requests.current_paramet_url(url))
    return links_list


def is_family(ring_data):
    return bool(
        ring_data.get('Family', {}).get('ProductDetails')
    )


def is_not_family(ring_data):
    if ring_data.get('Product') and ring_data.get('HasSizes'):
        return True
    return False


def description_parser(ring_data):
    description = ring_data.get('Product', {}).get('Description')
    return description


def size_parser(ring_data):
    size = ring_data.get('Product', {}).get('Size')
    return size


def msrp_parser(ring_data):
    msrp = ring_data.get('Product', {}).get('MSRP')
    return msrp


def amount_in_stoock_parser(ring_data):
    amount = ring_data.get('Product', {}).get('InStock')
    return amount


def images_list_parser(ring_data):
    images = []
    images_data = ring_data.get('Images')
    for image in images_data:
        file_name = image.get('FileName')
        image_link = f'{IMAGE_URL}{file_name}'
        images.append(image_link)
    return images


def video_parser(ring_data):
    video_data = ring_data.get('Video')
    if not video_data:
        return '-'
    file_name = video_data.get('FileName')
    video_link = f'{VIDE0_URL}{file_name}'
    return video_link


def product_detail_parser(ring_data):
    ring_detail = {}
    specs = ring_data.get('Specifications')
    for spec in specs:
        key = spec.get('Specification')
        value = spec.get('Value')
        ring_detail[key] = value
    return ring_detail


def main_parser(ring_data):

    description = description_parser(ring_data)
    size = size_parser(ring_data)
    msrp = msrp_parser(ring_data)
    in_stock = amount_in_stoock_parser(ring_data)
    image = images_list_parser(ring_data)
    video = video_parser(ring_data)
    details = product_detail_parser(ring_data)

    data = {
        'Description': description,
        'Size': size,
        'MSRP': msrp,
        'In_stock': in_stock,
        'Image': image,
        'Video': video,
        'Details': details,
    }

    return data


def make_advanced_details(ring_data):
    data = ring_data
    details = data.pop('Details')
    merged = {**data, **details}
    return merged


def get_longest_detail(details):
    max_length = list(
        map(
            lambda d: len(d.get('Details',  '')),
            details
        )
    )
    index = max_length.index(max(max_length))
    res = details[index].get('Details')
    return list(res.keys())


def turn_ring_info_into_dicts(ring):
    print('Преобразую информацию')
    end = []
    for elem in ring:
        data = main_parser(elem)
        end.append(data)
    return end


def generate_column_titles(formated_ring_data):
    column_titles = list(formated_ring_data[0].keys())
    all_details = get_longest_detail(formated_ring_data)
    column_titles.remove('Details')
    column_titles.extend(all_details)
    return column_titles
