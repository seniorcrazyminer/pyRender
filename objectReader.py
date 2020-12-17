

def getVertices(name):
  vertices = []
  with open(name, "r") as filestream:
    for line in filestream:
        cl = line.split(",")
        if cl[0] == "v" or cl[0] == "vlt" or cl[0] == "vpg":
          vertices.append([int(cl[1]), int(cl[2]), int(cl[3]), cl[0]])
  return vertices
          
