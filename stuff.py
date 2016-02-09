#need a bunch of classes to represent the polyhedron

# each vertex knows the vertex it is connected to
class Vertex:
	def __init__(self, vertex):
		self.name = vertex
		
		# it can be assumed that there are edges connecting this vertex to the ones in the list
		self.connections = []
	
	def insertVertex(self, vertex):
		if vertex:
			self.connections.append(vertex)
		print(self.connections)
			
	def toString(self):
		return self.name + ": " + str(self.connections)

class Face:
	def __init__(self, face_name):
		self.name = face_name
		self.vertices = []
	
	def insertVertex(self, vertex):
		if vertex:
			self.vertices.append(vertex)
		print(self.vertices)
	
	def toString(self):
		return self.name + ": " + str(self.vertices)

x = Vertex("F")
x.insertVertex("G")
x.insertVertex("H")
print(x.toString())

y = Vertex("Q")
y.insertVertex("R")
y.insertVertex("S")
print(x.toString())
print(y.toString())

import tkinter as tk