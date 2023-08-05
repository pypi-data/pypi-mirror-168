# labels file name and columns
LABELS_FILENAME = "labels.csv"
COL_ID = "data_id"
COL_DATA_PATH = "data_path"
COL_MASK_PATH = "mask_path"
COL_LABEL = "label"

# radiomics config
DST_CONFIG_NAME = "radiomics.yaml"

# radiomics features
RADIOMIC_FEATURE_DIRNAME = "feature_data"
RADIOMIC_FEATURE_FILENAME = "features.csv"

# image&video extension supported by opencv
IMAGE_EXTS = {"bmp", "dib", "jpeg", "jpg", "jpe", "jp2", "png", "webp", "pbm",
              "pgm", "ppm", "pxm", "pnm", "pfm", "sr", "ras", "tiff", "tif",
              "exr", "hdr", "pic"}

# from https://en.wikipedia.org/wiki/Video_file_format
VIDEO_EXTS = {"mkv", "flv", "vob", "ogv", "ogg", "avi", "mov", "wmv", "rm",
              "rmvb", "mp4", "m4p", "m4v", "mpg", "mp2", "mpeg", "mpe", "mpv",
              "m2v", "m4v", "3gp", "3g2"}
