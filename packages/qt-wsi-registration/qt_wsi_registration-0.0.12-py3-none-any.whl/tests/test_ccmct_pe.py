import unittest
import sys
from pathlib import Path
import concurrent.futures
import qt_wsi_reg.registration_tree as registration
from openslide import OpenSlide
import functools
import numpy as np


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
                "run_async": True,
                "num_workers": 2,
                "thumbnail_size": (1024, 1024)
            }



    def test_pe(self):

        slide_paths = {source : target for source, target in 
                        zip(Path(r"D:/Datasets/ScannerStudy/Aperio/CCMCT").glob("*.svs"), 
                        Path(r"D:/Datasets/ScannerStudy/PE/CCMCT_29_06").glob("*.tif"))}


        for soure_path, targert_path in slide_paths.items():

            if "183715A"not in soure_path.name:
                continue

            qtree = registration.RegistrationQuadTree(source_slide_path=soure_path, target_slide_path=targert_path, **self.parameters)
            
            xmin=30939
            ymin=15389
            xmax=31106
            ymax=15492

            anno_width = xmax-xmin
            anno_height = ymax - ymin
            center_x = xmin + (anno_width / 2)
            center_y = ymin + (anno_height / 2)

            box = [center_x, center_y, anno_width, anno_height]
            trans_box = qtree.transform_boxes(np.array([box]))[0]

            new_x1 = int(trans_box[0] - trans_box[2] // 2)
            new_y1 = int(trans_box[1] - trans_box[3] // 2)
            new_x2 = int(trans_box[0] + trans_box[2] // 2)
            new_y2 = int(trans_box[1] + trans_box[3] // 2)

            vector = {'x1': new_x1, 'x2': new_x2, 'y1': new_y1, 'y2': new_y2}

            print(str(qtree))



if __name__ == '__main__':

    unittest.main()