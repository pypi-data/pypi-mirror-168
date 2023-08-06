import argparse
import torch
from pathlib import Path
from typing import Dict, List, Union, Optional
import h5py
from types import SimpleNamespace
import cv2
import numpy as np
from tqdm import tqdm
import pprint

from . import extractors, logger
from .utils.base_model import dynamic_load
from .utils.dataset import ImageDataset, preprocess_image
from .utils.tools import map_tensor
from .utils.io import read_image, list_h5_names


'''
A set of standard configurations that can be directly selected from the command
line using their name. Each is a dictionary with the following entries:
    - output: the name of the feature file that will be generated.
    - model: the model configuration, as passed to a feature extractor.
    - preprocessing: how to preprocess the images read from disk.
'''
confs = {
    'superpoint_outdoor': {
        'output': 'feats-superpoint-n4096-r1024',
        'model': {
            'name': 'superpoint',
            'nms_radius': 3,
            'max_keypoints': 4096,
        },
        'preprocessing': {
            'grayscale': True,
            'resize_max': 1024,
        },
    },
    'superpoint_indoor': {
        'output': 'feats-superpoint-n4096-r1600',
        'model': {
            'name': 'superpoint',
            'nms_radius': 4,
            'max_keypoints': 4096,
        },
        'preprocessing': {
            'grayscale': True,
            'resize_max': 1600,
        },
    },
    # Global descriptors
    'netvlad': {
        'output': 'global-feats-netvlad',
        'model': {'name': 'netvlad'},
        'preprocessing': {'resize_max': 1024},
    }
}


class ExtractFeatures():
    preprocessing_conf = {
        'grayscale': False,
        'resize_max': None,
        'resize_force': False,
        'interpolation': 'cv2_area',  # pil_linear is more accurate but slower
    }
    def __init__(self, conf: Dict, feature_path: Path):
        self.conf = conf
        self.preprocessing = SimpleNamespace(**{**self.preprocessing_conf, **conf['preprocessing']})

        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        Model = dynamic_load(extractors, conf['model']['name'])
        self.model = Model(conf['model']).eval().to(self.device)

        feature_path.parent.mkdir(exist_ok=True, parents=True)
        self.feature_path = feature_path
        
        logger.info('Extracting local features with configuration:'
                f'\n{pprint.pformat(conf)}')

    def get_data_from_file(self, root: Path, name: str) -> Dict:
        image = read_image(root / name, self.preprocessing.grayscale)
        data = preprocess_image(image, name, self.preprocessing)
        return data

    def get_data_from_image(self, image: cv2.Mat, name: str):
        data = preprocess_image(image, name, self.preprocessing)
        return data

    @torch.no_grad()
    def extract_features_for_image(self, data: Dict, as_half: bool = True) -> Path:
        name = data['name'][0]  # remove batch dimension
        pred = self.model(map_tensor(data, lambda x: x.to(self.device)))
        pred = {k: v[0].cpu().numpy() for k, v in pred.items()}

        pred['image_size'] = original_size = data['original_size'][0].numpy()
        if 'keypoints' in pred:
            size = np.array(data['image'].shape[-2:][::-1])
            scales = (original_size / size).astype(np.float32)
            pred['keypoints'] = (pred['keypoints'] + .5) * scales[None] - .5
            # add keypoint uncertainties scaled to the original resolution
            uncertainty = getattr(self.model, 'detection_noise', 1) * scales.mean()
        if as_half:
            for k in pred:
                dt = pred[k].dtype
                if (dt == np.float32) and (dt != np.float16):
                    pred[k] = pred[k].astype(np.float16)
        with h5py.File(str(self.feature_path), 'a') as fd:
            try:
                if name in fd:
                    del fd[name]
                grp = fd.create_group(name)
                for k, v in pred.items():
                    grp.create_dataset(k, data=v)
                if 'keypoints' in pred:
                    grp['keypoints'].attrs['uncertainty'] = uncertainty
            except OSError as error:
                if 'No space left on device' in error.args[0]:
                    logger.error(
                        'Out of disk space: storing features on disk can take '
                        'significant space, did you enable the as_half flag?')
                    del grp, fd[name]
                raise error
        del pred
        # logger.info('Extract features.')
        return self.feature_path

    def extract_features_for_dir(self, image_dir: Path, as_half: bool = True, image_list: Optional[Union[Path, List[str]]] = None, overwrite: bool = False) -> Path:
        loader = ImageDataset(image_dir, self.conf['preprocessing'], image_list)
        loader = torch.utils.data.DataLoader(loader, num_workers=1)
        skip_names = set(list_h5_names(self.feature_path) if self.feature_path.exists() and not overwrite else ())
        if set(loader.dataset.names).issubset(set(skip_names)):
            logger.info('Skipping the extraction.')
            return self.feature_path
        for data in tqdm(loader):
            if data['name'][0] in skip_names:
                continue
            self.extract_features_for_image(data, as_half)
        logger.info('Finished exporting features.')
        return self.feature_path


