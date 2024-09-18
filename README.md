# MERFISH images data analysis
Extracting and analysing MERFISH tif files into multiple channel images for better cellpose segmentation 

# Workflow

## Better to create new conda env for this project

1. Convert from original .dax to .tif file 

Dependencies:
* conda install -c conda-forge tifffile
* conda install -c anaconda numpy

```
python dax_converter.py input/path/with/.das_and_.inf/files
```

(Optional) copy files from original dir to the smaller dir with copy_files.sh
	
2. Extraction of 3 border staining + DAPI

```
python extract_tiff_images.py --i /input/dir/with/.tif/files --o output/empty/dir 
```


3. Split 1 .tif into 4 different channels

```
python split_tif.py -i /input/dir/with/.tif/files/4_images -o output/empty/dir/for/splited/files 
```

4. Add colors and merge together 

```
python merged_tif.py -i /input/dir/with/splited/files -o output/empty/dir/for/merged/files 
```

5. (Optional) add export annotation of masks into QuPath

* For the annotation script to work one need to create a project in QuPath, then paste it in automate > script editor > runs script (delete empty lines, because otherwise it will get an error)

```
export_annotation.groovy
```
