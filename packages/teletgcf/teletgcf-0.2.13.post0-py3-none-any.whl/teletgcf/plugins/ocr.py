import pytesseract
from PIL import Image

from teletgcf.plugins import TeletgcfMessage, TeletgcfPlugin
from teletgcf.utils import cleanup


class TeletgcfOcr(TeletgcfPlugin):
    id_ = "ocr"

    def __init__(self, data) -> None:
        pass

    async def modify(self, tm: TeletgcfMessage) -> TeletgcfMessage:

        if not tm.file_type in ["photo"]:
            return tm

        file = await tm.get_file()
        tm.text = pytesseract.image_to_string(Image.open(file))
        cleanup(file)
        return tm
