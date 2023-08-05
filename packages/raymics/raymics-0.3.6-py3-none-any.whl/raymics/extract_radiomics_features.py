import os
import sys
import re
import math
import json
import argparse
import logging
import tqdm
import skvideo.io
import numpy as np
import pandas as pd
import cv2
import radiomics
import SimpleITK as sitk
import PIL
import PIL.Image
import PIL.ImageDraw

from typing import List, Union, Tuple
from multiprocessing import Manager, Pool
from collections import OrderedDict
from radiomics.featureextractor import RadiomicsFeatureExtractor
from raymics import DatasetType
from raymics.constants import COL_LABEL, RADIOMIC_FEATURE_FILENAME
from raymics.dataset import Dataset, LabeledDataset
from raymics.utils import is_image, is_video, is_ndarray, is_labelme


logging.basicConfig(format="%(asctime)s - %(levelname)s: %(message)s",
                    stream=sys.stdout, level=logging.ERROR)
radiomics.logger.setLevel(logging.CRITICAL)


def dummy_mask(shape: Tuple[int, int]) -> sitk.Image:
    mask = np.ones(shape=shape)
    mask[0, 0] = 0
    mask = sitk.GetImageFromArray(mask)
    return mask


def cv_img2sitk_image(path: str) -> sitk.Image:
    img = cv2.imread(path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = sitk.GetImageFromArray(img)
    return img


def ndarray2sitk_image(path: str) -> sitk.Image:
    """ndarray of gray image or opencv image"""
    img = np.load(path)
    assert len(img.shape) in [2, 3], f"Not 2D data: {path}"
    if len(img.shape) == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = sitk.GetImageFromArray(img)
    return img


def shape_to_mask(img_shape: Tuple[int, int], points: List[Tuple[float, float]],
                  shape_type: str = None, line_width: int = 10,
                  point_size: int = 5) -> np.ndarray:

    mask = np.zeros(img_shape[:2], dtype=np.uint8)
    mask = PIL.Image.fromarray(mask)
    draw = PIL.ImageDraw.Draw(mask)
    xy = [tuple(point) for point in points]

    if shape_type == "circle":
        assert len(xy) == 2, "Shape of shape_type=circle must have 2 points"
        (cx, cy), (px, py) = xy
        d = math.sqrt((cx - px) ** 2 + (cy - py) ** 2)
        draw.ellipse([cx - d, cy - d, cx + d, cy + d], outline=1, fill=1)

    elif shape_type == "rectangle":
        assert len(xy) == 2, "Shape of shape_type=rectangle must have 2 points"
        draw.rectangle(xy, outline=1, fill=1)

    elif shape_type == "line":
        assert len(xy) == 2, "Shape of shape_type=line must have 2 points"
        draw.line(xy=xy, fill=1, width=line_width)

    elif shape_type == "linestrip":
        draw.line(xy=xy, fill=1, width=line_width)

    elif shape_type == "point":
        assert len(xy) == 1, "Shape of shape_type=point must have 1 points"
        cx, cy = xy[0]
        r = point_size
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=1, fill=1)

    else:
        assert len(xy) > 2, "Polygon must have points more than 2"
        draw.polygon(xy=xy, outline=1, fill=1)

    mask = np.array(mask)

    return mask


def labelme_json2mask(path) -> sitk.Image:
    with open(path) as f:
        json_data = json.load(f)

    points = json_data["shapes"][0]["points"]
    shape = json_data["shapes"][0]["shape_type"]
    h, w = json_data["imageHeight"], json_data["imageWidth"]
    mask = shape_to_mask(img_shape=(h, w), points=points, shape_type=shape)
    mask = sitk.GetImageFromArray(mask)
    return mask


