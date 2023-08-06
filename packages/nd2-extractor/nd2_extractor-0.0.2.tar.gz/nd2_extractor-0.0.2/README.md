# Setup

Run the following commands 

`pip install -r nd2_extractor_requirements.txt`

`jupyter nbextension enable --py widgetsnbextension`

# Usage

### From a notebook:

Then launch `nd2_extractor_interactive.ipynb` in a Jupyter notebook.

### From the command line

```
$ python nd2_extractor.py --help
    usage: nd2_extractor.py [-h] --ND2_directory ND2_DIRECTORY --save_directory SAVE_DIRECTORY --save_type SAVE_TYPE [--workers WORKERS]

    Extract and ND2 file to TIFF or PNG (zarr coming soon)

    options:
    -h, --help            show this help message and exit
    --ND2_directory ND2_DIRECTORY
                            The absolute directory of the ND2 file
    --save_directory SAVE_DIRECTORY
                            The absolute directory of the extraction folder
    --save_type SAVE_TYPE
                            The file type to save as (PNG/TIFF)
    --workers WORKERS     The number of joblib workers to send to the extractor
  ```