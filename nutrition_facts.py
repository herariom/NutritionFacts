import re
import config

class NutritionFacts:
    # Process the text for the nutrition facts

    def process_text(self, text):
        facts = {'Calories': 0, 'Fat': 0, 'Carbohydrates': 0, 'Protein': 0}
        regex = re.compile(config.CALORIE_NAME + '\s+[0-9]+', re.IGNORECASE)
        facts['Calories'] = self.validate_search(regex, text)

        regex = re.compile(r'total fat\s+[0-9]+', re.IGNORECASE)
        facts['Fat'] = self.validate_search(regex, text)

        regex = re.compile(r'total carb[a-zA-Z\.]+\s+[0-9]+', re.IGNORECASE)
        facts['Carbohydrates'] = self.validate_search(regex, text)

        regex = re.compile(r'protein\s+[0-9]+', re.IGNORECASE)
        facts['Protein'] = self.validate_search(regex, text)

        return facts


    # def process_fat(self, types_of_fat, text):
    #     all_fat = 0
    #     all_fat += self.add_together(types_of_fat, text)
    #     return all_fat
    #
    #
    # def add_together(self, types, text):
    #     added_fat = 0
    #
    #     for fat_type in types:
    #         pass
    #         regex = re.compile(fat_type + r'\s+[0-9]+', re.IGNORECASE)
    #         if self.validate_search(regex, text) >= 0:
    #             added_fat = self.validate_search(regex, text)
    #     return added_fat


    def validate_search(self, regex, text):
        try:
            temp = -1
            temp_regex = regex.search(text)
            if temp_regex:
                temp = int(re.sub("\D", "", temp_regex.group(0)))
                # Check for invalid numbers
                if temp <= 0:
                    temp = -1
        except ValueError:
            # Likely bad data
            temp = -1
        return temp
