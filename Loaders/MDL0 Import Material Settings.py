__author__ = "mawwwk"
__version__ = "1.0"

from System.Windows.Forms import ToolStripMenuItem # Needed for all loaders
from BrawlCrate.API import *
from BrawlCrate.NodeWrappers import *
from mawwwkLib import *

## Start enable check functions
# Wrapper: MDL0Wrapper
def EnableCheck(sender, event_args):
	node = BrawlAPI.SelectedNode
	matsGroup = getChildFromName(node, "Materials")
	shadersGroup = getChildFromName(node, "Shaders")
	sender.Enabled = (node is not None and node.HasChildren and matsGroup and shadersGroup)

## End enable check functions
## Start loader functions

def import_model_settings(sender, event_args):
	# "Dest model" refers to the selected model whose mats/shaders are being replaced
	DEST_MODEL = BrawlAPI.SelectedNode
	DEST_MODEL_WRAPPER = BrawlAPI.SelectedNodeWrapper
	PARENT_MODELS_GROUP = BrawlAPI.SelectedNode.Parent
	
	# "Source model" refers to the imported model from which settings are being imported
	BrawlAPI.SelectedNodeWrapper.Parent.Parent.ImportModel()
	
	SOURCE_MODEL_INDEX = len(PARENT_MODELS_GROUP.Children)-1
	SOURCE_MODEL = DEST_MODEL.Parent.Children[SOURCE_MODEL_INDEX]
	
	DEST_MODEL_MAT_GROUP = getChildFromName(DEST_MODEL, "Materials")
	SOURCE_MODEL_MAT_GROUP = getChildFromName(SOURCE_MODEL, "Materials")
	
	DEST_MODEL_SHADERS = getChildFromName(DEST_MODEL, "Shaders").Children
	SOURCE_MODEL_SHADERS = getChildFromName(SOURCE_MODEL, "Shaders").Children
	
	sourceMatsList = getChildNodes(SOURCE_MODEL_MAT_GROUP)
	
	# Replace materials that share names
	for mat in DEST_MODEL_MAT_GROUP.Children:
		sourceMatName = mat.Name
		sourceMat = getChildFromName(SOURCE_MODEL_MAT_GROUP, sourceMatName)
		
		# If material exists in source model, assign it to dest model
		if sourceMat:
			mat.Replace(sourceMat)
			sourceMatsList.remove(sourceMat)
	
	# Copy any remaining materials (which don't share names)
	for sourceMat in sourceMatsList:
		newMat = DEST_MODEL_WRAPPER.NewMaterial()
		newMat.Replace(sourceMat)
		newMat.Name = sourceMat.Name
	
	# Copy over shaders
	# If dest model has fewer shaders than source model, add more to dest model until it's equal
	DEST_SHADER_COUNT = len(DEST_MODEL_SHADERS)
	SOURCE_SHADER_COUNT = len(SOURCE_MODEL_SHADERS)
	
	while DEST_SHADER_COUNT < SOURCE_SHADER_COUNT:
		DEST_MODEL_WRAPPER.NewShader()
		DEST_SHADER_COUNT += 1
		
	# For each shader in dest group, replace it with corresponding source shader
	for i in range(0, DEST_SHADER_COUNT, 1):
		sourceShader = SOURCE_MODEL_SHADERS[i]
		destShader = DEST_MODEL_SHADERS[i]
		
		destShader.Replace(sourceShader)
	
	# Delete temp stuff
	removeNode(SOURCE_MODEL)
	
	# Number of materials imported that aren't assigned to any objects -- may be incorrectly assigned or unused
	EMPTY_MATS_COUNT = len(sourceMatsList)
	
	BrawlAPI.ShowMessage("Materials and shaders imported successfully!\n\n" + str(EMPTY_MATS_COUNT) + " materials unassigned to objects (may be incorrectly assigned, or unused)","Success")
## End loader functions
## Start context menu add

BrawlAPI.AddContextMenuItem(MDL0Wrapper, "", "Import materials and shaders from an external MDL0 file", EnableCheck, ToolStripMenuItem("Import materials and shaders from...", None, import_model_settings))
