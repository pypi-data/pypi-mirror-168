import argparse
import shutil
from typing import Optional, List, Dict, Any
import multiprocessing
from pathlib import Path
import pycolmap

from . import logger
from .utils.database import COLMAPDatabase
from .triangulation import (
    import_features, import_matches, estimation_and_geometric_verification,
    OutputCapture, parse_option_args)


def create_empty_db(database_path: Path):
    if database_path.exists():
        logger.warning('The database already exists, deleting it.')
        database_path.unlink()
    logger.info('Creating an empty database...')
    db = COLMAPDatabase.connect(database_path)
    db.create_tables()
    db.commit()
    db.close()


def import_images(image_dir: Path,
                  database_path: Path,
                  camera_mode: pycolmap.CameraMode,
                  image_list: Optional[List[str]] = None,
                  options: Optional[Dict[str, Any]] = None):
    """
    @Description :提取图像信息，并将图像导入数据库
        image_dir: 图像根文件夹
        database_path: 数据库的路径
        camera_mode: 指定相机模型
        image_list: 要导入的图像列表，为None时，导入根文件夹下的所有图像
        options: 图像信息读取配置, {'camera_model': 'SIMPLE_RADIAL', 
                                    'existing_camera_id': -1, 
                                    'camera_params': '', 
                                    'default_focal_length_factor': 1.2, 
                                    'camera_mask_path': ''}
    @Returns     :
    """
    logger.info('Importing images into the database...')
    if options is None:
        options = {}
    images = list(image_dir.iterdir())
    if len(images) == 0:
        raise IOError(f'No images found in {image_dir}.')
    with pycolmap.ostream():
        pycolmap.import_images(database_path, image_dir, camera_mode,
                               image_list=image_list or [],
                               options=options)


def get_image_ids(database_path: Path) -> Dict[str, int]:
    """
    @Description :从数据库获查询获取图像名和id的映射
        database_path: 数据库的路径
    @Returns     :Dict{'name': id, ...}
    """
    db = COLMAPDatabase.connect(database_path)
    images = {}
    for name, image_id in db.execute("SELECT name, image_id FROM images;"):
        images[name] = image_id
    db.close()
    return images


def create_colmap_format_db(database_path: Path,
                            image_dir: Path,
                            pairs_path: Path,
                            features_path: Path,
                            matches_path: Path,
                            camera_mode: pycolmap.CameraMode = pycolmap.CameraMode.AUTO,
                            verbose: bool = False,
                            skip_geometric_verification: bool = False,
                            min_match_score: Optional[float] = None,
                            image_list: Optional[List[str]] = None,
                            image_options: Optional[Dict[str, Any]] = None):
    """
    @Description :创建colmap格式的数据库文件
        database_path: 数据库文件路径
        image_dir: 图像跟文件路径
        pairs_path: 图像对文件路径
        features_path: 局部特征文件路径
        matches_path: 匹配文件路径
        camera_mode: 相机模型
        verbose: 是否打印详情
        skip_geometric_verification: 是否跳过几何验证
        min_match_score: 最小匹配分数
        image_list: 要添加的图像列表
        image_options:  图像信息读取配置
    @Returns     :
    """
    assert features_path.exists(), features_path
    assert pairs_path.exists(), pairs_path
    assert matches_path.exists(), matches_path

    create_empty_db(database_path)
    import_images(image_dir, database_path, camera_mode,
                  image_list, image_options)
    image_ids = get_image_ids(database_path)
    import_features(image_ids, database_path, features_path)
    import_matches(image_ids, database_path, pairs_path, matches_path,
                   min_match_score, skip_geometric_verification)
    if not skip_geometric_verification:
        estimation_and_geometric_verification(
            database_path, pairs_path, verbose)