def get_mask(mask_path: Union[str, None], shape: Tuple[int, int]) -> sitk.Image:
    # no mask
    if mask_path is None:
        mask = dummy_mask(shape=shape)

    # numpy.ndarray
    elif is_ndarray(mask_path):
        mask = ndarray2sitk_image(mask_path)

    # opencv image
    elif is_image(mask_path):
        mask = cv_img2sitk_image(mask_path)

    # labelme json
    elif is_labelme(mask_path):
        mask = labelme_json2mask(mask_path)

    # try to read mask using SimpleITK - raise error if wrong file is supplied
    else:
        mask = sitk.ReadImage(mask_path)

    return mask


def check_data(paths: Union[str, List[str]]) -> int:
    """

    Parameters
    ----------
    paths : List of data paths

    Returns
    -------
    0 : 2D or 3D, not time series
    1 : Video, time series
    2 : Error, mix includes 0, 1

    """
    # video_paths = [p for p in paths if len(FFProbe(p).video)]
    if isinstance(paths, str):
        paths = [paths]

    video_paths = [p for p in paths if is_video(p)]
    if video_paths:
        if len(video_paths) == len(paths):
            return DatasetType.TS
        else:
            raise Exception("It is supposed only time series data or"
                            " non-time series data in the paths.")
    else:
        return DatasetType.NON_TS


def convert_to_rel_paths(paths: List[str], root_dir: str) -> List[str]:
    # todo
    return paths


def rename_duplicate_path(path: str) -> str:
    p, ext = os.path.splitext(path)
    if re.match(".+_\d", os.path.basename(p)):
        splits = p.split("_")
        seq = int(splits[-1])
        new_path = "_".join(splits[:-1]) + f"_{seq + 1}" + ext
    else:
        new_path = p + "_1" + ext

    return rename_duplicate_path(new_path) \
        if os.path.exists(new_path) else new_path


def read_mask(mask_path: str) -> sitk.Image:
    """
    Parameters
    ----------
    mask_path : str
        Path of the mask file.

    """
    ext = os.path.splitext(mask_path)[-1].lower()
    ext = ext[1:] if ext.startswith(".") else ext
    if is_image(mask_path):
        mask = cv2.imread(mask_path)
        mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
        mask = sitk.GetImageFromArray(mask)
    elif ext == "npy":
        mask = np.load(mask_path)
        mask = sitk.GetImageFromArray(mask)
    else:
        raise ValueError(f"Mask with extension '{ext}' is not supported!")

    return mask


def execute(extractor, data, mask, label=None) -> OrderedDict:
    feature_data = extractor.execute(data, mask)
    if label is not None:
        feature_data[COL_LABEL] = label
    return feature_data


def extract_non_ts(data_paths: List[str], mask_paths: List[str],
                   labels: List[Union[int, float, int, None]],
                   result_path: str, extractor: RadiomicsFeatureExtractor, lock):

    def read_non_ts(data_path, mask_path, label):
        # opencv image
        if is_image(data_path):
            img = cv_img2sitk_image(data_path)
        # numpy ndarray
        elif is_ndarray(data_path):
            img = np.load(data_path)
        # try to read image using SimpleITK
        else:
            img = sitk.ReadImage(data_path)
        mask = get_mask(mask_path=mask_path,
                        shape=(img.GetHeight(), img.GetWidth()))

        return img, mask, label

    feature_list: List[OrderedDict] = [
        execute(extractor, *read_non_ts(data, mask, label))
        for data, mask, label in zip(data_paths, mask_paths, labels)
    ]
    feature_df = pd.DataFrame(feature_list)

    with lock:
        if not os.path.exists(result_path):
            feature_df.to_csv(result_path, index=False)
        else:
            feature_df.to_csv(result_path, index=False, mode="a", header=False)