@torch.no_grad()
def main(conf: Dict,
         image_dir: Path,
         export_dir: Optional[Path] = None,
         as_half: bool = True,
         image_list: Optional[Union[Path, List[str]]] = None,
         feature_path: Optional[Path] = None,
         overwrite: bool = False) -> Path:
    logger.info('Extracting local features with configuration:'
                f'\n{pprint.pformat(conf)}')

    loader = ImageDataset(image_dir, conf['preprocessing'], image_list)
    loader = torch.utils.data.DataLoader(loader, num_workers=1)

    if feature_path is None:
        feature_path = Path(export_dir, conf['output']+'.h5')
    feature_path.parent.mkdir(exist_ok=True, parents=True)
    skip_names = set(list_h5_names(feature_path)
                     if feature_path.exists() and not overwrite else ())
    if set(loader.dataset.names).issubset(set(skip_names)):
        logger.info('Skipping the extraction.')
        return feature_path

    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    Model = dynamic_load(extractors, conf['model']['name'])
    model = Model(conf['model']).eval().to(device)

    for data in tqdm(loader):
        name = data['name'][0]  # remove batch dimension
        if name in skip_names:
            continue

        pred = model(map_tensor(data, lambda x: x.to(device)))
        pred = {k: v[0].cpu().numpy() for k, v in pred.items()}

        pred['image_size'] = original_size = data['original_size'][0].numpy()
        if 'keypoints' in pred:
            size = np.array(data['image'].shape[-2:][::-1])
            scales = (original_size / size).astype(np.float32)
            pred['keypoints'] = (pred['keypoints'] + .5) * scales[None] - .5
            # add keypoint uncertainties scaled to the original resolution
            uncertainty = getattr(model, 'detection_noise', 1) * scales.mean()

        if as_half:
            for k in pred:
                dt = pred[k].dtype
                if (dt == np.float32) and (dt != np.float16):
                    pred[k] = pred[k].astype(np.float16)

        with h5py.File(str(feature_path), 'a', libver='latest') as fd:
            try:
                if name in fd:
                    del fd[name]
                grp = fd.create_group(name)
                for k, v in pred.items():
                    grp.create_dataset(k, data=v)
                if 'keypoints' in pred:
                    grp['keypoints'].attrs['uncertainty'] = uncertainty
            except OSError as error:
                if 'No space left on device' in error.args[0]:
                    logger.error(
                        'Out of disk space: storing features on disk can take '
                        'significant space, did you enable the as_half flag?')
                    del grp, fd[name]
                raise error

        del pred

    logger.info('Finished exporting features.')
    return feature_path


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--image_dir', type=Path, required=True)
    parser.add_argument('--export_dir', type=Path, required=True)
    parser.add_argument('--conf', type=str, default='superpoint_outdoor',
                        choices=list(confs.keys()))
    parser.add_argument('--as_half', action='store_true')
    parser.add_argument('--image_list', type=Path)
    parser.add_argument('--feature_path', type=Path)
    args = parser.parse_args()
    main(confs[args.conf], args.image_dir, args.export_dir, args.as_half)
