import unittest
import sys
from pathlib import Path
import concurrent.futures
import qt_wsi_reg.registration_tree as registration
from openslide import OpenSlide
import functools
import cv2
import numpy as np
import openslide 
from tqdm import tqdm 

from PIL import Image

class TestRegistrationMethods(unittest.TestCase):

    def setUp(self):
    
        self.parameters = {
                # feature extractor parameters
                "point_extractor": "sift",  #orb , sift
                "maxFeatures": 512, 
                "crossCheck": False, 
                "flann": False,
                "ratio": 0.7, 
                "use_gray": False,

                # QTree parameter 
                "homography": True,
                "filter_outliner": False,
                "debug": True,
                "target_depth": 0,
                "run_async": False,
                "num_workers": 2,
                "thumbnail_size": (1024, 1024),

            }


    def test_anhir(self):

        self.pic_results = Path(f"tests/results/Anhir")
        self.pic_results.mkdir(exist_ok=True, parents=True)
                
        base_path = Path(r"D:/ProgProjekte/Python/DeepFastAiAffine/examples/TrainSet/")

        slide_paths = []
        with open(str(base_path/"anhir.txt")) as file:
            lines = file.readlines()
            slide_paths = [line.rstrip().split(" ") for line in lines]

        for soure_path, target_path in tqdm(slide_paths[133:]):

            soure_path = base_path/soure_path
            target_path = base_path/target_path

            qtree = registration.RegistrationQuadTree(source_slide_path=soure_path, target_slide_path=target_path, **self.parameters)
            l0_fig, _ = qtree.draw_feature_points(num_sub_pic=5, figsize=(24, 24))
            l0_fig.savefig(self.pic_results / f'{soure_path.stem}-{target_path.stem}.png')  


    def test_breast_wsi(self):

        self.pic_results = Path(f"tests/results/breast")
        self.pic_results.mkdir(exist_ok=True, parents=True)
                
        start_folder = Path(r"D:\Datasets/Registration/Breast WSI Registration")

        slide_paths = []

        for folder in tqdm(list(start_folder.glob("*"))):

            folder_files = list(folder.glob("*.svs"))
            soure_path = None
            for ff in folder_files:
                if "HE.".lower() in ff.name.lower():
                    soure_path = ff
            if soure_path == None:
                soure_path = folder_files[0]

            target_files = [f for f in folder_files if f != soure_path]
        

            for target_path in target_files:

                qtree = registration.RegistrationQuadTree(source_slide_path=soure_path, target_slide_path=target_path, **self.parameters)
                l0_fig, _ = qtree.draw_feature_points(num_sub_pic=5, figsize=(24, 24))
                l0_fig.savefig(self.pic_results / f'{soure_path.stem}-{target_path.stem}.png') 


if __name__ == '__main__':

    unittest.main()