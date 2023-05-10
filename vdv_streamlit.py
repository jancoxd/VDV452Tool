import streamlit as st
import os
import io
import pandas as pd
import openpyxl
from zipfile import ZipFile, ZIP_DEFLATED
from vdv452_functions import get_stop_coordinates, create_deadhead_catalog,  extract_vdv452_zip,readlines_from_file, update_zip, validate_files, update_coordinates, write_file, add_new_line, check_empty_coordinates, find_files_without_rec, find_additional_files_with_rec, switch_ort_names

st.title('VDV Tools v0.23b')

uploaded_file = st.file_uploader('Upload a VDV zip file:', type=['zip'])

if uploaded_file is not None:
    # Save the uploaded file to a temporary location
    temp_path = 'temp.zip'
    with open(temp_path, 'wb') as f:
        f.write(uploaded_file.getbuffer())

    # Let users select a function to perform
    function_options = ['Switch Columns', 'Add New Vehicle', 'Update Coordinates', 'Check VDV Files', 'Create Deadhead Catalog']
    selected_function = st.selectbox('Select a function to perform:', function_options)

    if selected_function == 'Add New Vehicle':
        new_id = st.text_input('Enter the new vehicle ID:', '')

    # Process the file with the selected function
    process_button = st.button('Process VDV zip file')
    if process_button:
        try:
            download = 1
            if selected_function == 'Switch Columns':
                new_zip_path = switch_ort_names(temp_path)
                print(new_zip_path)

            elif selected_function == 'Add New Vehicle':
                temp_dir = 'temp_folder'

                new_zip_path = update_zip(temp_path, new_id, 1)
                print(new_zip_path)

            elif selected_function == 'Check VDV Files':
                temp_dir = 'temp_folder'

                check1 = update_zip(temp_path, 0, 4)
                check2 = update_zip(temp_path, 0, 5)
                check3 = update_zip(temp_path, 0, 6)
                check4 = update_zip(temp_path, 0, 7)
                check5 = update_zip(temp_path, 0, 3)
                st.success("Empty Files found: ", check1)
                st.success("Additional Files found: ",check2)
                st.success(check3)
                st.success(check4)
                st.success(check5)
                new_zip_path = temp_path
                download = 0

            elif selected_function == 'Check for additional Files':
                temp_dir = 'temp_folder'

                check = update_zip(temp_path, 0, 5)
                st.success(check)
                new_zip_path = temp_path
                download = 0

            elif selected_function == 'Validate Files':
                temp_dir = 'temp_folder'

                check = update_zip(temp_path, 0, 6)
                st.success(check)
                new_zip_path = temp_path
                download = 0

            elif selected_function == 'Check for Columns with 0s':
                temp_dir = 'temp_folder'

                check = update_zip(temp_path, 0, 7)
                st.success(check)
                new_zip_path = temp_path
                download = 0

            elif selected_function == 'Check for empy Coordinates':
                temp_dir = 'temp_folder'

                check = update_zip(temp_path, 0, 3)
                st.success(check)
                new_zip_path = temp_path
                download = 0
            elif selected_function == 'Update Coordinates':

                new_zip_path = update_zip(temp_path, 0, 2)
                print(new_zip_path)
                st.success(f'VDV452 zip file updated successfully: {new_zip_path}')
            elif selected_function == 'Create Deadhead Catalog':

                excel_data = create_deadhead_catalog(temp_path)
                st.success(f'Deadhead Catalog finished:')
                st.download_button(
                    label='Download Deadhead Catalog',
                    data=excel_data,
                    file_name='deadhead.xlsx',
                    mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                )
                new_zip_path = temp_path
            # Offer the processed file for download
            with open(new_zip_path, 'rb') as f:
                if download == 1:
                    st.download_button(
                        label='Download the updated VDV zip file',
                        data=f,
                        file_name='vdv_updated.zip',
                        mime='application/zip'
                    )


            # Remove the temporary files
            os.remove(new_zip_path)
        except Exception as e:
            st.error(f'Error processing the VDV zip file: {str(e)}')