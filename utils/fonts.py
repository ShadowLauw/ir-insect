from tkinter import ttk
import tkinter.font as tkFont


def init_emoji_style(root, font_family="Noto Color Emoji", font_size=12):
    emoji_font = tkFont.Font(root=root, family=font_family, size=font_size)
    style = ttk.Style(root)

    style.configure("Emoji.TButton", font=emoji_font)
    style.configure("Emoji.TLabel", font=emoji_font)
    style.configure("Emoji.TCheckbutton", font=emoji_font)

    # Return a dict to use easily 
    return {
        "button": "Emoji.TButton",
        "label": "Emoji.TLabel",
        "checkbutton": "Emoji.TCheckbutton",
    }
