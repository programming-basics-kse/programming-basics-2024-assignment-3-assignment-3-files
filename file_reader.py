
def read_file(filename:str, access: str) -> list:
    file_data = []
    with open(filename, access) as file:
        lines = file.read().splitlines()
        first_line = lines[0].split("\t")
        for line in lines[1::]:
            fields = line.split("\t")
            entry = {
                first_line[i]: int(component) if component.isdigit() else component
                for i, component in enumerate(fields)
            }
            file_data.append(entry)
    return file_data