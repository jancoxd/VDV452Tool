import zipfile
import os
import tempfile
import shutil
import tkinter as tk
from tkinter import filedialog, ttk
from datetime import datetime


def extract_vdv452_zip(zip_path):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall('extracted_files')
        for name in zip_ref.namelist():
            if name.lower() == 'menge_fzg_typ.x10':
                with zip_ref.open(name) as source, open('extracted_files/menge_fzg_typ.x10', 'wb') as target:
                    shutil.copyfileobj(source, target)
                break
        else:
            raise FileNotFoundError("menge_fzg_typ.x10 not found in the zip file")


def update_coordinates(content):
    updated_content = []
    for line in content:
        if line.startswith("rec;"):
            columns = line.split(";")
            columns[11] = columns[11] + "0"
            columns[12] = columns[12] + "0"
            updated_line = ";".join(columns)
            updated_content.append(updated_line)
        else:
            updated_content.append(line)
    return updated_content


def readlines_from_file(file_path):
    with open(file_path, 'r', encoding='ISO-8859-1') as file:
        content = file.readlines()
    return content

def add_new_line(content, new_id):
    new_line = f"rec;1000;{new_id};0;0;0;\"New Bus {new_id}\";0;\"NB{new_id}\""
    for index, line in enumerate(content):
        if line.startswith("end;"):
            content.insert(index, new_line)
            break
    return content


def write_lines_to_file(file_path, content):
    with open(file_path, 'w') as file:
        file.writelines(content)


def create_new_vdv452_zip(zip_path):
    with zipfile.ZipFile('new_vdv452.zip', 'w') as zip_ref:
        for foldername, subfolders, filenames in os.walk('extracted_files'):
            for filename in filenames:
                file_path = os.path.join(foldername, filename)
                zip_ref.write(file_path, os.path.relpath(file_path, 'extracted_files'))


def create_gui():
    def on_add_new_vehicle_click():
        new_id = new_id_entry.get()

        try:
            new_id = int(new_id)
        except ValueError:
            tk.messagebox.showerror("Invalid ID", "Invalid ID format. Please enter an integer.")
            return

        add_new_vehicle(new_id)

    def on_update_rec_ort_click():
        update_rec_ort()

    def add_new_vehicle(new_id):
        zip_path = filedialog.askopenfilename(title="Select a VDV452 zip file",
                                              filetypes=(("zip files", "*.zip"), ("all files", "*.*")))

        if not zip_path:
            print("No file selected.")
            return

        extract_vdv452_zip(zip_path)
        content = readlines_from_file("extracted_files/menge_fzg_typ.x10")
        updated_content = add_new_line(content, new_id)
        write_lines_to_file("extracted_files/menge_fzg_typ.x10", updated_content)
        create_new_vdv452_zip(zip_path)
        tk.messagebox.showinfo("Success", "New vehicle type added successfully.")

    def update_rec_ort():
        zip_path = filedialog.askopenfilename(title="Select a VDV452 zip file",
                                              filetypes=(("zip files", "*.zip"), ("all files", "*.*")))

        if not zip_path:
            print("No file selected.")
            return

        extract_vdv452_zip(zip_path)

        rec_ort_content = readlines_from_file("extracted_files/rec_ort.x10")
        updated_rec_ort_content = update_coordinates(rec_ort_content)
        write_lines_to_file("extracted_files/rec_ort.x10", updated_rec_ort_content)

        create_new_vdv452_zip(zip_path)

        tk.messagebox.showinfo("Success", "rec_ort.x10 updated successfully.")

    root = tk.Tk()
    root.title("VDV452 Tool")

    new_id_label = ttk.Label(root, text="Enter the new ID:")
    new_id_label.pack(pady=(20, 0))

    new_id_entry = ttk.Entry(root)
    new_id_entry.pack(pady=(0, 20))

    add_new_vehicle_button = ttk.Button(root, text="Add New Vehicle Type", command=on_add_new_vehicle_click)
    add_new_vehicle_button.pack(pady=10)

    update_rec_ort_button = ttk.Button(root, text="Update rec_ort.x10", command=on_update_rec_ort_click)
    update_rec_ort_button.pack(pady=10)





    root.mainloop()


if __name__ == '__main__':
    create_gui()