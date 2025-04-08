import tkinter as tk
import tkinter.font as tkFont
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

def paste_clipboard_text():
    try:
        data = root.clipboard_get()
    except Exception:
        data = ""
    ciphertext_text.delete("1.0", tk.END)
    ciphertext_text.insert(tk.END, data)

def paste_clipboard_passkey():
    try:
        data = root.clipboard_get()
    except Exception:
        data = ""
    passkey_entry.delete(0, tk.END)
    passkey_entry.insert(tk.END, data)

def copy_to_clipboard():
    text = output_text.get("1.0", tk.END)
    root.clipboard_clear()
    root.clipboard_append(text)

def gui_crack():
    output_text.delete("1.0", tk.END)
    ciphertext = ciphertext_text.get("1.0", tk.END).strip()
    passkeys_path = passkey_entry.get().strip().replace('"', '').replace("'", "")
    if not passkeys_path:
        passkeys_path = "passkeys.txt"
    if not ciphertext:
        output_text.insert(tk.END, "Please enter the ciphertext in the input field.\n")
        return
    output_text.insert(tk.END, "Ciphertext:\n" + "*" * 80 + "\n")
    output_text.insert(tk.END, textwrap.fill(ciphertext, 80) + "\n")
    output_text.insert(tk.END, "*" * 80 + "\n")
    if not os.path.isfile(passkeys_path):
        output_text.insert(tk.END, f"Passkeys file not found at: {passkeys_path}\n")
        return
    with open(passkeys_path, "r") as f:
        keys = [line.strip() for line in f if line.strip()]
    found_valid = False
    for key in keys:
        try:
            plaintext = vigenere_decrypt(ciphertext, key)
        except Exception as e:
            continue
        if is_english_sentence(plaintext):
            output_text.insert(tk.END, "\nCracking successful, a valid English sentence has been found!\n")
            output_text.insert(tk.END, "Key: " + repr(key) + "\n")
            output_text.insert(tk.END, "Decrypted plaintext:\n")
            output_text.insert(tk.END, "=" * 80 + "\n")
            output_text.insert(tk.END, textwrap.fill(plaintext, 80) + "\n")
            output_text.insert(tk.END, "=" * 80 + "\n")
            found_valid = True
            break
    if not found_valid:
        output_text.insert(tk.END, "No valid English sentence was found using the provided passkeys.\n")

def clear_inputs():
    ciphertext_text.delete("1.0", tk.END)
    passkey_entry.delete(0, tk.END)
    output_text.delete("1.0", tk.END)

root = tk.Tk()
root.title("Classical Vigenère Cracker GUI v1.00")
mono_font = tkFont.Font(family="Courier", size=10)

header_frame = tk.Frame(root)
header_frame.pack(fill=tk.X, padx=5, pady=5)
ascii_art = (
    "██╗   ██╗██╗ ██████╗ ███████╗███╗   ██╗███████╗██████╗ ███████╗\n"
    "██║   ██║██║██╔════╝ ██╔════╝████╗  ██║██╔════╝██╔══██╗██╔════╝\n"
    "██║   ██║██║██║  ███╗█████╗  ██╔██╗ ██║█████╗  ██████╔╝█████╗  \n"
    "╚██╗ ██╔╝██║██║   ██║██╔══╝  ██║╚██╗██║██╔══╝  ██╔══██╗██╔══╝  \n"
    " ╚████╔╝ ██║╚██████╔╝███████╗██║ ╚████║███████╗██║  ██║███████╗\n"
    "  ╚═══╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝╚══════╝\n"
    "                                                               \n"
    "     ██████╗██████╗  █████╗  ██████╗██╗  ██╗███████╗██████╗    \n"
    "    ██╔════╝██╔══██╗██╔══██╗██╔════╝██║ ██╔╝██╔════╝██╔══██╗   \n"
    "    ██║     ██████╔╝███████║██║     █████╔╝ █████╗  ██████╔╝   \n"
    "    ██║     ██╔══██╗██╔══██║██║     ██╔═██╗ ██╔══╝  ██╔══██╗   \n"
    "    ╚██████╗██║  ██║██║  ██║╚██████╗██║  ██╗███████╗██║  ██║   \n"
    "     ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝   \n"
    "                                                               "
)
ascii_label = tk.Label(header_frame, text=ascii_art, fg="red", font=mono_font, justify="left")
ascii_label.pack(anchor="w")
title_frame = tk.Frame(header_frame)
title_frame.pack(anchor="w", pady=(2, 0))
title_label = tk.Label(title_frame, text="C L A S S I C A L   V I G E N E R E   C R A C K E R", fg="blue", font=mono_font)
title_label.pack(side="left")
version_label = tk.Label(title_frame, text="  Version 1.00", fg="red", font=mono_font)
version_label.pack(side="left")
signature_label = tk.Label(header_frame, text="By Joshua M Clatney - Ethical Pentesting Enthusiast", fg="black", font=mono_font)
signature_label.pack(anchor="w", pady=(2, 5))
input_frame = tk.Frame(root)
input_frame.pack(fill=tk.X, padx=5, pady=5)
ciphertext_label = tk.Label(input_frame, text="Ciphertext:")
ciphertext_label.grid(row=0, column=0, sticky=tk.W, padx=2, pady=2)
ciphertext_frame = tk.Frame(input_frame)
ciphertext_frame.grid(row=1, column=0, columnspan=2, padx=2, pady=2, sticky="w")
ciphertext_text = tk.Text(ciphertext_frame, height=5, width=70, font=mono_font)
ciphertext_text.grid(row=0, column=0)
paste_text_button = tk.Button(ciphertext_frame, text="Paste", command=paste_clipboard_text)
paste_text_button.grid(row=0, column=1, padx=5)
passkey_label = tk.Label(input_frame, text="Passkeys File Path:")
passkey_label.grid(row=2, column=0, sticky=tk.W, padx=2, pady=2)
passkey_frame = tk.Frame(input_frame)
passkey_frame.grid(row=2, column=1, padx=2, pady=2, sticky="w")
passkey_entry = tk.Entry(passkey_frame, width=40)
passkey_entry.insert(0, "Enter Path Here")
passkey_entry.grid(row=0, column=0)
paste_passkey_button = tk.Button(passkey_frame, text="Paste", command=paste_clipboard_passkey)
paste_passkey_button.grid(row=0, column=1, padx=5)
crack_button = tk.Button(input_frame, text="Crack", command=gui_crack)
crack_button.grid(row=3, column=0, columnspan=2, pady=5)
output_frame = tk.Frame(root)
output_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
output_label = tk.Label(output_frame, text="Output:")
output_label.pack(anchor="w")
output_area_frame = tk.Frame(output_frame)
output_area_frame.pack(fill=tk.BOTH, expand=True)
output_text = tk.Text(output_area_frame, height=15, width=80, font=mono_font)
output_text.grid(row=0, column=0, sticky="nsew")
copy_button = tk.Button(output_area_frame, text="Copy", command=copy_to_clipboard)
copy_button.grid(row=0, column=1, padx=5, sticky="n")
clear_button = tk.Button(output_area_frame, text="Clear", command=clear_inputs)
clear_button.grid(row=1, column=1, padx=5, pady=(5, 0), sticky="n")
output_area_frame.grid_rowconfigure(0, weight=1)
output_area_frame.grid_columnconfigure(0, weight=1)
root.mainloop()