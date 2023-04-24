# merfish_tif
Extracting and analysing MERFISh tif files into multiple channel images for better cellpose segmentation 

# Workflow

1. Convert from original .dax to .tif file 

	
2. Extraction of 3 border staining + DAPI

```
...
```


3. Split 1 .tif into 4 different channels

```
...
```

4. Add colors and merge together 

```
...
```

5. (Optional) add export annotation of masks into QuPath

* For the annotation script to work one need to create a project in QuPath, then paste it in automate > script editor > runs script (delete empty lines, because otherwise it will get an error)

```
export_annotation.groovy
```
