import streamlit as st
import os
from zipfile import ZipFile, ZIP_DEFLATED
from vdv452_functions import get_stop_coordinates_from_zip, create_deadhead_catalog,  extract_vdv452_zip,readlines_from_file, update_zip, validate_files, update_coordinates, write_file, add_new_line, check_empty_coordinates, find_files_without_rec, find_additional_files_with_rec, switch_ort_names

st.title('VDV Tools v0.23b')

uploaded_file = st.file_uploader('Upload a VDV zip file:', type=['zip'])

if uploaded_file is not None:
    # Save the uploaded file to a temporary location
    temp_path = 'temp.zip'
    with open(temp_path, 'wb') as f:
        f.write(uploaded_file.getbuffer())

    # Let users select a function to perform
    function_options = ['Switch Columns', 'Add New Vehicle', 'Update Coordinates', 'Check for empy Coordinates', 'Check for empty Files', 'Check for additional Files', 'Validate Files', 'Check for Columns with 0s', 'Create Deadhead Catalog']
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

            elif selected_function == 'Check for empty Files':
                temp_dir = 'temp_folder'

                check = update_zip(temp_path, 0, 4)
                st.success(check)
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

                new_zip_path = get_stop_coordinates_from_zip(temp_path)
                print(new_zip_path)
                st.success(f'VDV452 zip file updated successfully: {str(new_zip_path)}')

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