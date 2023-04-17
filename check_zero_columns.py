import zipfile

def check_zero_columns(zip_path, files_to_check):
    zero_columns = {}

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        for file_name in files_to_check:
            if file_name not in zip_ref.namelist():
                continue

            with zip_ref.open(file_name) as file:
                file_content = file.read().decode('iso-8859-1')
                lines = file_content.splitlines()

                columns = None
                column_values = {}

                for line in lines:
                    if line.startswith("atr;"):
                        columns = [col.strip() for col in line.split(";")[1:]]
                        for column in columns:
                            column_values[column] = []

                    if line.startswith("rec;"):
                        values = line.split(";")[1:]
                        for column, value in zip(columns, values):
                            column_values[column].append(value)

                if columns is None:
                    continue

                for column, values in column_values.items():
                    if all(value == '0' or value == '' for value in values):
                        if file_name not in zero_columns:
                            zero_columns[file_name] = []
                        zero_columns[file_name].append(column)

    result = "Columns containing only zeros:\n"
    for file_name, columns in zero_columns.items():
        result += f"{file_name}: {', '.join(columns)}\n"

    return result.strip()
