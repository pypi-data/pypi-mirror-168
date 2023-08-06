import faiss
from os.path import join, dirname

from pimmi.toolbox import Sift, get_all_images
from pimmi.cli.config import parameters as prm
from pimmi.pimmi import create_index_mt
from test.utils import SMALL_DATASET_DIR

INDEX_TYPE = "IVF1024,Flat"

config_path = join(dirname(dirname(__file__)), "pimmi", "cli", "config.yml")
config_dict = prm.load_config_file(config_path)
prm.set_config_as_attributes(config_dict)


class TestIndex(object):
    def test_create_index(self):
        sift = Sift(prm.sift_nfeatures, prm.sift_nOctaveLayers, prm.sift_contrastThreshold, prm.sift_edgeThreshold,
                        prm.sift_sigma, prm.nb_threads)
        images = get_all_images(SMALL_DATASET_DIR)
        faiss_index = faiss.index_factory(128, INDEX_TYPE)
        index = {
            "faiss": faiss_index,
            "faiss_type": INDEX_TYPE,
            "meta": dict(),
            "meta_df": None,
            "faiss_nb_features": 1598,
            "faiss_nb_images": 11,
            "id_generator": 11
        }

        tested_index = create_index_mt(INDEX_TYPE, images, SMALL_DATASET_DIR, sift, only_empty_index=False)
        # assert index == tested_index


if __name__ == "__main__":
    ti = TestIndex()
    ti.test_create_index()

