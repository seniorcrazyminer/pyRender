import objectReader as obr

import numpy as np
import math as math
import pygame
from pygame import gfxdraw

angles = [0, .1, math.pi]
camera = [0, 0, 0]
surface = [0, 0, 1]
gfxSurface = pygame.display.set_mode((640, 480))

qt = math.pi / 2
ht = math.pi


screen = [0, 0]

def init(scrn, surface):
  global screen
  global gfxSurface
  screen = scrn
  gfxSurface = surface


def initCamera(pos, fov):
  global camera
  global surface
  camera = pos
  surface[2] = 1 / math.tan(fov / 2)


def rotate(x, y, z):
  global angles
  delta_a = [x, y, z]
  for a in range(3):
    angles[a] = angles[a] + delta_a[a]

def moveCamera(x, z, y):
  global camera
  global angles
  camera[0] = camera[0] - math.sin(angles[1])*z
  camera[0] = camera[0] - math.cos(angles[1])*x
  camera[2] = camera[2] + math.cos(angles[1])*z
  camera[2] = camera[2] - math.sin(angles[1])*x
  camera[1] = camera[1] + y

def setAngle(ang):
  global angles
  angles = ang

def getVector(point):
  global angles
  global camera
  pos = [0, 0, 0]
  vector = [0, 0, 0]
  for p in range(3):
    pos[p] = point[p] - camera[p]
  m1 = [[1, 0, 0],[0, math.cos(angles[0]), math.sin(angles[0])], [0, -math.sin(angles[0]), math.cos(angles[0])]]
  m2 = [[math.cos(angles[1]), 0, -math.sin(angles[1])], [0, 1, 0], [math.sin(angles[1]), 0, math.cos(angles[1])]]
  m3 = [[math.cos(angles[2]), math.sin(angles[2]), 0], [-math.sin(angles[2]), math.cos(angles[2]), 0], [0, 0, 1]]
  vector = np.matmul(np.matmul(np.matmul(m1, m2), m3), pos)
  return vector

def getProjectionMatrix(near, far, left, right, top, bottom):
  return [[(2*near)/(right - left), 0, (right + left)/(right - left), 0], [0, (2*near)/(top - bottom), (top + bottom)/(top - bottom), 0], [0, 0, (far+ + near)/(near - far), (2*far*near)/(near - far)], [0, 0, -1, 0]]

def getSimplifiedProjectionMatrix(near, far, right, top):
  return [[near/right, 0, 0, 0], [0, near/top, 0, 0], [0, 0, (far + near)/(near-far), (2*far*near)/(near-far)], [0, 0, -1, 0]]

def getCoords(vector):
  global surface
  s1 = [[1, 0, (surface[0] / surface[2])], [0, 1, (surface[1] / surface[2])], [0, 0, (1 / surface[2])]]
  f = np.matmul(s1, vector)
  b = [f[0]/f[2],f[1]/f[2], (f[2] > .25)]
  return b

def getPoint(point):
  global screen
  p = getCoords(getVector(point))
  w = math.floor(screen[0] / 2)
  h = math.floor(screen[1] / 2)
  p[0] = (p[0]*w) + w
  p[1] = (p[1]*h) + h
  for i in range(2):
    p[i] = math.floor(p[i])
  return p

def drawPoint(point, color):
  global gfxSurface
  b = getPoint(point)
  x, y = [b[i] for i in [0,1]]
  if b[2] == 1:
    gfxdraw.pixel(gfxSurface, x + math.floor(screen[0] / 2), y + math.floor(screen[1] / 2), color)

def drawLine(point1, point2, color):
  global gfxSurface
  global screen
  b1 = getPoint(point1)
  b2 = getPoint(point2)
  w = math.floor(screen[0] / 2)
  h = math.floor(screen[1] / 2)
  x1, y1 = [b1[i] for i in [0,1]]
  x2, y2 = [b2[i] for i in [0,1]]
  if b1[2] == 1 and b2[2] == 1:
    gfxdraw.line(gfxSurface, x1, y1, x2, y2, color)

def transformCenter(center, x, y, z):
  return [center[0] + x, center[1] + y, center[2] + z]

def transformCoords(base, change):
  return [base[0] + change[0], base[1] + change[1], base[2] + change[2]]

def applyScalar(coord, scalar):
  for i in range(3):
    coord[i] = coord[i] * scalar
  return coord

def resizeVertices(vertices, scale):
  for i in range(len(vertices) - 1):
    for j in range(3):
      vertices[i][j] = vertices[i][j] * scale
  return vertices

def drawCube(center, dim, color):
  dx = dim[0] / 2
  dy = dim[1] / 2
  dz = dim[2] / 2
  
  drawLine(transformCenter(center, dx, dy, -dz) , transformCenter(center, dx, dy, dz), color)
  drawLine(transformCenter(center, -dx, dy, -dz) , transformCenter(center, -dx, dy, dz), color)
  drawLine(transformCenter(center, -dx, dy, dz) , transformCenter(center, dx, dy, dz), color)
  drawLine(transformCenter(center, -dx, dy, -dz) , transformCenter(center, dx, dy, -dz), color)

  drawLine(transformCenter(center, dx, -dy, -dz) , transformCenter(center, dx, -dy, dz), color)
  drawLine(transformCenter(center, -dx, -dy, -dz) , transformCenter(center, -dx, -dy, dz), color)
  drawLine(transformCenter(center, -dx, -dy, dz) , transformCenter(center, dx, -dy, dz), color)
  drawLine(transformCenter(center, -dx, -dy, -dz) , transformCenter(center, dx, -dy, -dz), color)

  drawLine(transformCenter(center, -dx, -dy, -dz) , transformCenter(center, -dx, dy, -dz), color)
  drawLine(transformCenter(center, -dx, -dy, dz) , transformCenter(center, -dx, dy, dz), color)
  drawLine(transformCenter(center, dx, -dy, -dz) , transformCenter(center, dx, dy, -dz), color)
  drawLine(transformCenter(center, dx, -dy, dz) , transformCenter(center, dx, dy, dz), color)

def drawPolygon(origin, numpoints, points, color, filled):
  global gfxSurface
  points1 = []
  noDraw = False
  for i in points:
    points1.append(getPoint(transformCoords(origin, i)))
    if getPoint(transformCoords(origin, i))[2] == 0:
      noDraw = True
  if filled:
    if not noDraw:
      gfxdraw.filled_polygon(gfxSurface, points1, color)
  if not filled:
    if not noDraw:
      gfxdraw.polygon(gfxSurface, points1, color)
    

def handleVertex(origin, vertex1, vertex2, color):
  coord1 = [vertex1[0], vertex1[1], vertex1[2]]
  coord2 = [vertex2[0], vertex2[1], vertex2[2]]

  if vertex2[3] == "vlt":
    drawLine(transformCoords(origin, coord1), transformCoords(origin, coord2), color)
  

def drawObject(pos, scale, fileName, color):
  drawVertices(pos, scale, obr.getVertices(fileName + ".obj"), color)

def drawVertices(pos, scale, vertices, color):
  vertices.append(next(reversed(vertices)))
  vertices = resizeVertices(vertices, scale)
  plain = []
  poly = []
  for i in range(len(vertices) - 1):
    if vertices[i][3] == "vpg":
      poly.append(vertices[i])
    if vertices[i][3] != "vpg":
      plain.append(vertices[i])
  for i in range(len(plain) - 1):
    handleVertex(pos, plain[i], plain[i + 1], color)
  if len(poly) > 2:
    drawPolygon(pos, len(poly), poly, color, 1)