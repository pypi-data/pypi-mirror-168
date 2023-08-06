from .backend import initialize_environment, process_data, findrelations_imp, use_gpu, gpu_available
import os
import numpy as np
import pandas as pd
from typing import Optional, List


class Nyxus:
    """Nyxus image feature extraction library

    Scalably extracts features from images.

    Parameters
    ----------
    features : list[str]
        List of features to be calculated. Individual features can be
        provided or pre-specified feature groups. Valid groups include:
            *ALL*
            *ALL_INTENSITY*
            *ALL_MORPHOLOGY*
            *BASIC_MORPHOLOGY*
            *ALL_GLCM*
            *ALL_GLRM*
            *ALL_GLSZM*
            *ALL_GLDM*
            *ALL_NGTDM*
            *ALL_BUT_GABOR*
            *ALL_BUT_GLCM*
        Both individual features and feature groups are case sensitive.
    neighbor_distance: float (optional, default 5.0)
        Any two objects separated by a Euclidean distance (pixel units) greater than this
        value will not be be considered neighbors. This cutoff is used by all features which
        rely on neighbor identification.
    pixels_per_micron: float (optional, default 1.0)
        Specify the image resolution in terms of pixels per micron for unit conversion
        of non-unitless features.
    coarse_gray_depth: int (optional, default 256)
        Custom number of levels in grayscale denoising used in texture features.
    n_feature_calc_threads: int (optional, default 4)
        Number of threads to use for feature calculation parallelization purposes.
    n_loader_threads: int (optional, default 1)
        Number of threads to use for loading image tiles from disk. Note: image loading
        multithreading is very memory intensive. You should consider optimizing
        `n_feature_calc_threads` before increasing `n_loader_threads`.
    using_gpu: int (optional, default -1)
        Id of the gpu to use. To find available gpus along with ids, using nyxus.get_gpu_properties().
        The default value of -1 uses cpu calculations. Note that the gpu features only support a single 
        thread for feature calculation. 
    """

    def __init__(
        self,
        features: List[str],
        neighbor_distance: float = 5.0,
        pixels_per_micron: float = 1.0,
        coarse_gray_depth: int = 256, 
        n_feature_calc_threads: int = 4,
        n_loader_threads: int = 1,
        using_gpu: int = -1
    ):
        if neighbor_distance <= 0:
            raise ValueError("Neighbor distance must be greater than zero.")

        if pixels_per_micron <= 0:
            raise ValueError("Pixels per micron must be greater than zero.")

        if coarse_gray_depth <= 0:
            raise ValueError("Custom number of grayscale levels (parameter coarse_gray_depth, default=256) must be non-negative.")

        if n_feature_calc_threads < 1:
            raise ValueError("There must be at least one feature calculation thread.")

        if n_loader_threads < 1:
            raise ValueError("There must be at least one loader thread.")
        
        if(using_gpu > -1 and n_feature_calc_threads != 1):
            print("Gpu features only support a single thread. Defaulting to one thread.")
            n_feature_calc_threads = 1
            
        if(using_gpu > -1 and not gpu_available()):
            print("No gpu available.")
            using_gpu = -1

        initialize_environment(
            features,
            neighbor_distance,
            pixels_per_micron,
            coarse_gray_depth, 
            n_feature_calc_threads,
            n_loader_threads,
            using_gpu
        )

    def featurize(
        self,
        intensity_dir: str,
        label_dir: Optional[str] = None,
        file_pattern: Optional[str] = ".*",
    ):
        """Extract features from provided images.

        Extracts all the requested features _at the image level_ from the images
        present in `intensity_dir`. If `label_dir` is specified, features will be
        extracted for each unique label present in the label images. The file names
        of the label images are expected to match those of the intensity images.

        Parameters
        ----------
        intensity_dir : str
            Path to directory containing intensity images.
        label_dir : str (optional, default None)
            Path to directory containing label images.
        file_pattern: str (optional, default ".*")
            Regular expression used to filter the images present in both
            `intensity_dir` and `label_dir`

        Returns
        -------
        df : pd.DataFrame
            Pandas DataFrame containing the requested features with one row per label
            per image.
        """
        if not os.path.exists(intensity_dir):
            raise IOError(
                f"Provided intensity image directory '{intensity_dir}' does not exist."
            )

        if label_dir is not None and not os.path.exists(label_dir):
            raise IOError(
                f"Provided label image directory '{label_dir}' does not exist."
            )

        if label_dir is None:
            label_dir = intensity_dir

        header, string_data, numeric_data = process_data(
            intensity_dir, label_dir, file_pattern
        )

        df = pd.concat(
            [
                pd.DataFrame(string_data, columns=header[: string_data.shape[1]]),
                pd.DataFrame(numeric_data, columns=header[string_data.shape[1] :]),
            ],
            axis=1,
        )

        # Labels should always be uint.
        if "label" in df.columns:
            df["label"] = df.label.astype(np.uint32)

        return df
    
    def using_gpu(self, gpu_on: bool):
        use_gpu(gpu_on)
		
class Nested:
    """Nyxus image feature extraction library / ROI hierarchy analyzer
	
	Example
	-------
	from nyxus import Nested
	nn = Nested()
	segPath = '/home/data/6234838c6b123e21c8b736f5/tissuenet_tif/seg'
	fPat = '.*'
	cnlSig = '_c'
	parCnl = '1'
	chiCnl = '0'
	rels = nn.findrelations (segPath, fPat, cnlSig, parCnl, chiCnl)	
    """

    def __init__(self):
        pass

    def findrelations(
        self,
        label_dir: str,
        file_pattern: str, 
        channel_signature: str, 
        parent_channel: str, 
        child_channel: str):
        """Finds parent-child relationships.

        Find parent-child relationships assuming that images ending <channel_signature><parent_channel> 
        contain parent ROIs and images ending <channel_signature><child_channel> contain child ROIs.

        Parameters
        ----------
        label_dir : str 
            Path to directory containing label images.
        file_pattern: str 
            Regular expression used to filter the images present in `label_dir`.
        channel_signature : str
            Characters preceding the channel identifier e.g. "_c". 
        parent_channel : str
            Identifier of the parent channel e.g. "1".
        child_channel : str
            Identifier of the child channel e.g. "0".

        Returns
        -------
        rel : array
            array of <parent label>,<child label> structure
        """

        if not os.path.exists(label_dir):
            raise IOError (f"Provided label image directory '{label_dir}' does not exist.")

        header, string_data, numeric_data = findrelations_imp (label_dir, file_pattern, channel_signature, parent_channel, child_channel)

        df = pd.concat(
            [
                pd.DataFrame(string_data, columns=header[: string_data.shape[1]]),
                pd.DataFrame(numeric_data, columns=header[string_data.shape[1] :]),
            ],
            axis=1,
        )

        # Labels should always be uint.
        if "label" in df.columns:
            df["label"] = df.label.astype(np.uint32)

        return df
		