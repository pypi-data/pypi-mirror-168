import logging
from packaging import version
from pathlib import Path
import numpy as np
from typing import Dict, List

__version__ = '1.3'

formatter = logging.Formatter(
    fmt='[%(asctime)s %(name)s %(levelname)s] %(message)s',
    datefmt='%Y/%m/%d %H:%M:%S')
handler = logging.StreamHandler()
handler.setFormatter(formatter)
handler.setLevel(logging.INFO)

logger = logging.getLogger("vml")
logger.setLevel(logging.INFO)
logger.addHandler(handler)
logger.propagate = False

try:
    import pycolmap
except ImportError:
    logger.warning('pycolmap is not installed, some features may not work.')
else:
    minimal_version = version.parse('0.3.0')
    found_version = version.parse(getattr(pycolmap, '__version__'))
    if found_version < minimal_version:
        logger.warning(
            'vml now requires pycolmap>=%s but found pycolmap==%s, '
            'please upgrade with `pip install --upgrade pycolmap`',
            minimal_version, found_version)


from . import extract_features, match_features, localize_sfm, pairs_from_retrieval, pairs_from_exhaustive, reconstruction
from .utils.parsers import parse_retrieval


def get_reconstruction_from_dir(model_dir: str) -> pycolmap.Reconstruction:
    """
    @Description :从文件夹获取重建数据结构
        model_dir: 数据目录
    @Returns     :
    """
    reconstruction = pycolmap.Reconstruction(model_dir)
    return reconstruction


def mapping(image_dir: str, output_dir: str, 
        retrieval_name: str, feature_name: str, 
        matcher_name: str, num_matchde: int = 10,
        is_exhaustive: bool = False):
    """
    @Description :建图
        image_dir: 图像根目录
        output_dir: 结果输出目录
        retrieval_name: 图像检索器名称
        feature_name: 特征提取器名称
        matcher_name: 特征匹配器名称
        num_matchde:  每幅图像进行匹配的图像对数
        is_exhaustive:是否进行详细列举匹配
    @Returns     :
    """
    path_config = get_working_path(image_dir, output_dir)
    config = get_extractor_matcher_config(retrieval_name, feature_name, matcher_name)
    
    global_extract = extract_features.ExtractFeatures(config['retrieval_conf'], path_config['map_retrieval_path'])
    global_extract.extract_features_for_dir(path_config['images_dir'])

    if(is_exhaustive):
        pairs_from_exhaustive.main(path_config['map_pairs_path'], features=path_config['map_retrieval_path'])
    else:
        pairs_from_retrieval.main(path_config['map_retrieval_path'], path_config['map_pairs_path'], num_matchde)

    local_extract = extract_features.ExtractFeatures(config['feature_conf'], path_config['map_features_path'])
    local_extract.extract_features_for_dir(path_config['images_dir'])

    match_feature = match_features.MatchFeatures(config['matcher_conf'], path_config['map_features_path'], path_config['map_matches_path'])
    match_feature.match_from_paths(path_config['map_pairs_path'], path_config['map_features_path'])
    # match_feature.match_from_pairs_path(path_config['map_pairs_path'])

    reconstruction.create_colmap_format_db(path_config['map_database_path'], path_config['images_dir'], path_config['map_pairs_path'], path_config['map_features_path'], path_config['map_matches_path'])
    sfm_model = reconstruction.run_reconstruction(path_config['map_dir'], path_config['map_database_path'], path_config['images_dir'])

    sfm_model.export_PLY(path_config['map_dir'] / 'sparse.ply')


def loc(image_dir: str, output_dir: str, 
        retrieval_name: str, feature_name: str, 
        matcher_name: str, query_name: str,
        num_matchde: int = 10) -> Dict :
    """
    @Description :定位
        image_dir: 图像根目录
        output_dir: 结果输出目录
        retrieval_name: 图像检索器名称
        feature_name: 特征提取器名称
        matcher_name: 特征匹配器名称
        query_name:   定位图像名称
        num_matchde:  每幅图像进行匹配的图像对数
    @Returns     :
    """

    path_config = get_working_path(image_dir, output_dir)
    config = get_extractor_matcher_config(retrieval_name, feature_name, matcher_name)
    
    global_extract = extract_features.ExtractFeatures(config['retrieval_conf'], path_config['loc_retrieval_path'])
    data = global_extract.get_data_from_file(path_config['querys_dir'], query_name)
    global_extract.extract_features_for_image(data)
    
    pairs_from_retrieval.main(path_config['loc_retrieval_path'], path_config['loc_pairs_path'], num_matchde, db_descriptors=path_config['map_retrieval_path'])

    local_extract = extract_features.ExtractFeatures(config['feature_conf'], path_config['loc_features_path'])
    data = local_extract.get_data_from_file(path_config['querys_dir'], query_name)
    local_extract.extract_features_for_image(data)

    match_feature = match_features.MatchFeatures(config['matcher_conf'], path_config['loc_features_path'], path_config['loc_matches_path'])
    match_feature.match_from_paths(path_config['loc_pairs_path'], path_config['map_features_path'], True)

    camera = infer_camera_from_image_file(path_config['querys_dir'] / query_name)
    model = get_reconstruction_from_dir(path_config['map_dir'])
    query_ids = get_query_img_pairs_ids_from_model(model, path_config['loc_pairs_path'], query_name)
    localizer = get_query_localizer(model)
    ret, _ = localize_sfm.pose_from_cluster(localizer, query_name, camera, query_ids, path_config['loc_features_path'], path_config['loc_matches_path'])
    del ret['inliers']
    return ret


