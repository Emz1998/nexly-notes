from scripts import phase_validation, block_coding
from utils import read_stdin_json


def main() -> None:
    # """Main function to execute the pre-tool-use hook."""
    # print("Validating phase transition...")
    # phase_validation()
    # print("Phase transition validated.")
    block_coding(read_stdin_json())


if __name__ == "__main__":
    main()
