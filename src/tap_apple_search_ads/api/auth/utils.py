def read_private_key_from_file(private_key_path) -> str:
    with open(private_key_path, "r") as key_file:
        private_key = "".join(key_file.readlines()).strip()

    return private_key
