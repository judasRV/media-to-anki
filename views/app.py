import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path

from models.media_clipper import MediaClipper
from models.subtitle_manager import SubtitleManager
from models.card_manager import CardManager

"""
    This is an early version of this project, 
    more features may be implemented in the 
    future.
"""

class App:
    """
        This class handles the GUI Elements
    """

    def __init__(self, root):

        self.root = root
        self.root.title("Media → Anki Cards")

        self.icon = tk.PhotoImage(file='icon.png')
        self.root.iconphoto(True, self.icon)
        self.root.resizable(False, False)

        self.media = None
        self.subtitles = None
        self.card_manager = CardManager()

        self.clip_counter = 1
        self.image_path = None

        self.build_ui()

    # ---------- TIME CONVERSION ----------

    def seconds_to_timestamp(self, seconds):

        h = int(seconds // 3600)
        m = int((seconds % 3600) // 60)
        s = seconds % 60

        return f"{h:02}:{m:02}:{s:06.3f}"

    def timestamp_to_seconds(self, ts):

        h, m, s = ts.split(":")
        return int(h) * 3600 + int(m) * 60 + float(s)

    """ 
        Builds the GUI for the app.
    """

    def build_ui(self):

        main = ttk.Frame(self.root, padding=10)
        main.grid(row=0, column=0, sticky="nsew")
        
        ttk.Button(main, text="Open Media", command=self.open_media)\
            .grid(row=0, column=0, padx=5, pady=5)

        ttk.Button(main, text="Open SRT", command=self.open_subtitles)\
            .grid(row=0, column=1, padx=5, pady=5)

        list_frame = ttk.Frame(main)
        list_frame.grid(row=1, column=0, columnspan=4, sticky="nsew")

        self.subtitle_list = tk.Listbox(list_frame, width=80, height=12)
        self.subtitle_list.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side="right", fill="y")

        self.subtitle_list.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.subtitle_list.yview)

        self.subtitle_list.bind("<<ListboxSelect>>", self.select_subtitle)

        ttk.Label(main, text="Front").grid(row=2, column=0, sticky="w")

        self.front_text = tk.Text(main, height=3, width=70)
        self.front_text.grid(row=3, column=0, columnspan=4, pady=5)

        ttk.Label(main, text="Back").grid(row=4, column=0, sticky="w")

        self.back_text = tk.Text(main, height=3, width=70)
        self.back_text.grid(row=5, column=0, columnspan=4, pady=5)

        ttk.Label(main, text="Start").grid(row=6, column=0)

        self.start_entry = ttk.Entry(main, width=15)
        self.start_entry.grid(row=6, column=1)

        ttk.Label(main, text="End").grid(row=6, column=2)

        self.end_entry = ttk.Entry(main, width=15)
        self.end_entry.grid(row=6, column=3)

        ttk.Button(main, text="Add Image", command=self.add_image)\
            .grid(row=7, column=0, pady=10)

        ttk.Button(main, text="Create Card", command=self.create_card)\
            .grid(row=7, column=2)

        ttk.Button(main, text="Export Deck", command=self.export_deck)\
            .grid(row=7, column=3)

        self.status = ttk.Label(main, text="")
        self.status.grid(row=8, column=0, columnspan=4)



    """
        Request the media file to open.
    """

    def open_media(self):

        path = filedialog.askopenfilename(
            filetypes=[("Media", "*.mp4 *.mkv *.mp3 *.wav")]
        )

        if path:
            self.media = MediaClipper(path)

    """
        Request the srt file to open.
    """

    def open_subtitles(self):

        path = filedialog.askopenfilename(
            filetypes=[("Subtitles", "*.srt")]
        )

        if path:

            self.subtitles = SubtitleManager(path)
            self.subtitle_data = self.subtitles.get_all()

            self.subtitle_list.delete(0, tk.END)

            for sub in self.subtitle_data:

                start = self.seconds_to_timestamp(sub["start"])
                end = self.seconds_to_timestamp(sub["end"])

                text = f"{start} → {end} | {sub['text']}"

                self.subtitle_list.insert(tk.END, text)

    def select_subtitle(self, event):

        if not self.subtitle_list.curselection():
            return

        index = self.subtitle_list.curselection()[0]
        sub = self.subtitle_data[index]

        self.front_text.delete("1.0", tk.END)
        self.front_text.insert("1.0", sub["text"])

        start = self.seconds_to_timestamp(sub["start"])
        end = self.seconds_to_timestamp(sub["end"])

        self.start_entry.delete(0, tk.END)
        self.start_entry.insert(0, start)

        self.end_entry.delete(0, tk.END)
        self.end_entry.insert(0, end)

    """
        Request the image to be added to the card.
    """

    def add_image(self):

        path = filedialog.askopenfilename(
            filetypes=[("Images", "*.png *.jpg *.jpeg")]
        )

        if path:
            self.image_path = path
            self.status.config(text=f"Image added: {Path(path).name}")

    """
       create the card and add to the list..
    """

    def create_card(self):

        if not self.media:
            messagebox.showerror("Error", "No media loaded")
            return

        start = self.timestamp_to_seconds(self.start_entry.get())
        end = self.timestamp_to_seconds(self.end_entry.get())

        audio_file = self.media.extract_audio(
            start,
            end,
            self.clip_counter
        )

        front = self.front_text.get("1.0", tk.END).strip()
        back = self.back_text.get("1.0", tk.END).strip()

        if self.image_path:

            img_name = Path(self.image_path).name
            front += f'<br><img src="{img_name}" width="400">'

            self.card_manager.media_files.append(self.image_path)

        self.card_manager.add_card(front, back, audio_file)

        self.status.config(text=f"Card {self.clip_counter} created")

        self.clip_counter += 1
        self.image_path = None

    """
        Export the deck once is done.
    """

    def export_deck(self):

        path = filedialog.asksaveasfilename(
            defaultextension=".apkg"
        )

        if path:
            self.card_manager.export(path)
            messagebox.showinfo("Done", "Deck exported")