import os
import asyncio
import shutil
from pathlib import Path
import argparse
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


async def read_folder(source_path: Path, output_path: Path):
    tasks = []
    for root, _, files in os.walk(source_path):
        for file in files:
            file_path = Path(root) / file
            tasks.append(copy_file(file_path, output_path))
    await asyncio.gather(*tasks)


async def copy_file(file_path: Path, output_path: Path):
    try:
        ext = file_path.suffix[1:] or 'unknown'
        target_dir = output_path / ext
        target_dir.mkdir(parents=True, exist_ok=True)
        target_file_path = target_dir / file_path.name

        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, shutil.copy2, file_path, target_file_path)

        logging.info(f"Copied: {file_path.name} -> {target_dir}/")
    except Exception as e:
        logging.error(f"Copy error: {file_path}: {e}")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Asynchronous sorting of files by extension.")
    parser.add_argument('--source_folder', default=r'.\task_1\source_folder',
                        help="Path to the source folder")
    parser.add_argument('--output_folder', default=r'.\task_1\output_folder',
                        help="Path to the output folder")
    return parser.parse_args()


async def main():
    args = parse_args()
    sourse_path = Path(args.source_folder)
    output_path = Path(args.output_folder)

    if not sourse_path.exists() or not sourse_path.is_dir():
        logging.error(
            f"The folder '{sourse_path}' does not exist or is not a directory")
        return

    output_path.mkdir(parents=True, exist_ok=True)
    logging.info(
        f"Start sorting files from '{sourse_path}' to '{output_path}' ...")
    await read_folder(sourse_path, output_path)
    logging.info(f"Sorting is complete!")

if __name__ == "__main__":
    asyncio.run(main())
