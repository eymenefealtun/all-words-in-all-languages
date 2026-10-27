# 1- Import the txt file into your project.
# For Kabyle, the word list is stored in 'Kabyle.txt' with one word per line, UTF-8 encoding.
# source: https://github.com/tasuqilt/Tamazight-Wordlist

# 2- If any pre-processing is required for the Kabyle word list, such as normalization or removing non-word lines, do it here.
# For Kabyle, no additional pre-processing is necessary as the file is clean and each line is a single word.

# 3- Provide the path to the Kabyle word list file.
KABYLE_WORDLIST_FILE = 'Kabyle.txt'

# 4- Assign to a string array using the method below;

def GetArrayOfWords():
    """
    Reads the Kabyle.txt file and returns a list of words (strings).
    Each line in Kabyle.txt is considered one word.
    The file should be in UTF-8 encoding.
    """
    with open(KABYLE_WORDLIST_FILE, 'r', encoding='utf-8') as file:
        words = [line.strip() for line in file if line.strip()]
    return words

# Example usage:
# kabyle_words = GetArrayOfWords()
# print(kabyle_words[:10])  # Show the first 10 words
