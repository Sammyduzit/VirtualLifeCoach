from BMI_calculater import calculate_bmi, get_bmi_category
from twilio_setup import setup_whatsapp_communication
from database import save_user_data, get_user_history


def get_user_input():
    print("Willkommen zum BMI-Rechner!")

    # User eingabe des Namens
    name = input("Bitte geben Sie Ihren Namen ein: ")

    # User eingabe des Alters
    age = input("Bitte geben Sie Ihr Alter ein: ")

    # User eingabe des Ziels
    goal = input("Bitte geben Sie Ihr Ziel ein (z.B. Gewichtsverlust, Muskelaufbau): ")

    # User eingabe des Geschlechts
    gender = input("Bitte geben Sie Ihr Geschlecht ein (m/w/d): ")

    # User eingabe des Ernährungsstils
    diet = input("Bitte beschreiben Sie Ihren Ernährungsstil (z.B. vegan, vegetarisch, omnivor): ")

    # User eingabe der täglichen Aktivität
    daily_activity = input("Bitte beschreiben Sie Ihre tägliche Aktivität (z.B. sitzend, aktiv): ")

    try:
        # User eingabe des Gewichts und der Größe
        weight = float(input("Bitte geben Sie Ihr Gewicht in Kilogramm ein: "))
        height = float(input("Bitte geben Sie Ihre Größe in Metern ein: "))

        # BMI berechnen
        bmi = calculate_bmi(weight, height)

        # BMI-Kategorie bestimmen
        category = get_bmi_category(bmi)

        # Ergebnis anzeigen
        print(f"\nHallo {name}! Ihr BMI beträgt: {bmi:.2f}")
        print(f"Sie fallen in die Kategorie: {category}")

        # Daten als Dictionary zurückgeben
        user_data = {
            "name": name,
            "age": age,
            "goal": goal,
            "gender": gender,
            "diet": diet,
            "daily_activity": daily_activity,
            "weight": weight,
            "height": height,
            "bmi": bmi,
            "category": category
        }

        # Benutzerdaten speichern
        save_user_data(name, user_data)

        # Benutzerhistorie abrufen
        history = get_user_history(name)
        print("\nIhre bisherigen Einträge:")
        for entry in history:
            print(f"Datum: {entry['timestamp']}, BMI: {entry['bmi']}")

        # WhatsApp kommunikations setup
        user_phone_number = "whatsapp:+491773285719" #Sam's output
        setup_whatsapp_communication(user_phone_number, f"Hallo {name}! Ihr BMI beträgt {bmi:.2f}.")

        return user_data

    except ValueError:
        print("Ungültige Eingabe. Bitte geben Sie Gewicht und Größe als Zahlen ein.")
        return None

if __name__ == "__main__":
    user_data = get_user_input()
    if user_data:
        print("\nDaten gesammelt:", user_data)


