# How to contribute?

1. [Fork](https://github.com/eymenefealtun/all-words-in-all-languages/fork) the repository.

2. Create a folder for your language [here](https://github.com/eymenefealtun/all-words-in-all-languages/tree/main/) with the name of your language 
				 
3. Create a file for your language inside of the folder you created with the name of `YourLanguage.txt`.
    * **Format:** List all words in a **single line**, separated by commas (no spaces after the commas). **Do not use new lines or line breaks**, not even at the end of the file. No empty entries: no `,,` and no comma at the start or end.
    * **Case:** Please provide all words in lowercase unless the language specifically requires capitalization.
    * **Encoding:** Ensure the file is saved in **UTF-8** encoding (without BOM) to support special characters/scripts.
    * **Content:** Include only unique words; avoid duplicates within the same file.

4. Add your language to [`languages.json`](https://github.com/eymenefealtun/all-words-in-all-languages/blob/main/languages.json) with its English name (the same as the folder name) and its native name:

    ```json
    {"name": "YourLanguage", "native": "Native name of your language"},
    ```

5. Check your file and update the **Available Languages** table in `README.md` (requires [Python](https://www.python.org/downloads/) 3.9 or newer):

    ```
    python scripts/validate.py YourLanguage
    python scripts/build_readme.py
    ```

    * `validate.py` lists **errors** (rule violations such as line breaks, empty entries or duplicates) that must be fixed, and **warnings** (entries with digits, symbols, spaces or another alphabet) worth a look but fine if your language really writes words that way.
    * `build_readme.py` sorts the table, counts the words and updates the language count for you. Do not edit the table by hand.

6. If you collected the words from an external dataset, add the link to the **Sources** section at the bottom of the `README.md`.

7. Submit a pull request. The same checks run automatically on every pull request.