import re
import config


def process_text(text):
    facts = {'Calories': 0, 'Fat': 0, 'Carbohydrates': 0, 'Protein': 0}
    regex = re.compile(config.CALORIE_NAME + r'\s+[0-9]+', re.IGNORECASE)
    facts['Calories'] = validate_search(regex, text)

    regex = re.compile(config.FAT_NAME + r'\s+[0-9]+', re.IGNORECASE)
    facts['Fat'] = validate_search(regex, text)

    regex = re.compile(config.CARBOHYDRATE_NAME + r'[a-zA-Z\.]+\s+[0-9]+', re.IGNORECASE)
    facts['Carbohydrates'] = validate_search(regex, text)

    regex = re.compile(config.PROTEIN_NAME + r'\s+[0-9]+', re.IGNORECASE)
    facts['Protein'] = validate_search(regex, text)

    return facts


def validate_search(regex, text):
    try:
        fact_string = regex.search(text)

        if fact_string:
            fact_value = re.search(r'\s+[0-9]+', fact_string.group(0))

            if fact_value:
                return int(fact_value.group(0))
            return -1
    except ValueError:
        # Likely bad data
        return -1
