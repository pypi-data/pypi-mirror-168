import os, glob
from simba.read_config_unit_tests import (read_config_entry, read_config_file, check_file_exist_and_readable)
from simba.features_scripts.unit_tests import read_video_info_csv, read_video_info
from simba.rw_dfs import read_df
from simba.misc_tools import get_fn_ext, check_multi_animal_status, detect_bouts
from simba.drop_bp_cords import getBpNames, create_body_part_dictionary
from collections import defaultdict
import pandas as pd
import numpy as np


class CueLightMovementAnalyzer(object):
    def __init__(self,
                 config_path: str=None,
                 pre_window: int=None,
                 post_window: int=None,
                 cue_light_names: list=None,
                 threshold: float=None,
                 rois: bool=False):
        self.config_path, self.cue_light_names = config_path, cue_light_names
        self.config, self.rois = read_config_file(config_path), rois
        self.p_threshold = threshold
        self.pre_window, self.post_window = pre_window, post_window
        self.project_path = read_config_entry(self.config, 'General settings', 'project_path', data_type='folder_path')
        self.in_dir = os.path.join(self.project_path, 'csv', 'cue_lights')
        self.file_type = read_config_entry(self.config, 'General settings', 'workflow_file_type', 'str', 'csv')
        self.vid_info_df = read_video_info_csv(os.path.join(self.project_path, 'logs', 'video_info.csv'))
        self.no_animals = read_config_entry(self.config, 'General settings', 'animal_no', 'int')
        self.x_cols, self.y_cols, self.pcols = getBpNames(config_path)
        self.multi_animal_status, self.multi_animal_id_lst = check_multi_animal_status(self.config, self.no_animals)
        self.files_found = glob.glob(self.in_dir + '/*.' + self.file_type)
        self.animal_bp_dict = create_body_part_dictionary(self.multi_animal_status, self.multi_animal_id_lst, self.no_animals, self.x_cols, self.y_cols, self.pcols,[])
        self.bp_dict, self.bp_columns = defaultdict(list), []
        for cnt, animal in enumerate(self.multi_animal_id_lst):
            bp_name = read_config_entry(self.config, 'cue_light_analysis', 'animal_{}_bp'.format(cnt+1), 'str')
            if bp_name == 'None':
                print('SIMBA ERROR: No body-parts found in config [process movements][animal_N_bp]')
                raise ValueError
            for c in ['_x', '_y', '_p']:
                self.bp_dict[animal].append(bp_name + c)
                self.bp_columns.append(bp_name + c)


    def euclidean_distance(self, bp_1_x_vals, bp_2_x_vals, bp_1_y_vals, bp_2_y_vals, px_per_mm):
        series = (np.sqrt((bp_1_x_vals - bp_2_x_vals) ** 2 + (bp_1_y_vals - bp_2_y_vals) ** 2)) / px_per_mm
        return series

    def find_frames_when_cue_light_on(self):
        self.light_on_dict = {}
        for cue_light in self.cue_light_names:
            light_bouts = detect_bouts(data_df=self.data_df, target_lst=[cue_light], fps=self.fps)
            print(light_bouts)


            #self.light_on_dict[cue_light] =


    def calculate_whole_session_movement(self):
        self.results = {}
        for file_cnt, file_path in enumerate(self.files_found):
            _, self.video_name, _ = get_fn_ext(file_path)
            self.results[self.video_name] = {}
            self.data_df = read_df(file_path, self.file_type).reset_index(drop=True)
            self.video_info_settings, self.px_per_mm, self.fps = read_video_info(self.vid_info_df, self.video_name)
            self.prior_window_frames_cnt = int(self.pre_window / (1000 / self.fps))
            self.post_window_frames_cnt = int(self.post_window / (1000 / self.fps))
            self.find_frames_when_cue_light_on()
            for animal_name, animal_bps in self.bp_dict.items():
                animal_df = self.data_df[animal_bps]
                if self.p_threshold > 0.00:
                    animal_df = animal_df[animal_df[animal_bps[2]] >= self.p_threshold]
                animal_df = animal_df.iloc[:, 0:2].reset_index(drop=True)
                df_shifted = animal_df.shift(1)
                df_shifted = df_shifted.combine_first(animal_df).add_suffix('_shifted')
                animal_df = pd.concat([animal_df, df_shifted], axis=1)
                self.movement = self.euclidean_distance(animal_df[animal_bps[0]], animal_df[animal_bps[0] + '_shifted'], animal_df[animal_bps[1]], animal_df[animal_bps[1] + '_shifted'], self.px_per_mm)















test = CueLightMovementAnalyzer(config_path='/Users/simon/Desktop/troubleshooting/light_analyzer/project_folder/project_config.ini',
                                cue_light_names=['Cue_light'],
                                pre_window=100,
                                post_window=100,
                                threshold=0.0)
test.calculate_whole_session_movement()


