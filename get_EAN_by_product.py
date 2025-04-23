import requests

URL = "https://world.openfoodfacts.org/cgi/search.pl"

def get_ean_by_product(product_name):
    params = {
        "search_terms": product_name,
        "search_simple": 1,
        "action": "process",
        "json": 1
    }

    try:
        response = requests.get(URL, params=params)
        response.raise_for_status()
        data = response.json()

        ean_list = []
        for product in data.get("products", []):
            name = product.get("product_name", "Unknown")
            ean = product.get("code", "Unknown")
            print(f"Product: {name} | EAN: {ean}")
            ean_list.append((name, ean))
        return ean_list

    except requests.exceptions.RequestException as e:
        return f"Error during API request: {e}"
    except ValueError:
        return f"Error decoding the response as JSON."


def main():
    product = input("Please enter product name: ")
    get_ean_by_product(product)


if __name__ == "__main__":
    main()
