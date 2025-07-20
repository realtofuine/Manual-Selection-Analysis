# Manual Detection
1. Delete all files other than .gitkeep in `cropped_videos` folder.
2. Open Fiji/ImageJ and use rectangle tool to select well. Press T to save.
3. Export ROIs as zip file and upload to `rois` folder.
4. Update the folder and file paths in `manual_selection.sh`.
5. Ensure that well edge number is correct (p_Edge in `analyzedata.py`)
5. Run `bash /users/rrai8/zebrafish_analysis/Manual-Selection/manual_selection.sh`
6. Ensure no errors by looking at logs in `output` folder.