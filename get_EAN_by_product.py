import requests
import re
from difflib import SequenceMatcher

URL = "https://world.openfoodfacts.org/cgi/search.pl"

def clean_name(name):
    """Remove numbers and extra spaces from the product name for better comparison."""
    return re.sub(r'\d+', '', name).strip().lower()


def similar(a, b):
    """Return similarity ratio between cleaned strings (ignoring numbers)."""
    a_clean = clean_name(a)
    b_clean = clean_name(b)
    return SequenceMatcher(None, a_clean, b_clean).ratio()


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

        matched_products = []
        for product in data.get("products", []):
            name = product.get("product_name", "")
            ean = product.get("code", "")
            # Choose only EANs with 13 digits
            if similar(product_name, name) >= 0.9 and re.fullmatch(r"\d{13}", ean):
                matched_products.append({name: ean})

        return matched_products

    except requests.exceptions.RequestException as e:
        return f"Error during API request: {e}"
    except ValueError:
        return f"Error decoding the response as JSON."

def main():
    product = input("Please enter product name: ")
    result = get_ean_by_product(product)
    print(result)  # Remove the print statement before product release

if __name__ == "__main__":
    main()
