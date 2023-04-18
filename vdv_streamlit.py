import streamlit as st
import os
from zipfile import ZipFile, ZIP_DEFLATED
from vdv452_functions import extract_vdv452_zip,readlines_from_file, update_zip, validate_files, update_coordinates, write_file, add_new_line, check_empty_coordinates, find_files_without_rec, find_additional_files_with_rec, switch_ort_names

st.title('VDV452 Modifier v0.22')

uploaded_file = st.file_uploader('Upload a VDV zip file:', type=['zip'])

if uploaded_file is not None:
    # Save the uploaded file to a temporary location
    temp_path = 'temp.zip'
    with open(temp_path, 'wb') as f:
        f.write(uploaded_file.getbuffer())

    # Let users select a function to perform
    function_options = ['Switch Columns', 'Add New Vehicle', 'Update Coordinates']
    selected_function = st.selectbox('Select a function to perform:', function_options)

    if selected_function == 'Add New Vehicle':
        new_id = st.text_input('Enter the new vehicle ID:', '')

    # Process the file with the selected function
    process_button = st.button('Process VDV zip file')
    if process_button:
        try:
            if selected_function == 'Switch Columns':
                new_zip_path = switch_ort_names(temp_path)
                print(new_zip_path)

            elif selected_function == 'Add New Vehicle':
                temp_dir = 'temp_folder'

                # Extract zip file contents to a temporary folder
                with ZipFile(temp_path, 'r') as zip_ref:
                    zip_ref.extractall(temp_dir)
                menge_fzg_typ_path = os.path.join(temp_dir, 'menge_fzg_typ.x10')
                content = readlines_from_file(menge_fzg_typ_path)
                updated_content = add_new_line(content, new_id)

                new_zip_path = write_file(menge_fzg_typ_path, updated_content)
                print(new_zip_path)

            elif selected_function == 'Update Coordinates':

                new_zip_path = update_zip(temp_path, 0, 2)
                print(new_zip_path)

            st.success('Successfully processed the VDV zip file.')

            # Offer the processed file for download
            with open(new_zip_path, 'rb') as f:
                st.download_button(
                    label='Download the updated VDV zip file',
                    data=f,
                    file_name='vdv_updated.zip',
                    mime='application/zip'
                )

            # Remove the temporary files
            os.remove(temp_path)
            os.remove(new_zip_path)
        except Exception as e:
            st.error(f'Error processing the VDV zip file: {str(e)}')