def run_reconstruction(sfm_dir: Path,
                       database_path: Path,
                       image_dir: Path,
                       verbose: bool = False,
                       options: Optional[Dict[str, Any]] = None,
                       ) -> pycolmap.Reconstruction:
    """
    @Description :重建
        sfm_dir: 重建文件输出路径
        database_path:  数据库文件路径
        image_dir: 图像跟根文件路径
        verbose: 是否打印详情
        options: 重建配置,{'min_num_matches': 15,               'ignore_watermarks': False, 
                          'multiple_models': True,             'max_num_models': 50, 
                          'max_model_overlap': 20,             'min_model_size': 10, 
                          'init_image_id1': -1,                'init_image_id2': -1, 
                          'init_num_trials': 200,              'extract_colors': True, 
                          'num_threads': -1,                   'min_focal_length_ratio': 0.1, 
                          'max_focal_length_ratio': 10.0,      'max_extra_param': 1.0, 
                          'ba_refine_focal_length': True,      'ba_refine_principal_point': False, 
                          'ba_refine_extra_params': True,      'ba_min_num_residuals_for_multi_threading': 50000, 
                          'ba_local_num_images': 6,            'ba_local_function_tolerance': 0.0, 
                          'ba_local_max_num_iterations': 25,   'ba_global_use_pba': False, 
                          'ba_global_pba_gpu_index': -1,       'ba_global_images_ratio': 1.1, 
                          'ba_global_points_ratio': 1.1,       'ba_global_images_freq': 500, 
                          'ba_global_points_freq': 250000,     'ba_global_function_tolerance': 0.0, 
                          'ba_global_max_num_iterations': 50,  'ba_local_max_refinements': 2, 
                          'ba_local_max_refinement_change': 0.001,   'ba_global_max_refinements': 5, 
                          'ba_global_max_refinement_change': 0.0005, 'snapshot_path': '', 
                          'snapshot_images_freq': 0, 'image_names': set(), 'fix_existing_images': False}
    @Returns     :重建对象
    """
    models_path = sfm_dir / 'models'
    models_path.mkdir(exist_ok=True, parents=True)
    logger.info('Running 3D reconstruction...')
    if options is None:
        options = {}
    options = {'num_threads': min(multiprocessing.cpu_count(), 16), **options}
    with OutputCapture(verbose):
        with pycolmap.ostream():
            reconstructions = pycolmap.incremental_mapping(
                database_path, image_dir, models_path, options=options)

    if len(reconstructions) == 0:
        logger.error('Could not reconstruct any model!')
        return None
    logger.info(f'Reconstructed {len(reconstructions)} model(s).')

    largest_index = None
    largest_num_images = 0
    for index, rec in reconstructions.items():
        num_images = rec.num_reg_images()
        if num_images > largest_num_images:
            largest_index = index
            largest_num_images = num_images
    assert largest_index is not None
    logger.info(f'Largest model is #{largest_index} '
                f'with {largest_num_images} images.')

    for filename in ['images.bin', 'cameras.bin', 'points3D.bin']:
        if (sfm_dir / filename).exists():
            (sfm_dir / filename).unlink()
        shutil.move(
            str(models_path / str(largest_index) / filename), str(sfm_dir))
    shutil.rmtree(str(models_path))
    return reconstructions[largest_index]


def main(sfm_dir: Path,
         image_dir: Path,
         pairs: Path,
         features: Path,
         matches: Path,
         camera_mode: pycolmap.CameraMode = pycolmap.CameraMode.AUTO,
         verbose: bool = False,
         skip_geometric_verification: bool = False,
         min_match_score: Optional[float] = None,
         image_list: Optional[List[str]] = None,
         image_options: Optional[Dict[str, Any]] = None,
         mapper_options: Optional[Dict[str, Any]] = None,
         ) -> pycolmap.Reconstruction:

    assert features.exists(), features
    assert pairs.exists(), pairs
    assert matches.exists(), matches

    sfm_dir.mkdir(parents=True, exist_ok=True)
    database = sfm_dir / 'database.db'

    create_empty_db(database)
    import_images(image_dir, database, camera_mode, image_list, image_options)
    image_ids = get_image_ids(database)
    import_features(image_ids, database, features)
    import_matches(image_ids, database, pairs, matches,
                   min_match_score, skip_geometric_verification)
    if not skip_geometric_verification:
        estimation_and_geometric_verification(database, pairs, verbose)
    reconstruction = run_reconstruction(
        sfm_dir, database, image_dir, verbose, mapper_options)
    if reconstruction is not None:
        logger.info(f'Reconstruction statistics:\n{reconstruction.summary()}'
                    + f'\n\tnum_input_images = {len(image_ids)}')
    return reconstruction


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--sfm_dir', type=Path, required=True)
    parser.add_argument('--image_dir', type=Path, required=True)

    parser.add_argument('--pairs', type=Path, required=True)
    parser.add_argument('--features', type=Path, required=True)
    parser.add_argument('--matches', type=Path, required=True)

    parser.add_argument('--camera_mode', type=str, default="AUTO",
                        choices=list(pycolmap.CameraMode.__members__.keys()))
    parser.add_argument('--skip_geometric_verification', action='store_true')
    parser.add_argument('--min_match_score', type=float)
    parser.add_argument('--verbose', action='store_true')

    parser.add_argument('--image_options', nargs='+', default=[],
                        help='List of key=value from {}'.format(
                            pycolmap.ImageReaderOptions().todict()))
    parser.add_argument('--mapper_options', nargs='+', default=[],
                        help='List of key=value from {}'.format(
                            pycolmap.IncrementalMapperOptions().todict()))
    args = parser.parse_args().__dict__

    image_options = parse_option_args(
        args.pop("image_options"), pycolmap.ImageReaderOptions())
    mapper_options = parse_option_args(
        args.pop("mapper_options"), pycolmap.IncrementalMapperOptions())

    main(**args, image_options=image_options, mapper_options=mapper_options)
