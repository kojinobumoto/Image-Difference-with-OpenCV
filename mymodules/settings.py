def init():
    global DATA_SAVE_BASE_DIR, ORIG_IMAGE_DIRNAME, SECOND_IMAGE_DIRNAME, DATA_OUT_DIRNAME_BASE
    # global vars
    DATA_SAVE_BASE_DIR = 'img'

    ORIG_IMAGE_DIRNAME = DATA_SAVE_BASE_DIR + '/01.first'
    SECOND_IMAGE_DIRNAME = DATA_SAVE_BASE_DIR + '/02.second'
    DATA_OUT_DIRNAME_BASE = DATA_SAVE_BASE_DIR + '/03.diff'

    # if there's no saving directory, just create them.
    # (03.diff will be created in workers.py with timestamp.)
    from pathlib import Path
    Path(ORIG_IMAGE_DIRNAME).mkdir(exist_ok=True, parents=True)
    Path(SECOND_IMAGE_DIRNAME).mkdir(exist_ok=True, parents=True)
    # Path(DATA_OUT_DIRNAME_BASE).mkdir(exist_ok=True, parents=True)
