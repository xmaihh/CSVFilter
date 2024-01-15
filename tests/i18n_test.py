import sys
import os

sys.path.append("../csvfilter")
current_path = os.getcwd()

print("Current path:", current_path)

import csvfilter
import locale

# ````de.json```

# {
#   "title": "Dialogstation",
#   "ques-name": "Geben Sie Ihren Namen ein:",
#   "ques-age": "Geben Sie Ihr Alter ein:",
#   "ans-name": "Hallo, $name! Willkommen bei Phrase",
#   "ans-age": {
#     "one": "Du bist $count Jahr alt",
#     "other": "Du bist $count Jahre alt"
#   },
#   "ques-dob": "Geben Sie Ihr Geburtsdatum ein (JJJJ-MM-TT):",
#   "ans-dob": "Sie wurden am $dob geboren"
# }

# ````de.yaml```

# title: Dialogstation
# ques-name: "Geben Sie Ihren Namen ein:"
# ques-age: "Geben Sie Ihr Alter ein:"
# ans-name: Hallo, $name! Willkommen bei Phrase
# ans-age:
#   one: Du bist $count Jahr alt
#   other: Du bist $count Jahre alt
# ques-dob: "Geben Sie Ihr Geburtsdatum ein (JJJJ-MM-TT):"
# ans-dob: Sie wurden am $dob geboren


if __name__ == "__main__":
    # instantiate a new Translator class with the path to the data
    translator = csvfilter.i18n.Translator("csvfilter/data/")
    current_locale, encoding = locale.getlocale()
    lower_locale = current_locale.lower()
    print("Current system language:", current_locale)
    if "zh" in lower_locale or "chinese" in lower_locale or "china" in lower_locale:
        print("Current system language is Chinese")
    else:
        print("Current system language is not Chinese")

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
