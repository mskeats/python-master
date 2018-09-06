import poser

#############################################
# Function returns Node within a shader tree
# that has the given name
#############################################
def findNodeInMat( oMat, sName ):

    oFoundNode = None    
    oShaderTree = oMat.ShaderTree()
    oNodeSet =  oShaderTree.Nodes()

    for Node in oNodeSet:
        if Node.Name() == sName:
            print "         " + "Compare node name : " + Node.Name() + " name is  equal to " + sName + "  FOUND!"
            oFoundNode = Node
            break
        else:
            print "         " + "Compare node name : " + Node.Name() + " name is NOT equal to " + sName

        
    return oFoundNode

###############################################################
# Copies blender colour nodes from source to destinattion
###############################################################

def CopyInputs(oSource, oDest):
    
    (cRed,cGreen,cBlue) = oSource.InputByInternalName("Input_1").Value()
    
    print "            Setting input 1 to ("+str(cRed)+","+str(cGreen)+","+str(cBlue)+")"
    oDest.InputByInternalName("Input_1").SetColor(cRed,cGreen,cBlue)
    (cRed,cGreen,cBlue) = oSource.InputByInternalName("Input_2").Value()
    print "            Setting input 2 to ("+str(cRed)+","+str(cGreen)+","+str(cBlue)+")"
    oDest.InputByInternalName("Input_2").SetColor(cRed,cGreen,cBlue)

    return


#####################################################################
# Main
####################################################################

print "Start script"

sSearchnode = "Blender-PaintColor"

oActorSet = []

scn = poser.Scene()
cMat = scn.CurrentMaterial()

print "===== Finding blender node in current material ====="

print "Current material is called "+cMat.Name() + "\n"

oCopyName = findNodeInMat(cMat,sSearchnode)

if oCopyName:
    print "===== Scanning scene looking for other blender nodes called " + sSearchnode + " ===== \n"
    oActorSet = scn.Actors()
else:
    print "\n!!!!!! " + sSearchnode + " was not found in active material " + cMat.Name() + " so script cannot continue."


if oCopyName and not oActorSet:
    print "Something odd has happened, scene does not appear to have any actors????"


for oActor in oActorSet:
    
    print "\n   Checking figure:" + oActor.Name() + "\n"
    
    if oActor.IsProp():
        oMats = oActor.Materials()
        
        for Mat in oMats:
           
            print "      Scanning nodes used by material " + oActor.Name()+"."+Mat.Name()
            fNode = findNodeInMat(Mat,sSearchnode)
            if fNode:
                
                if fNode != oCopyName:
                    print ">      Found matching node!!!"
                    CopyInputs(oCopyName,fNode)
                else:
                    print ">      Found current node so ignoring!!!"
                    
            else:
                print "         " + oActor.Name()+ "." + Mat.Name() + " is not a matching node name\n"

    else:
        print "   " + oActor.Name() + " is not a prop so ignored \n"

