import requests

def get_product_nutrients(barcode):
    """
    Callable function:
    Fetch product nutrient data from Open Food Facts by EAN.

    Returns a dictionary containing the product name and a sub-dictionary of nutrient data,
              or an error message.
    """
    url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
    response = requests.get(url)

    if response.status_code != 200:
        return {"error": f"Failed to retrieve data. Status code: {response.status_code}"}

    data = response.json()
    if data.get("status") != 1:
        return {"error": "Product not found."}

    product = data["product"]
    name = product.get("product_name", f"Unnamed Product ({barcode})")
    nutrients = product.get("nutriments", {})

    product_nutrients = {
        "calories_100g": nutrients.get("energy-kcal_100g", "Not available"),
        "carbohydrates_100g": nutrients.get("carbohydrates_100g", "Not available"),
        "fat_100g": nutrients.get("fat_100g", "Not available"),
        "sugars_100g": nutrients.get("sugars_100g", "Not available"),
        "salt_100g": nutrients.get("salt_100g", "Not available"),
        "proteins_100g": nutrients.get("proteins_100g", "Not available")
    }

    return {
        "product_name": name,
        "nutrients": product_nutrients
    }
