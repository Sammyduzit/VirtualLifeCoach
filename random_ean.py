import requests
import random

URL = "https://world.openfoodfacts.org/cgi/search.pl"

def get_random_ean():
    # Random page number to fetch different products
    page = random.randint(1, 100)

    params = {
        "search_simple": 1,
        "action": "process",
        "json": 1,
        "page_size": 100,
        "page": page
    }

    try:
        response = requests.get(URL, params=params)
        response.raise_for_status()
        data = response.json()

        products = data.get("products", [])
        if not products:
            print("No products found on this page. Try again.")
            return

        product = random.choice(products)
        ean = product.get("code", "Unknown")
        return ean

    except requests.exceptions.RequestException as e:
        return f"API error: {e}"
    except ValueError:
        return "Error parsing JSON response."


def main():
    get_random_ean()


if __name__ == "__main__":
    main()


