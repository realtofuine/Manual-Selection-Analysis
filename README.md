# Manual Detection

1. Open Fiji/ImageJ and use rectangle tool to select well. Press T to save.
2. Export ROIs as zip file and upload to `rois` folder.
3. Update the folder and file paths in `manual_selection.sh`.
4. Ensure that well edge number is correct (p_Edge in `analyzedata.py`)
5. Run `bash manual_selection.sh`
6. Ensure no errors by looking at logs in `output` folder.
