import asyncio
import argparse
import shutil
import logging
from pathlib import Path
from aiopath import AsyncPath

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


async def read_folder(source_path: AsyncPath, output_path: AsyncPath):
    def sync_rglob():
        return list(Path(source_path).rglob("*"))

    paths = await asyncio.to_thread(sync_rglob)

    for path in paths:
        async_file = AsyncPath(path)
        if await async_file.is_file():
            asyncio.create_task(copy_file(async_file, output_path))


async def copy_file(file_path: AsyncPath, output_path: AsyncPath):
    try:
        ext = file_path.suffix[1:] or 'unknown'
        target_dir = output_path / ext
        if not await target_dir.exists():
            await target_dir.mkdir(parents=True, exist_ok=True)

        target_file_path = target_dir / file_path.name

        await asyncio.to_thread(shutil.copy2, file_path, target_file_path)

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
    source_path = AsyncPath(args.source_folder)
    output_path = AsyncPath(args.output_folder)

    if not await source_path.exists() or not await source_path.is_dir():
        logging.error(
            f"The folder '{source_path}' does not exist or is not a directory")
        return

    if not await output_path.exists():
        await output_path.mkdir(parents=True, exist_ok=True)

    logging.info(
        f"Start sorting files from '{source_path}' to '{output_path}' ...")
    await read_folder(source_path, output_path)
    logging.info(f"Sorting is complete!")


if __name__ == "__main__":
    asyncio.run(main())
