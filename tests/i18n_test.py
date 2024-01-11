import sys
import os

sys.path.append("../csvfilter")
current_path = os.getcwd()

print("Current path:", current_path)

import csvfilter


if __name__ == "__main__":
    # instantiate a new Translator class with the path to the data
    translator = csvfilter.i18n.Translator("csvfilter/data/")

    name = "John Doe"
    print(translator.translate("ans-name", name=name))
    # Hello, John Doe! Welcome to Phrase

    # change the active locale to de
    translator.set_locale("de")
    print(translator.translate("ans-name", name=name))
    # Hallo, John Doe! Willkommen bei Phrase

    age = 30
    print(translator.translate("ans-age", count=age))
    # Du bist 30 Jahre alt

    dob = "1992-01-01"
    dob = csvfilter.i18n.parse_datetime(dob)

    print(translator.translate("ans-dob", dob=dob))
    # Sie wurden am January 01, 1992 geboren
