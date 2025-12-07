def read_file(file_path: str) -> str:
    # Read a file and return its content
    with open(file_path, "r") as file:
        return file.read()


def write_file(file_path: str, content: str) -> None:
    # Write content to a file
    with open(file_path, "w") as file:
        file.write(content)
