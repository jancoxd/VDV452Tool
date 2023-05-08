import zipfile
import os
import tempfile
import shutil
import tkinter as tk
from tkinter import filedialog
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


def read_menge_fzg_typ():
    with open('extracted_files/menge_fzg_typ.x10', 'r') as file:
        content = file.readlines()
    return content

def add_new_line(content, new_id):
    new_line = f"rec;1000;{new_id};0;0;0;\"New Bus {new_id}\";0;\"NB{new_id}\""
    for index, line in enumerate(content):
        if line.startswith("end;"):
            content.insert(index, new_line)
            break
    return content


def write_menge_fzg_typ(content):
    with open('extracted_files/menge_fzg_typ.x10', 'w') as file:
        file.writelines(content)

def create_new_vdv452_zip(zip_path):
    with zipfile.ZipFile('new_vdv452.zip', 'w') as zip_ref:
        for foldername, subfolders, filenames in os.walk('extracted_files'):
            for filename in filenames:
                file_path = os.path.join(foldername, filename)
                zip_ref.write(file_path, os.path.relpath(file_path, 'extracted_files'))

def main():
    root = tk.Tk()
    root.withdraw()

    zip_path = filedialog.askopenfilename(title="Select a VDV452 zip file",
                                          filetypes=(("zip files", "*.zip"), ("all files", "*.*")))

    if not zip_path:
        print("No file selected.")
        return

    new_id = input("Enter the new ID: ")

    try:
        new_id = int(new_id)
    except ValueError:
        print("Invalid ID format. Please enter an integer.")
        return

    extract_vdv452_zip(zip_path)
    content = read_menge_fzg_typ()
    # Read and update rec_ort.x10 file
    rec_ort_content = read_file("extracted_files/rec_ort.x10")
    updated_rec_ort_content = update_coordinates(rec_ort_content)
    write_file("extracted_files/rec_ort.x10", updated_rec_ort_content)

    updated_content = add_new_line(content, new_id)
    write_menge_fzg_typ(updated_content)
    create_new_vdv452_zip(zip_path)
    print("VDV452 zip file updated successfully.")

if __name__ == '__main__':
    main()
