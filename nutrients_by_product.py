import requests
import json

# Dictionary to store product data
product_nutrient_data = {}

def get_product_data(barcode):
    url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if data.get("status") == 1:
            product = data["product"]
            name = product.get("product_name", f"Unnamed Product ({barcode})")
            nutrients = product.get("nutriments", {})

            # Extract nutrient values
            product_nutrients = {
                "calories_100g": nutrients.get("energy-kcal_100g", "Not available"),
                "carbohydrates_100g": nutrients.get("carbohydrates_100g", "Not available"),
                "fat_100g": nutrients.get("fat_100g", "Not available"),
                "sugars_100g": nutrients.get("sugars_100g", "Not available"),
                "salt_100g": nutrients.get("salt_100g", "Not available"),
                "proteins_100g": nutrients.get("proteins_100g", "Not available")
            }

            # Save to main dictionary
            product_nutrient_data[name] = product_nutrients

            # Print summary
            print(f"\n📦 Product: {name}")
            for nutrient, value in product_nutrients.items():
                emoji = {
                    "calories_100g": "🔥",
                    "carbohydrates_100g": "🍞",
                    "fat_100g": "🧈",
                    "sugars_100g": "🍭",
                    "salt_100g": "🧂",
                    "proteins_100g": "🥩"
                }.get(nutrient, "🔹")
                print(f"{emoji} {nutrient.replace('_100g', '').capitalize()} (100g): {value}")

            return product
        else:
            print("❌ Product not found.")
    else:
        print(f"🚨 Failed to retrieve data. Status code: {response.status_code}")

def save_to_json(data, filename="product_data.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"\n💾 Data saved to {filename}")

# Example usage
get_product_data("5449000000996")  # Coca Cola

# Save the data to a JSON file
save_to_json(product_nutrient_data)