def mvs(path_config: Dict) -> None:
    """
    @Description :多视立体重建
        path_config: 路径配置文件
    @Returns     :
    """
    pycolmap.undistort_images(path_config['sfm_dir'], path_config['sfm_dir'], path_config['images_dir'])
    pycolmap.patch_match_stereo(path_config['mvs_dir'])
    pycolmap.stereo_fusion(path_config['sfm_dir'] / "dense.ply", path_config['sfm_dir'])


def get_working_path(image_dir: str, output_dir: str) -> Dict:
    images_dir = Path(image_dir) / 'mapping'
    querys_dir = Path(image_dir) / 'querys'

    outputs = Path(output_dir)
    map_dir = outputs / 'map'
    mvs_dir = outputs / "mvs"
    loc_dir = outputs / "loc"

    map_database_path =  map_dir / 'database.db'
    map_retrieval_path = map_dir / 'retrievals.h5'
    map_features_path = map_dir / 'features.h5'
    map_matches_path = map_dir / 'matches.h5'
    map_pairs_path = map_dir / 'pairs-map.txt'

    loc_retrieval_path = loc_dir / 'retrievals.h5'
    loc_features_path = loc_dir / 'features.h5'
    loc_matches_path = loc_dir / 'matches.h5'
    loc_pairs_path = loc_dir / 'pairs-loc.txt'


    path_config = {'images_dir': images_dir, 'querys_dir': querys_dir, 
                   'map_pairs_path': map_pairs_path, 'map_retrieval_path': map_retrieval_path, 
                   'map_features_path': map_features_path, 'map_matches_path': map_matches_path, 
                   'map_dir': map_dir, 'map_database_path': map_database_path, 
                   'loc_pairs_path': loc_pairs_path, 'loc_retrieval_path': loc_retrieval_path, 
                   'loc_features_path': loc_features_path, 'loc_matches_path': loc_matches_path, 
                   'loc_dir': loc_dir, 'mvs_dir': mvs_dir}
    return path_config


def get_extractor_matcher_config(retrieval_name: str, 
                                 feature_name: str, 
                                 matcher_name: str) -> Dict:
    retrieval_conf = extract_features.confs[retrieval_name]
    feature_conf = extract_features.confs[feature_name]
    matcher_conf = match_features.confs[matcher_name]
    config = {'retrieval_conf': retrieval_conf,
              'feature_conf': feature_conf, 
              'matcher_conf': matcher_conf}
    return config


def get_query_img_pairs_ids_from_model(model: pycolmap.Reconstruction, 
                                       pairs_path: Path, 
                                       query_name: str) -> List[int]:
    retrieval_dict = parse_retrieval(pairs_path)
    model_image_name_to_id = {img.name: i for i, img in model.images.items()}
    ref_img_ids = []
    for n in retrieval_dict[query_name]:
        if n not in model_image_name_to_id:
            logger.warning(f'Image {n} was retrieved but not in database')
            continue
        ref_img_ids.append(model_image_name_to_id[n])
    return ref_img_ids


def infer_camera_from_image_file(image_path: Path)->pycolmap.Camera:
    camera = pycolmap.infer_camera_from_image(image_path)
    return camera


def infer_camera_from_image_data(data: Dict)->pycolmap.Camera:
    size =  data['original_size'][0].numpy()
    camera = pycolmap.Camera()
    camera.model_name = 'SIMPLE_RADIAL'
    camera.has_prior_focal_length = False
    focal_length = 1.2 * max(size)
    camera.initialize_with_id(camera.model_id, focal_length, size[0], size[1])
    return camera


def get_query_localizer(model: pycolmap.Reconstruction , 
                        conf: Dict =  {
                                        'estimation': {'ransac': {'max_error': 12}},
                                        'refinement': {'refine_focal_length': True, 
                                                       'refine_extra_params': True}
                                        })->localize_sfm.QueryLocalizer:
    localizer = localize_sfm.QueryLocalizer(model, conf)
    return localizer