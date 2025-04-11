# VigenereCracker
A simple Python script that will crack the classical implementation of the Vigenere Cipher. It uses a word-list to brute force the correct key and NLTK to identify English words / sentences.

Below is a sample README file in Markdown format that explains what the script does and how to use it.

---

# Classical Vigenère Cracker

## Overview

This Python script is designed to crack text encrypted with a modified Vigenère cipher by using a list of potential keys (passkeys). It leverages the Natural Language Toolkit (NLTK) to verify if a decrypted text is a valid English sentence. The script is interactive, prompting the user for ciphertext and the location of a passkeys file (default: `passkeys.txt`).

## Key Features

- **ASCII Art Header:**  
  Displays a visually appealing header with colored text, including the script title and version information.

- **Vigenère Cipher Implementation:**  
  Provides functions for both encryption (`vigenere`) and decryption (`vigenere_decrypt`) using a cyclic key. A special parameter `a_is_zero` is used to adjust the cipher’s offset.

- **English Sentence Detection:**  
  Uses NLTK’s English words corpus to determine if the decrypted text is likely to be a valid English sentence. This is done by checking the ratio of recognized English words in the text.

- **Brute-Force Key Cracking:**  
  Iterates through a list of passkeys (from a specified file) to decrypt the ciphertext. Once a decryption yields a valid English sentence, the script displays the successful key and the decrypted message.

- **User-Friendly Interface:**  
  Operates in a loop, allowing users to repeatedly input new ciphertexts until they choose to exit.

## Prerequisites

- **Python 3.x**  
- **NLTK (Natural Language Toolkit):**  
  Install via pip:  

  pip install nltk
  
  After installation, download the English words corpus by running:
  python import nltk
  nltk.download('words')
 
- **Passkeys File:**  
  A text file (by default named `passkeys.txt`) containing potential keys, one per line.

## How It Works

1. **Initialization:**  
   - The script attempts to import NLTK and load the English words corpus.
   - If NLTK or the corpus is missing, the user is prompted to install/download them.

2. **Display Header:**  
   - An ASCII art header is printed to introduce the tool.

3. **Vigenère Cipher Functions:**  
   - `vigenere(plaintext, key, a_is_zero=True)`: Encrypts the plaintext by cyclically applying the key.
   - `vigenere_decrypt(ciphertext, key, a_is_zero=True)`: Decrypts the ciphertext by generating an inverse key and reusing the encryption logic.

4. **English Sentence Verification:**  
   - `is_english_sentence(text, threshold=0.80, min_words=2)`: Splits the text into tokens, cleans punctuation, and checks if a sufficient percentage of words appear in the English words corpus.

5. **Cracking Process:**  
   - `cracking_attempt(ciphertext)`:  
     - Displays the ciphertext.
     - Prompts the user for a passkeys file path (defaulting to `passkeys.txt`).
     - Reads keys from the file and attempts decryption with each key.
     - If a valid English sentence is detected in the decrypted text, it prints the successful key and the plaintext.

6. **Main Loop:**  
   - The `main()` function continuously prompts the user for ciphertext until an empty input is received, at which point the script exits.

## How to Use

1. **Set Up Your Environment:**
   - Ensure Python 3.x is installed.
   - Install NLTK and download the necessary corpus:
     pip install nltk
     python -c "import nltk; nltk.download('words')
     
   - Create a `passkeys.txt` file in the same directory as the script, listing one potential key per line, or using the comprehensive one provided in this repository.

2. **Run the Script:**
   - Git clone or download the script, ensure the dependencies are installed, and open it.

3. **Enter Ciphertext:**
   - When prompted, enter the ciphertext you wish to decrypt.
   - If you have a custom passkeys file, enter its path; otherwise, press Enter to use the default `passkeys.txt` file or enter the path of the file.

4. **View the Results:**
   - If a valid English sentence is found, the script will display the key used and the decrypted message.
   - If no valid decryption is achieved, the script informs you and returns to the home screen.

## Customization and Considerations

- **`a_is_zero` Parameter:**  
  Adjust this parameter in the cipher functions if needed; it alters the offset used in the encryption/decryption process.

- **Passkeys File Format:**  
  Ensure the file contains one passkey per line and is accessible by the script. The one provided in this repository is formatted correctly, and contains the full English dictionary, men's names, women's names, pet names, slang, expletives, seasons, months and days. No substitution rules or other rules have been applied, it is one word per line. If you need substitution rules added, I recommend you download the Mentalist software to do this.

## Troubleshooting

- **NLTK or Corpus Errors:**  
  If you encounter errors related to NLTK, verify you have installed NLTK and downloaded the `words` corpus.
  
- **File Not Found:**  
  Ensure the passkeys file path is correct and the file exists.

---

**Author**

Joshua M Clatney (Clats97)

Ethical Pentesting Enthusiast

Copyright 2025 Joshua M Clatney (Clats97)
