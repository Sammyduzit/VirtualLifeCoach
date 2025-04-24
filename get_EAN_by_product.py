import requests
from difflib import SequenceMatcher


def search_products(query, page_size=50):
    url = "https://world.openfoodfacts.org/cgi/search.pl"
    params = {
        'search_terms': query,
        'search_simple': 1,
        'action': 'process',
        'json': 1,
        'page_size': page_size
    }
    response = requests.get(url, params=params)
    data = response.json()
    products = data.get('products', [])
    return products


def similar(a, b):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


def filter_and_deduplicate_products(query, products, threshold=0.6):
    filtered = []
    seen_names = set()

    for product in products:
        name = product.get('product_name_complete') or product.get('product_name', '')
        if not name or name in seen_names:
            continue

        if similar(query, name) >= threshold:
            ean = product.get('code', 'No EAN')
            filtered.append({"name": name, "ean": ean})
            seen_names.add(name)

    return filtered


def get_matched_products(query):
    products = search_products(query)
    return filter_and_deduplicate_products(query, products)


def main():
    query_input = input("Enter product name to search: ")
    matched_results = get_matched_products(query_input)
    print(matched_results) #remove in production


if __name__ == "__main__":
    main()
