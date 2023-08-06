import matplotlib.pyplot as plt
import pprint
from pims import ND2Reader_SDK
pp = pprint.PrettyPrinter(indent=0)
from tabulate import tabulate
from tqdm.auto import tqdm 
import cv2
import numpy as np
from cowpy import cow
from celluloid import Camera
import colorama
from termcolor import colored
from joblib import Parallel, delayed, parallel_backend
import yaml
import argparse



def greeting():
    cheese = cow.Turtle()
    msg = cheese.milk("BakshiLab FAST ND2 Extractor - By Georgeos Hardo")
    print(msg)

def predict_t(directory): 
    frames =  ND2Reader_SDK(directory)
    frames.default_coords["t"] = 0
    t = 0
    while True:
        try:
            frames[t]
            t = t+1
        except:
            break
    frames.close()
    return int(t)

def predict_FOVs(directory):
    frames =  ND2Reader_SDK(directory)
    i = 1
    frames.default_coords["m"] = 0
    x_um = [frames[0].metadata["x_um"]]
    y_um = [frames[0].metadata["y_um"]]
    frames.default_coords["m"] = i
    while (x_um[0] != frames[0].metadata["x_um"] or y_um[0] != frames[0].metadata["y_um"]):
        frames.default_coords["m"] = i
        x_um.append(frames[0].metadata["x_um"])
        y_um.append(frames[0].metadata["y_um"])
        i+=1
    frames.close()
    return int(len(x_um) - 1)


def save_image(frame, i, img_format,save_directory,FOV,IMG_CHANNELS,channel):
    if np.sum(frame) == 0: # Check if a frame is empty, as Nikon inserts empty frames when you have some channels being read ever n frames.
        pass
    else:
        if img_format.lower() in "tiff":
            cv2.imwrite(save_directory + 'xy{}_{}_T{}.tif'.format(str(FOV).zfill(3),IMG_CHANNELS[channel],str(i).zfill(4)), frame, [cv2.IMWRITE_TIFF_COMPRESSION, 1])
        if img_format.lower() in "png":
            cv2.imwrite(save_directory + 'xy{}_{}_T{}.png'.format(str(FOV).zfill(3),IMG_CHANNELS[channel],str(i).zfill(4)), frame)
        else:
            raise Exception("Invalid format, please choose either TIFF or PNG")

        
        
def main_loop(directory,save_directory, joblib_workers, save_type = None):
    if save_directory[-1] != "/":
        save_directory = save_directory + "/"
    try:
        os.mkdir(save_directory)
    except:
        pass
    # Get parameters of the experiment
    frames =  ND2Reader_SDK(directory)
    metadata_dir = save_directory + "/../"
    with open(metadata_dir+'metadata.yml', 'w') as outfile:
        yaml.dump(frames.metadata, outfile, default_flow_style=False)

    IMG_HEIGHT = frames.metadata["tile_height"]
    IMG_WIDTH = frames.metadata["tile_width"]
    IMG_CHANNELS_COUNT = frames.metadata["plane_count"]
    SEQUENCES = frames.metadata["sequence_count"]
    IMG_CHANNELS = []
    for x in tqdm(range(IMG_CHANNELS_COUNT), desc = "Getting experiment info - please wait"):
        IMG_CHANNELS.append(frames.metadata["plane_{}".format(x)]["name"])
    frames.close() 
    num_FOVs = frames.sizes["m"]
    num_t = frames.sizes["t"]
    assert int(SEQUENCES / num_FOVs) == num_t, "FOVs ({}) and timepoints ({}) do not match sequences ({}) in the experiment - check your inputs".format(num_FOVs,num_t,SEQUENCES)
    print(colored("Experiment parameters (please verify before proceeding with extraction".format(num_FOVs), 'blue', attrs=['bold']))
    print(tabulate([
        ['TIMEPOINTS', num_t],
        ['FOVs', num_FOVs],
        ['IMG_HEIGHT', IMG_HEIGHT], 
        ['IMG_WIDTH', IMG_WIDTH],
        ["IMG_CHANNELS_COUNT", IMG_CHANNELS_COUNT],
        ['IMG_CHANNELS', IMG_CHANNELS]], headers=['Parameter', 'Value'], tablefmt='orgtbl'))


    if save_type:
        img_format = save_type
    else:
        print(colored("Choose image format: (TIFF/PNG) ", 'red', attrs=['bold']))
        img_format = input()


    FOVs_list = list(range(num_FOVs))
    CHANNELS_list = list(range(IMG_CHANNELS_COUNT))
    
    #if img_format == "PNG":
    #    joblib_workers = 200
    #else:
    #    joblib_workers = 500

    with ND2Reader_SDK(directory) as frames:
        for FOV in tqdm(FOVs_list, desc = "Overall (FOV) progress"):
            for channel in tqdm(CHANNELS_list, desc = "Channel progress in FOV {}".format(FOV), leave = False, position = 1):
                frames.iter_axes = 't'
                try:
                    frames.default_coords['c'] = channel
                except:
                    pass
                frames.default_coords['m'] = FOV
                Parallel(prefer="threads", n_jobs = joblib_workers)(delayed(save_image)(frames[i], i, img_format,save_directory,FOV,IMG_CHANNELS,channel) for i in tqdm(range(num_t), desc = "Frame progress in channel {}".format(IMG_CHANNELS[channel]), leave = False, position = 2) )

 
def main():
    parser = argparse.ArgumentParser(description="Extract and ND2 file to TIFF or PNG (zarr coming soon)")
    parser.add_argument("--ND2_directory", type=str, nargs=1, help="The absolute directory of the ND2 file", required=True)
    parser.add_argument("--save_directory", type=str, nargs=1, help="The absolute directory of the extraction folder", required=True)
    parser.add_argument("--save_type", type=str, nargs=1, help="The file type to save as (PNG/TIFF)", required=True)
    parser.add_argument("--workers", type=int, nargs=1, help="The number of joblib workers to send to the extractor")

    args = parser.parse_args()
    main_loop(args.ND2_directory[0], args.save_directory[0], args.workers[0], args.save_type[0])


if __name__ == "__main__":
    main()