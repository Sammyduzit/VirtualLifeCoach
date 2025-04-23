import requests

def get_product_data(barcode):
    url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if data.get("status") == 1:
            product = data["product"]
            name = product.get("product_name", "Unknown")
            nutrients = product.get("nutriments", {})

            calories = nutrients.get("energy-kcal_100g", "Not available")
            carbohydrates = nutrients.get("carbohydrates_100g", "Not available")
            fat = nutrients.get("fat_100g", "Not available")
            sugars = nutrients.get("sugars_100g", "Not available")
            salt = nutrients.get("salt_100g", "Not available")

            print(f"📦 Product: {name}")
            print(f"🔥 Calories (100g): {calories} kcal")
            print(f"🍞 Carbohydrates (100g): {carbohydrates} g")
            print(f"🧈 Fat (100g): {fat} g")
            print(f"🍭 Sugars (100g): {sugars} g")
            print(f"🧂 Salt (100g): {salt} g")

            return product
        else:
            print("❌ Product not found.")
    else:
        print(f"🚨 Failed to retrieve data. Status code: {response.status_code}")


def main():
    get_product_data("5449000000996")  # Coca Cola
    print()
    get_product_data("040000394129")  # Snickers


if __name__ == "__main__":
    main()

