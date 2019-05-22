import numpy as np
from xml.dom import minidom

CSVFILEPATH = 'test.csv'
CSVDELIM = ','
OUTFILE = CSVFILEPATH[:-4] + '.xml'

# Import the CSV into numpy array
filen = CSVFILEPATH
defects = np.loadtxt(open(filen,'rb'), delimiter=CSVDELIM)
defects = defects.astype(int)

# Generate the xml file
doc = minidom.Document()

annotation = doc.createElement('annotation')
doc.appendChild(annotation)

# Generate metadata elements and add them to 'annotation'
folder = doc.createElement('folder')
folder.appendChild(doc.createTextNode('images'))
annotation.appendChild(folder)
filename = doc.createElement('filename')
filename.appendChild(doc.createTextNode(filen[:-4]))
annotation.appendChild(filename)
segmented = doc.createElement('segmented')
segmented.appendChild(doc.createTextNode('0'))
annotation.appendChild(segmented)
width = doc.createElement('width')
width.appendChild(doc.createTextNode('1280'))
height = doc.createElement('height')
height.appendChild(doc.createTextNode('800'))
depth = doc.createElement('depth')
depth.appendChild(doc.createTextNode('3'))
size = doc.createElement('size')
size.appendChild(width)
size.appendChild(height)
size.appendChild(depth)
annotation.appendChild(size)


for line in defects:
  # Create defect properties
  xmin = doc.createElement('xmin')
  xmax = doc.createElement('xmax')
  ymin = doc.createElement('ymin')
  ymax = doc.createElement('ymax')

  # Create branch elements to be used
  objet = doc.createElement('object')
  bndbox = doc.createElement('bndbox')
  name = doc.createElement('name')
  pose = doc.createElement('pose')
  truncated = doc.createElement('truncated')
  difficult = doc.createElement('difficult')
  
  # Add text data to the elements
  name.appendChild(doc.createTextNode('defect'))
  pose.appendChild(doc.createTextNode('center'))
  truncated.appendChild(doc.createTextNode('1'))
  difficult.appendChild(doc.createTextNode('0'))
  
  if line.size == 2: # Basic x,y points
    xmin.appendChild(doc.createTextNode(str(line[0]-5)))
    xmax.appendChild(doc.createTextNode(str(line[0]+5)))
    ymin.appendChild(doc.createTextNode(str(line[1]-5)))
    ymax.appendChild(doc.createTextNode(str(line[1]+5)))
  elif line.size == 3:
    xmin.appendChild(doc.createTextNode(str(line[1]-5)))
    xmax.appendChild(doc.createTextNode(str(line[1]+5)))
    ymin.appendChild(doc.createTextNode(str(line[2]-5)))
    ymax.appendChild(doc.createTextNode(str(line[2]+5)))
  elif line.size == 4:
    xmin.appendChild(doc.createTextNode(str(line[0])))
    xmax.appendChild(doc.createTextNode(str(line[2])))
    ymin.appendChild(doc.createTextNode(str(line[1]-1)))
    ymax.appendChild(doc.createTextNode(str(line[3]+1)))
  else:
    continue
  bndbox.appendChild(xmin)
  bndbox.appendChild(xmax)
  bndbox.appendChild(ymin)
  bndbox.appendChild(ymax)
  
  # Add the elements to the defect
  objet.appendChild(name)
  objet.appendChild(pose)
  objet.appendChild(truncated)
  objet.appendChild(difficult)
  objet.appendChild(bndbox)

  # Add the defect to the overall list
  annotation.appendChild(objet)


xml_str = doc.toprettyxml(indent="  ")
with open(OUTFILE,"w") as f:
  f.write(xml_str)
