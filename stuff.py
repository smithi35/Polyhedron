#need a bunch of classes to represent the polyhedron

# each vertex knows the vertex it is connected to
class Vertex:
	name = ""
	#connections = []
	
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

x = Vertex("F")
x.insertVertex("G")
x.insertVertex("H")
print(x.toString())

y = Vertex("Q")
y.insertVertex("R")
y.insertVertex("S")
print(x.toString())
print(y.toString())