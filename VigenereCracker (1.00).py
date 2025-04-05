import itertools
import string
import sys
import textwrap
import os
try:
    import nltk
    from nltk.corpus import words
except ImportError:
    print("NLTK is required. Install it with 'pip install nltk' and run nltk.download('words').")
    sys.exit(1)

try:
    english_words_set = set(words.words())
except LookupError:
    nltk.download('words')
    english_words_set = set(words.words())

def print_ascii_header():
    RED = "\033[31m"
    BLUE = "\033[34m"
    BLACK = "\033[30m"
    RESET = "\033[0m"
    ascii_art = """██╗   ██╗██╗ ██████╗ ███████╗███╗   ██╗███████╗██████╗ ███████╗
██║   ██║██║██╔════╝ ██╔════╝████╗  ██║██╔════╝██╔══██╗██╔════╝
██║   ██║██║██║  ███╗█████╗  ██╔██╗ ██║█████╗  ██████╔╝█████╗  
╚██╗ ██╔╝██║██║   ██║██╔══╝  ██║╚██╗██║██╔══╝  ██╔══██╗██╔══╝  
 ╚████╔╝ ██║╚██████╔╝███████╗██║ ╚████║███████╗██║  ██║███████╗
  ╚═══╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝╚══════╝
                                                               
     ██████╗██████╗  █████╗  ██████╗██╗  ██╗███████╗██████╗    
    ██╔════╝██╔══██╗██╔══██╗██╔════╝██║ ██╔╝██╔════╝██╔══██╗   
    ██║     ██████╔╝███████║██║     █████╔╝ █████╗  ██████╔╝   
    ██║     ██╔══██╗██╔══██║██║     ██╔═██╗ ██╔══╝  ██╔══██╗   
    ╚██████╗██║  ██║██║  ██║╚██████╗██║  ██╗███████╗██║  ██║   
     ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝   
                                                               
"""
    header_line = BLUE + "C L A S S I C A L   V I G E N E R E   C R A C K E R" + " " + RED + "Version 1.00" + RESET
    signature_line = BLACK + "By Joshua M Clatney - Ethical Pentesting Enthusiast" + RESET
    full_header = (RED + ascii_art + RESET) + "\n" + header_line + "\n" + signature_line + "\n"
    print(full_header)

def vigenere(plaintext, key, a_is_zero=True):
    key = key.lower()
    if not all(ch in string.ascii_lowercase for ch in key):
        raise ValueError("Key must consist of letters only: {!r}".format(key))
    key_iter = itertools.cycle(map(ord, key))
    return "".join(
        chr(ord('a') + ((next(key_iter) - ord('a') + ord(ch) - ord('a')) + (0 if a_is_zero else 2)) % 26)
        if ch in string.ascii_lowercase else ch
        for ch in plaintext.lower()
    )

def vigenere_decrypt(ciphertext, key, a_is_zero=True):
    inverse = "".join(
        chr(ord('a') + (((26 if a_is_zero else 22) - (ord(k) - ord('a'))) % 26))
        for k in key
    )
    return vigenere(ciphertext, inverse, a_is_zero)

def is_english_sentence(text, threshold=0.80, min_words=2):
    tokens = text.split()
    if len(tokens) < min_words:
        return False
    valid_count = 0
    total_count = 0
    for token in tokens:
        cleaned = token.strip(string.punctuation).lower()
        if cleaned:
            total_count += 1
            if cleaned in english_words_set:
                valid_count += 1
    if total_count == 0:
        return False
    ratio = valid_count / total_count
    return ratio >= threshold

def cracking_attempt(ciphertext):
    print("\nCiphertext:")
    print("*" * 80)
    print(textwrap.fill(ciphertext, 80))
    print("*" * 80)
    path = input("Enter path to passkeys file (or press Enter to use default passkeys.txt): ").strip().strip('"')
    if path == "":
        path = "passkeys.txt"
    if not os.path.isfile(path):
        print("Passkeys file not found at:", path)
        return
    with open(path, "r") as f:
        keys = [line.strip() for line in f if line.strip()]
    found_valid = False
    for key in keys:
        plaintext = vigenere_decrypt(ciphertext, key)
        if is_english_sentence(plaintext):
            print("\nCracking successful, a valid English sentence has been found!")
            print("Key: {!r}".format(key))
            print("Decrypted plaintext:")
            print("=" * 80)
            print(textwrap.fill(plaintext, 80))
            print("=" * 80)
            found_valid = True
            break
    if not found_valid:
        print("No valid English sentence was found using the provided passkeys.")

def main():
    while True:
        print_ascii_header()
        ciphertext = input("Enter the ciphertext (or press Enter to exit): ").strip()
        if ciphertext == "":
            sys.exit(0)
        cracking_attempt(ciphertext)
        input("\nPress Enter to return to the home screen...")

if __name__ == "__main__":
    main()