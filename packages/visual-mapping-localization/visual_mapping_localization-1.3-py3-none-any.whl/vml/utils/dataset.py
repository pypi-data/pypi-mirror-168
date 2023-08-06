from typing import Tuple
import torch
from pathlib import Path
from types import SimpleNamespace
import cv2
import numpy as np
import collections.abc as collections
import PIL.Image
from typing import Dict, List, Union, Optional


from .parsers import parse_image_lists
from .io import read_image
from ..import logger


def resize_image(image:cv2.Mat, size:Tuple[int,int], interp:str) -> cv2.Mat:
    """
    @Description :图片缩放
        image: 图片数据
        size: 缩放后的尺寸
        interp: 插值类型
    
    @Returns     :缩放后的图片
    """
    if interp.startswith('cv2_'):
        interp = getattr(cv2, 'INTER_'+interp[len('cv2_'):].upper())
        h, w = image.shape[:2]
        if interp == cv2.INTER_AREA and (w < size[0] or h < size[1]):
            interp = cv2.INTER_LINEAR
        resized = cv2.resize(image, size, interpolation=interp)
    elif interp.startswith('pil_'):
        interp = getattr(PIL.Image, interp[len('pil_'):].upper())
        resized = PIL.Image.fromarray(image.astype(np.uint8))
        resized = resized.resize(size, resample=interp)
        resized = np.asarray(resized, dtype=image.dtype)
    else:
        raise ValueError(
            f'Unknown interpolation {interp}.')
    return resized

def preprocess_image(image:cv2.Mat, name: str, conf:Dict) -> Dict:
    """
    @Description :图像数据预处理封装
        image: 图像数据
        name: 图像名称（数据库中的名称）
        conf: 预处理配置    {
                                'grayscale': False,
                                'resize_max': None,
                                'resize_force': False,
                                'interpolation': 'cv2_area'
                            }
    
    @Returns     : 封装处理后的数据
        {
            'name': 类型:List 图像名称
            'image': 类型: torch.Tensor 图像数据
            'original_size': 类型: torch.Tensor 原始图像尺寸
        }
    """
    if image.ndim > 2 and conf.grayscale:
        cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)
    image = image.astype(np.float32)
    size = image.shape[:2][::-1]
    if conf.resize_max and (conf.resize_force or max(size) > conf.resize_max):
        scale = conf.resize_max / max(size)
        size_new = tuple(int(round(x*scale)) for x in size)
        image = resize_image(image, size_new, conf.interpolation)
    if conf.grayscale:
        image = image[None]
    else:
        image = image.transpose((2, 0, 1))  # HxWxC to CxHxW
    image = image / 255.
    data = {
        'name': [name],
        'image': torch.from_numpy(image).unsqueeze(0),
        'original_size': torch.from_numpy(np.array(size)).unsqueeze(0),
    }
    return data


class ImageDataset(torch.utils.data.Dataset):
    default_conf = {
        'globs': ['*.jpg', '*.png', '*.jpeg', '*.JPG', '*.PNG'],
        'grayscale': False,
        'resize_max': None,
        'resize_force': False,
        'interpolation': 'cv2_area',  # pil_linear is more accurate but slower
    }

    def __init__(self, root: Path, conf: Dict, paths: Optional[Union[Path, str, List[str]]]=None):
        """
        Args:
            root : str
                图片根目录
            conf : Dict
                数据配置
            paths : Path 或 str 或 List[str]
                Path 或 str 时为存储图片列表文件的路径（txt格式，文件中的路径以root路径为起始路径）
                List[str] 时为图片路径列表，以root路径为起始路径
        """
        self.conf = conf = SimpleNamespace(**{**self.default_conf, **conf})
        self.root = root

        if paths is None:
            paths = []
            for g in conf.globs:
                paths += list(Path(root).glob('**/'+g))
            if len(paths) == 0:
                raise ValueError(f'Could not find any image in root: {root}.')
            paths = sorted(list(set(paths)))
            self.names = [i.relative_to(root).as_posix() for i in paths]
            logger.info(f'Found {len(self.names)} images in root {root}.')
        else:
            if isinstance(paths, (Path, str)):
                self.names = parse_image_lists(Path(paths))
            elif isinstance(paths, collections.Iterable):
                self.names = [p.as_posix() if isinstance(p, Path) else p
                              for p in paths]
            else:
                raise ValueError(f'Unknown format for path argument {paths}.')
            for name in self.names:
                if not (root / name).exists():
                    raise ValueError(
                        f'Image {name} does not exists in root: {root}.')
        
    def __getitem__(self, idx):
        name = self.names[idx]
        image = read_image(self.root / name, self.conf.grayscale)
        image = image.astype(np.float32)
        size = image.shape[:2][::-1]

        if self.conf.resize_max and (self.conf.resize_force
                                     or max(size) > self.conf.resize_max):
            scale = self.conf.resize_max / max(size)
            size_new = tuple(int(round(x*scale)) for x in size)
            image = resize_image(image, size_new, self.conf.interpolation)

        if self.conf.grayscale:
            image = image[None]
        else:
            image = image.transpose((2, 0, 1))  # HxWxC to CxHxW
        image = image / 255.

        data = {
            'name': name,
            'image': image,
            'original_size': np.array(size),
        }
        return data

    def __len__(self):
        return len(self.names)