def extract_ts(data_path: str, mask_path: str, label: Union[int, float, int, None],
               result_path: str, extractor: RadiomicsFeatureExtractor):

    def read_ts():
        mask = None
        for frame in skvideo.io.vreader(data_path):
            gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
            img = sitk.GetImageFromArray(gray)
            if mask is None:
                mask = get_mask(mask_path=mask_path,
                                shape=(img.GetHeight(), img.GetWidth()))

            yield img, mask, label
    try:
        feature_list: List[OrderedDict] = [execute(extractor, data, mask, label)
                                           for data, mask, label in read_ts()]
        feature_df = pd.DataFrame(feature_list)

        if os.path.exists(result_path):
            result_path = rename_duplicate_path(result_path)

        feature_df.to_csv(result_path, index=False)
    except Exception as e:
        logging.warning(f"\nRadiomics extracting error: {e}, "
                        f"\ndata_path: {data_path}, "
                        f"\nmask_path: {mask_path}")


def extract(data_dir: str, result_dir: str, config_path: str,
            processes: int = 2, cloud_run: bool = False,
            progress = None) -> RadiomicsFeatureExtractor:
    """

    Parameters
    ----------
    data_dir : str
        Directory of the raw dataset.

    result_dir : str
        提取到的radiomics特征文件存放文件夹

    config_path : str
        radiomics配置文件路径

    processes : int
        提取radiomics的进程数量

    cloud_run : bool, default=False
        云端执行

    """
    assert os.path.exists(config_path), f"Config yaml file not found."

    dataset = LabeledDataset(root_dir=data_dir)

    if not os.path.exists(result_dir):
        os.makedirs(result_dir)

    if not os.path.exists(result_dir):
        os.makedirs(result_dir)

    pool = Pool(processes=processes)
    extractor = RadiomicsFeatureExtractor(config_path)

    data_type = DatasetType.TS if is_video(dataset[0][0]) else DatasetType.NON_TS

    # non-time series
    if data_type == DatasetType.NON_TS:
        result_path = os.path.join(result_dir, RADIOMIC_FEATURE_FILENAME)
        assert not os.path.exists(result_path), \
            f"The result_path is not supposed to exist: {result_path}"

        group_len = 1000
        idxs = list(range(len(dataset)))
        group_idxs = [idxs[i: i + group_len] for i in range(0, len(idxs), group_len)]

        lock = Manager().Lock()

        bar = tqdm.tqdm(total=len(group_idxs))
        if progress is None:
            callback = lambda _: bar.update()
        else:
            progress.set_tqdm(bar=bar)
            callback = progress.update

        for idx_list in group_idxs:
            pool.apply_async(
                func=extract_non_ts,
                args=([dataset.data_paths[_] for _ in idx_list],
                      [dataset.mask_paths[_] for _ in idx_list],
                      [dataset.labels[_] for _ in idx_list],
                      result_path,
                      extractor,
                      lock),
                callback=callback
            )

    # time series
    else:    # data_type == 1
        result_paths = [
            os.path.join(result_dir,
                         os.path.splitext(os.path.basename(path))[0] + ".csv")
            for path in dataset.data_paths]

        bar = tqdm.tqdm(total=len(dataset))
        if progress is None:
            callback = lambda _: bar.update()
        else:
            progress.set_tqdm(bar=bar)
            callback = progress.update

        for i, (data_path, mask_path, label) in enumerate(dataset):
            result_path = result_paths[i]
            # extract_ts(data_path, mask_path, label, result_path, extractor)
            pool.apply_async(
                func=extract_ts,
                args=(data_path, mask_path, label, result_path, extractor),
                callback=callback
            )

    pool.close()
    pool.join()

    return extractor


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--data_dir",
        type=str,
        help="raw data dir"
    )
    parser.add_argument(
        "--result_dir",
        type=str,
        help="Directory to save the features result."
    )
    parser.add_argument(
        "--config_path",
        type=str,
        help="yaml file path."
    )
    parser.add_argument(
        "--cloud_run",
        action='store_true',
        help="Whether run in cloud."
    )
    parser.add_argument(
        "--processes",
        type=int,
        help="multiprocessing pool max size."
    )

    args = parser.parse_args()

    extract(data_dir=args.data_dir,
            config_path=args.config_path,
            result_dir=args.result_dir,
            cloud_run=args.cloud_run,
            processes=args.processes)
