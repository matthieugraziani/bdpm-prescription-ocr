from typing import Optional

import cv2
import easyocr

_READER: Optional[easyocr.Reader] = None


def get_reader(lang_list: Optional[list] = None, gpu: bool = False):

    # Avoid the `global` statement by updating the module-level name
    # through the globals() mapping. This keeps the lazy-initialisation
    # semantics without rebinding a local name.
    if _READER is None:
        globals()['_READER'] = easyocr.Reader(lang_list or ["fr"], gpu=gpu)
    return globals()['_READER']


def preprocess(image):

    if image.ndim == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)  # type: ignore[attr-defined]  # pylint: disable=no-member
    else:
        gray = image

    denoised = cv2.fastNlMeansDenoising(gray, h=10)  # type: ignore[attr-defined]  # pylint: disable=no-member

    return cv2.adaptiveThreshold(  # type: ignore[attr-defined]  # pylint: disable=no-member
        denoised,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,  # type: ignore[attr-defined]  # pylint: disable=no-member
        0,
        31,
        11,
    )


def extract(image, preprocess_image=True, gpu=False):

    if preprocess_image:
        image = preprocess(image)

    reader = get_reader(gpu=gpu)
    return "\n".join(str(line) for line in reader.readtext(image, detail=0))