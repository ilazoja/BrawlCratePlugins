__author__ = "Kapedani (with credit to mawwwk)"
__version__ = "1.0"

from BrawlCrate.API import *
from BrawlLib.SSBB.ResourceNodes import *
from BrawlLib.SSBB.ResourceNodes.ProjectPlus import *
from BrawlCrate.UI import MainForm
from BrawlLib.Internal import *
from BrawlLib.Imaging import *
from System.IO import *
from BrawlLib.Internal.Windows.Forms import ProgressWindow
from mawwwkLib import *

#import csv

SCRIPT_NAME = "Detect Low Quality BRSTM Files"

log_file_path = "brstm_logs.txt"
debug_last_file_path = "last_file.txt"

brstmFiles = []			# List containing file names of all brstm files in pf\sound\strm
goodQualitySampleRate = 32000

## Start helper methods

# Populate brstmFiles[] by adding all brstm file names, then recursively run through each subfolder
def populateBrstmFilesList(dir, parentFolder=""):
	for file in Directory.CreateDirectory(dir).GetFiles():

		if ".brstm" in file.Name:
			# Swap backslash (\) with forward slash (/) for consistency
			filePath = (parentFolder + file.Name).replace("\\", "/")
			brstmFiles.append(filePath)

	for subfolder in Directory.GetDirectories(dir):
		subfolderName = subfolder.split("strm\\")[-1]
		populateBrstmFilesList(subfolder, subfolderName + "/")

## End helper methods
## Start of main script

# Prompt for directory
workingDir = BrawlAPI.OpenFolderDialog("Open pf, sound, or strm folder")
workingDir = str(workingDir)

# Derive strm and tracklist folder paths
[STRM_DIR, TRACKLIST_DIR] = [0,0]
if workingDir[-3:] == "\\pf":
	STRM_DIR = workingDir + "\\sound\\strm"
elif workingDir[-9:] == "\\pf\\sound":
	STRM_DIR = workingDir + "\\strm"
elif workingDir [-5:] == "\\strm":
	STRM_DIR = workingDir

if workingDir and not STRM_DIR:
	BrawlAPI.ShowError("Invalid directory", "Error")


elif workingDir:
	# Save currently opened file, if any
	CURRENT_OPEN_FILE = getOpenFile()

	# Get list of brstm file names in sound/strm directory, and store in brstmFiles[]
	populateBrstmFilesList(STRM_DIR)
	BRSTM_FILE_COUNT = len(brstmFiles)

	# Progress bar start
	progressBar = ProgressWindow()
	progressBar.Begin(0,BRSTM_FILE_COUNT,0)

	# Iterate through all files in tracklist folder
	filesOpenedCount = 0

	with open(log_file_path, 'w') as log_file:
		for filepath in brstmFiles:
			#with open(debug_last_file_path, 'w') as debug_file:
			#	debug_file.write(filepath.encode("utf8"))

			# Update progress bar
			filesOpenedCount += 1
			progressBar.Update(filesOpenedCount)

			# Open tracklist file
			if filepath.lower().EndsWith(".brstm"):
				#dmessage(filepath)
				BrawlAPI.OpenFile(STRM_DIR + "\\" + filepath)

				# Iterate through entries in tracklist
				track = BrawlAPI.RootNode

				# If file exists, get its index and delete it from brstmFiles[]
				# Check pinch mode track (trackname_b.brstm)
				if track.SampleRate < goodQualitySampleRate:
					log_file.write((filepath + ", " + str(track.SampleRate) + "\n").encode("utf8"))

	# Progress bar close
	progressBar.Finish()

	# Reopen previously-opened file
	if CURRENT_OPEN_FILE:
		BrawlAPI.OpenFile(CURRENT_OPEN_FILE)

	# RESULTS

	BrawlAPI.ShowMessage("Wrote brstm file paths with less than " + str(goodQualitySampleRate) + " sample rate to " + str(log_file_path), "Success!")


