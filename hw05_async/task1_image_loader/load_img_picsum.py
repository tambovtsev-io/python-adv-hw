import asyncio
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, ForwardRef, List

import aiofiles
import aiohttp
from colorama import Fore, init

init(autoreset=True)

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@dataclass
class PicsumImageDownloaderAwait:
    base_url: str = "https://picsum.photos"
    output_dir: Path = Path("./output")

    async def fetch_image_list(self, num_images: int) -> List[Dict]:
        image_list_url = f"{self.base_url}/v2/list?limit={num_images}"
        async with aiohttp.ClientSession() as session:
            async with session.get(image_list_url) as response:
                if response.status != 200:
                    raise Exception(f"Failed to fetch image list: {response.status}")
                out = await response.json()
                logger.info(Fore.YELLOW + "Fetched image list")
                return out

    async def download_and_write_images(self, num_images: int) -> None:
        self.output_dir.mkdir(parents=True, exist_ok=True)
        try:
            image_list = await self.fetch_image_list(num_images)
            async with aiohttp.ClientSession() as session:
                tasks = [
                    self.download_image(session, image_data)
                    for image_data in image_list
                ]
                await asyncio.gather(*tasks)
        except Exception as e:
            logger.error(f"Error during download process: {str(e)}")

    async def download_image(
        self,
        session: aiohttp.ClientSession,
        image_data: Dict,
    ) -> None:
        image_id = image_data["id"]
        download_url = image_data["download_url"]
        author = image_data["author"]
        output_path = self.output_dir / f"image_{image_id}_by_{author}.jpg"

        try:
            logger.info(Fore.YELLOW + f"Requesting image {image_id}")
            async with session.get(download_url) as response:
                logger.info(Fore.GREEN + f"Fetched image {image_id}")
                if response.status != 200:
                    logger.error(
                        Fore.RED
                        + f"Failed to download image {image_id}: {response.status}"
                    )
                    return
                async with aiofiles.open(output_path, "wb") as f:
                    await f.write(await response.read())
                logger.info(Fore.BLUE + f"Saved image {image_id}")
        except Exception as e:
            logger.error(Fore.RED + f"Error downloading image {image_id}: {str(e)}")


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--num_images", type=int, default=100)
    parser.add_argument("--output_dir", type=Path, default=Path("./output"))
    args = parser.parse_args()

    downloader = PicsumImageDownloaderAwait(output_dir=args.output_dir)

    try:
        asyncio.run(downloader.download_and_write_images(args.num_images))
        logger.info(f"Downloaded {args.num_images} images")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {str(e)}")


if __name__ == "__main__":
    main()
