import yaml
import os
import sys
import cv2
import time
import numpy as np
from tqdm import tqdm
import multiprocessing
from concurrent import futures
from signal import *
import argparse
'''
Program:
        This program is for visualize inference result on frames
        Output videos finally
History:
        2021/08/27 Eric Chen First release
Usage:
        python apply_mask.py {path/to/base_frame_folder} {path/to/base_mask_folder} \
                             {path/to/base_output_video_folder}
'''
def process_run(data):
    mask_folder, frame_folder, dst_path = data
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    fps = 30
    frame0 = cv2.imread(os.path.join(frame_folder, os.listdir(frame_folder)[0]))
    video = cv2.VideoWriter(dst_path, fourcc, fps, frame0.shape[:2][::-1])
    # label_order = ['head', 'right_hand', 'left_hand', 'others']
    colors = np.array([(255, 0, 0), (0, 255, 0), (0, 0, 255), (90, 90, 90)], dtype=np.uint8)
    for name in sorted(os.listdir(mask_folder)):
        mask = cv2.imread(os.path.join(mask_folder, name))
        frame = cv2.imread(os.path.join(frame_folder, name.replace('.png', '.jpg')))
        mask_ = np.zeros(mask.shape, dtype=np.uint8)
        for i, color in enumerate(colors):
            # i= 1,2,3,4
            mask_[np.where((mask==(i+1)).all(axis=2))] += color
        frame = cv2.addWeighted(frame, 1, mask_, 0.7, 0)
        video.write(frame.astype('uint8'))
    video.release()


def worker_init():
    # ignore the SIGINI in sub process, just print a log
    def sig_int(signal_num, frame):
        print('KeyInterrupt')
        sys.exit(0)
    signal(SIGINT, sig_int)


def get_args():
    parser = argparse.ArgumentParser(description='input path to frame, mask, target folder')
    parser.add_argument('-f','--frame_path',type=str,help='path/to/frame/folder')
    parser.add_argument('-m','--mask_path',type=str,help='path/to/mask/folder')
    parser.add_argument('-t','--target_path',type=str,help='path/to/target/folder')
    args = parser.parse_args()
    return args


def main():
    processes = os.cpu_count()
    args = get_args()
    # args.mask_path = os.path.join('/home/Datasets/mask','0901spreadthesign_women')
    # args.target_path = os.path.join('/home/Datasets/result','0915fb-test')
    # args.frame_path = os.path.join('/home/Datasets','ASL/train/0901spreadthesign_men/frame/')

    # label_order = ['all', 'head', 'right_hand', 'left_hand', 'others']
    if not os.path.exists(args.target_path):
        os.makedirs(args.target_path)
    for dt in os.listdir(args.mask_path):
        mask_folder = os.path.join(args.mask_path, dt)
        video_folder = os.path.join(args.target_path, dt)
        frame_folder = os.path.join(args.frame_path, dt)

        mask_folders = os.listdir(mask_folder)
        # print(video_folder)
        # with tqdm(total=len(mask_folders)) as pbar:
        with tqdm(total=len(args.mask_path)) as pbar:
            with multiprocessing.Pool(processes, worker_init) as pool:
                masks_folder, frames_folder, dst_paths = [], [], []
                masks_folder.append(os.path.join(mask_folder))
                frames_folder.append(os.path.join(frame_folder))
                dst_paths.append(os.path.join(video_folder) + '.avi')
                # dst_paths.append(os.path.join(video_folder, name.replace('jpg','avi')) )
                for i in (pool.imap_unordered(process_run, zip(masks_folder, frames_folder, dst_paths))):
                    pbar.update()

if __name__ == '__main__':
    main()