import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Progressbar
from spleeter.separator import Separator

class SpleeterApp:
    SUPPORTED_FORMATS = ['mp3', 'wav', 'ogg', 'm4a', 'wma', 'flac']

    def __init__(self, root):
        self.root = root
        self.root.title("Spleeter Vocal Isolator")
        self._build_ui()

    def _build_ui(self):
        self.file_path = tk.StringVar()
        self.output_format = tk.StringVar()
        self.processing = tk.BooleanVar(value=False)

        self._build_file_selector()
        self._build_format_entry()
        self._build_process_button()
        self._build_progress_bar()

    def _build_file_selector(self):
        self.select_file_button = tk.Button(self.root, text="Select File", command=self._select_file)
        self.select_file_button.pack()

    def _build_format_entry(self):
        self.format_label = tk.Label(self.root, text="Output Format")
        self.format_label.pack()
        self.format_entry = tk.Entry(self.root, textvariable=self.output_format)
        self.format_entry.pack()

    def _build_process_button(self):
        self.process_button = tk.Button(self.root, text="Process", command=self._start_processing)
        self.process_button.pack()

    def _build_progress_bar(self):
        self.progress = Progressbar(self.root, length=100, mode='indeterminate')
        self.progress.pack()

    def _select_file(self):
        self.file_path.set(filedialog.askopenfilename())

    def _start_processing(self):
        if not self._validate_inputs():
            return

        self.process_button.config(state='disabled')
        self.processing.set(True)
        threading.Thread(target=self._process_audio).start()
        self.root.after(100, self._update_progress)

    def _validate_inputs(self):
        if not os.path.isfile(self.file_path.get()):
            messagebox.showerror("Error", "Invalid file path")
            return False

        if self.output_format.get() not in self.SUPPORTED_FORMATS:
            messagebox.showerror("Error", "Invalid output format")
            return False

        return True

    def _process_audio(self):
        try:
            separator = Separator('spleeter:2stems')
            separator.separate_to_file(self.file_path.get(), '/output/path', codec=self.output_format.get())
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            self.processing.set(False)

    def _update_progress(self):
        if self.processing.get():
            self.progress.step()
            self.root.after(100, self._update_progress)
        else:
            self._processing_finished()

    def _processing_finished(self):
        self.progress.stop()
        self.process_button.config(state='normal')
        if not messagebox.askyesno("Success", "Audio processed successfully. Process another file?"):
            self.root.quit()

def main():
    root = tk.Tk()
    app = SpleeterApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()