
def calculate_bmi(weight, height):
    return weight / (height ** 2)

def get_bmi_category(bmi):

    if bmi < 18.5:
        return "Untergewicht"
    elif 18.5 <= bmi < 24.9:
        return "Normalgewicht"
    elif 25 <= bmi < 29.9:
        return "Übergewicht"
    else:
        return "Adipositas"

def calculate_bmi(weight, height):
    """
    Berechnet den BMI basierend auf Gewicht und Größe.

    :param weight: Gewicht in Kilogramm
    :param height: Größe in Metern
    :return: BMI-Wert
    """
    return weight / (height ** 2)

def get_bmi_category(bmi):
    """
    Bestimmt die BMI-Kategorie basierend auf dem BMI-Wert.

    :param bmi: BMI-Wert
    :return: BMI-Kategorie
    """
    if bmi < 18.5:
        return "Untergewicht"
    elif 18.5 <= bmi < 24.9:
        return "Normalgewicht"
    elif 25 <= bmi < 29.9:
        return "Übergewicht"
    else:
        return "Adipositas"
