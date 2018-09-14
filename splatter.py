import poser

############################################
# Function returns Node within a shader tree
# that has the given name
############################################
def findNodeInMat( oMat, sName ):

    oFoundNode = None    
    oShaderTree = oMat.ShaderTree()
    oNodeSet =  oShaderTree.Nodes()

    for Node in oNodeSet:
        if Node.Name() == sName:
            oFoundNode = Node
            break
        
    return oFoundNode

###############################################################
# Copies blender colour nodes from source to destinattion
###############################################################

def CopyInputs(oSource, oDest):
    
    inpS = oSource.InputByInternalName("Color")
    inpD = oDest.InputByInternalName("Color")
    
    if (inpS and inpD):
        (cRed,cGreen,cBlue) = inpS.Value()
        inpD.SetColor(cRed,cGreen,cBlue)
 
    return


#####################################################################
# Main
####################################################################

sSearchnode = "ChooseYourColor"

oActorSet = []

scn = poser.Scene()
cMat = scn.CurrentMaterial()
oCopyName = findNodeInMat(cMat,sSearchnode)

if oCopyName:
    oActorSet = scn.Actors()
else:
    poser.DialogSimple.MessageBox("Could not find ChooseYourColor node. Set {PR} material active before running script")
    poser.Quit

if oCopyName and not oActorSet:
    poser.DialogSimple.MessageBox("Could not find any actors, stopping script")
    poser.Quit

for oActor in oActorSet:
  
    if oActor.IsProp():
        oMats = oActor.Materials()
        
        for Mat in oMats:
           
            fNode = findNodeInMat(Mat,sSearchnode)
            if fNode:
                
                if fNode != oCopyName:
                    CopyInputs(oCopyName,fNode)
                    Mat.ShaderTree().UpdatePreview()


