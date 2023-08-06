import logging
import os
import shutil
from typing import Any, Dict

import requests
from pydantic import BaseModel  # pylint: disable=no-name-in-module
from watermark import File, Position, Watermark, apply_watermark

from teletgcf.plugins import TeletgcfMessage, TeletgcfPlugin
from teletgcf.utils import cleanup


class MarkConfig(BaseModel):
    image: str = "image.png"
    position: Position = Position.centre
    frame_rate: int = 15


def download_image(url: str, filename: str = "image.png") -> bool:
    if filename in os.listdir():
        logging.info("Image for watermarking already exists.")
        return True
    try:
        logging.info(f"Downloading image {url}")
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            logging.info("Got Response 200")
            with open(filename, "wb") as file:
                response.raw.decode_content = True
                shutil.copyfileobj(response.raw, file)
    except Exception as err:
        logging.error(err)
        return False
    else:
        logging.info("File created image")
        return True


class TeletgcfMark(TeletgcfPlugin):
    id_ = "mark"

    def __init__(self, data: Dict[str, Any]) -> None:
        self.data = MarkConfig(**data)

    async def modify(self, tm: TeletgcfMessage) -> TeletgcfMessage:
        if not tm.file_type in ["gif", "video", "photo"]:
            return tm
        downloaded_file = await tm.get_file()
        base = File(downloaded_file)
        if self.data.image.startswith("https://"):
            download_image(self.data.image)
            overlay = File("image.png")
        else:
            overlay = File(self.data.image)
        wtm = Watermark(overlay, self.data.position)
        tm.new_file = apply_watermark(base, wtm, frame_rate=self.data.frame_rate)
        cleanup(downloaded_file)
        tm.cleanup = True
        return tm
