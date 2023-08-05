import os
import SimpleITK as sitk

from typing import List, Tuple
from raymics.constants import IMAGE_EXTS, VIDEO_EXTS


def is_hidden(file_path: str) -> bool:
    components = os.path.normpath(file_path).split(os.sep)
    for c in components:
        if c.startswith("."):
            return True
    return False


def is_cacahed(file_path: str) -> bool:
    components = os.path.normpath(file_path).split(os.sep)
    for c in components:
        if c and c.startswith("__"):  # __pycache__, __pypackages__, __MACOSX
            return True
    return False


def get_all_files(root_dir: str) -> List[str]:
    files = []
    for name in os.listdir(root_dir):
        abs_path = os.path.join(root_dir, name)
        if is_hidden(abs_path) or is_cacahed(abs_path):
            continue
        if os.path.isdir(abs_path):
            files += get_all_files(abs_path)
        else:
            files.append(abs_path)
    return files


def is_video(path: str) -> bool:
    ext = os.path.splitext(path)[1].replace(".", "")
    if not ext:
        return False
    else:
        return ext.lower() in VIDEO_EXTS


def is_image(path: str) -> bool:
    ext = os.path.splitext(path)[1].replace(".", "")
    if not ext:
        return False
    else:
        return ext.lower() in IMAGE_EXTS


def is_ndarray(path: str) -> bool:
    ext = os.path.splitext(path)[1].replace(".", "")
    if not ext:
        return False
    else:
        return ext.lower() == "npy"


def is_labelme(path: str) -> bool:
    ext = os.path.splitext(path)[1].replace(".", "")
    if not ext:
        return False
    else:
        return ext.lower() == "json"


def get_sitk_shape(image: sitk.Image) -> Tuple[int, int, int]:
    """Get the shape of SimpleITK image shape"""
    return image.GetWidth(), image.GetHeight(), image.GetDepth()
