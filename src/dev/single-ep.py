import sys
if sys.version_info < (3, 0):
    # Python 2
    import Tkinter as tk
    import tkMessageBox as messagebox
else:
    # Python 3
    import tkinter as tk
    from tkinter import messagebox

from _functions import *

root = tk.Tk()
root.geometry("600x400")  # Set the window size to 600x400
root.title("Update BEMA Transcripts")

## area for From and To
ep_from = tk.Text(root, height=1, width=6)  # Create the text area widget
ep_from.place(x=10, y=10)
ep_from.insert("1.0", "From")
ep_to = tk.Text(root, height=1, width=6)  # Create the text area widget
ep_to.place(x=100, y=10)
ep_to.insert("1.0", "To")

## area for Transcript preview
transcript_preview = tk.Text(root, height=25, width=50)  # Create the text area widget
transcript_preview.place(x=200, y=10)
transcript_preview.insert("1.0", "Transcript preivew")



button = tk.Button(root, text="Update transcripts", command=lambda: handle_button_click(ep_from, ep_to, transcript_preview))
button.place(x=10, y=50)

tk.mainloop()
