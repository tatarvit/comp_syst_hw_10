import random
import string
import shutil
from pathlib import Path

FILE_TYPES = ['docx', 'xlsx', 'pdf', 'txt', 'csv']
SOURCE_FOLDER = Path('D:/GoIT/computer_systema/hw_10/task_1/source_folder')
NUM_FILES = 50
NUM_SUBFOLDERS = 5


def create_random_content():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=100))


def clear_folder(folder: Path):
    if folder.exists():
        shutil.rmtree(folder)


def create_files():

    # Clean and create the original folder
    clear_folder(SOURCE_FOLDER)
    SOURCE_FOLDER.mkdir(parents=True, exist_ok=True)

    # Create folders
    subfolders = []
    for i in range(1, NUM_SUBFOLDERS + 1):
        subfolder = SOURCE_FOLDER / f'subfolder_{i}'
        subfolder.mkdir(parents=True, exist_ok=True)
        subfolders.append(subfolder)

    # Create files and move them in random folders
    for i in range(NUM_FILES):
        ext = random.choice(FILE_TYPES)
        subfolder = random.choice(subfolders)
        filename = f'file_{i + 1}.{ext}'
        file_path = subfolder / filename
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(create_random_content())
    print(f"{NUM_FILES} files created in '{SOURCE_FOLDER.resolve()}'")


if __name__ == "__main__":
    create_files()
