import fileinput
import sys
from tkinter import *
from random import randint
import math

# to be used with a priority queue
class Node:
	def __init__(self, name, value):
		self.name = str(name)
		self.value = value
	def increment_value(self):
		self.value = self.value + 1
	def get_name(self):
		return int(self.name)
	def get_value(self):
		return self.value
	def equals(self, name):
		return self.name == str(name)
	def toString(self):
		return "" + str(self.name) + ": " + str(self.value)

class Vertex:
	def __init__(self, name):
		self.name = str(name)
		self.connections = []
		self.coordinates = []
	
	def addVertex(self, vertex):
		self.connections.append(vertex)
	
	def insert_coordinates(self, coordinate):
		self.coordinates.append(coordinate)
	
	def get_connections(self):
		copy = []
		for item in self.connections:
			copy.append(item)
		return copy
	def get_coordinates(self):
		return self.coordinates
	def get_name(self):
		return self.name
	def toString(self):
		return "" + str(self.name) + ": " + str(self.connections) + ": " + str(self.coordinates) + ""
	def equals(self, name):
		return self.name == str(name)
	def copy(self):
		other = Vertex(self.name)
		
		for item in self.connections:
			other.addVertex(item)
		for coord in self.coordinates:
			other.insert_coordinates(coord)
		
		return other

class Vertex_List:
	def __init__(self, first_vertex):
		self.vertices = [first_vertex.get_name()]
		self.connections = []
		connections = first_vertex.get_connections()
		for item in connections:
			self.connections.append(Node(item, 1))

	def addVertex(self, vertex):
		v = vertex.copy()
		self.vertices.append(v.get_name())

		# copy the vertex's connections
		other_connections = v.get_connections()
		
		# remove vertex from self.connections
		for i in range(len(self.connections)):
			# print(self.connections[i].toString())
			# print(v.toString())
			if self.connections[i].equals(v.get_name()):
				self.connections.pop(i)
				break
		
		# remove any vertices included in the list
		removed = 0
		for i in range(len(other_connections)):
			curr1 = other_connections[i]
			for j in range(len(self.vertices)):
				curr2 = self.vertices[j]
				if curr2 == str(curr1):
					other_connections.pop(i)
					removed = 1
					break
			if removed:
				break

		to_remove = []
		
		for i in range(len(self.connections)):
			curr1 = self.connections[i]
			for j in range(len(other_connections)):
				curr2 = other_connections[j]
				if curr1.equals(str(curr2)):
					curr1.increment_value()
					to_remove.append(curr2)
		for item in to_remove:
			other_connections.remove(item)

		# add the contents of other_connections to self.connections as nodes
		for item in other_connections:
			self.connections.append(Node(item, 1))
		
	def get_vertices(self):
		return self.vertices
	def get_connections(self):
		return self.connections
	def get_best_connection(self):
		choices = []
		best_value = 1
		best_name = None
		for node in self.connections:
			if node.get_value() > best_value:
				best_value = node.get_value()
				best_name = node.get_name()
		for node in self.connections:
			if (node.get_value() == best_value) and (node.get_value() > 1):
				if best_name not in choices:
					choices.append(best_name)
				choices.append(node.get_name())
		if len(choices) > 0:
			index = randint(0, len(choices)-1)
			best_name = choices[index]
		if best_name == None:
			index = randint(0, len(self.connections)-1)
			# index = int((len(self.connections))/2)
			# index = len(self.connections)-2
			best_name = self.connections[index].get_name()
		
		return int(best_name)
	def toString(self):
		out = "List: ["
		for item in self.vertices:
			out = out + str(item) + ", "
		out = out + "], ["
		
		for item in self.connections:
			out = out + item.toString() + ", "
		out = out + "]"

		return out
	def get_names(self):
		v_list = []
		for vertex in self.vertices:
			v_list.append(int(vertex))
		return v_list
	def get_connections_number(self):
		return len(self.connections)
	def get_vertices_number(self):
		return len(self.vertices)

class Face:
	def __init__(self, vertex_list):
		self.vertices = []
		for i in range(len(vertex_list)):
			self.vertices.append(vertices[vertex_list[i]-1].copy())
			print(vertices[vertex_list[i]-1].toString())

		self.setCentre()
		self.setLight()
		self.setOrthogonalVector()
		self.setIntensity()
	
	def setCentre(self):
		self.centre = []
		
		# add vertex coordinates to list
		coords = []
		for vertex in self.vertices:
			coords.append(vertex.get_coordinates())

		index = 0;
		length = len(coords)
		while index < len(coords[0]):
			total = 0
			for vertex in coords:
				total = total + vertex[index]
			self.centre.append(total / length)
			index = index + 1

		print("centre = " + str(self.centre))
		# get the distance from the light source/viewer to the centre

	# assume that the light source is far to the negative side of the x-axis
	# and get the vector of the light source from self.centre
	def setLight(self):
		self.light = []
		
		for i in range(len(vp)):
			self.light.append(vp[i]-self.centre[i])
		
		self.lightdistance = pointDistance(vp, self.centre)
		print("distance = " + str(self.lightdistance))

	def setOrthogonalVector(self):
		# set vectors for face
		first = self.vertices[0].get_coordinates()
		second = self.vertices[1].get_coordinates()
		
		pq = []
		pr = []
		for i in range(0, 3):
			pq.append(self.centre[i] - first[i])
			pr.append(self.centre[i] - second[i])
		print("pq = " + str(pq))
		print("pr = " + str(pr))
		# determine orthogonal vector for face
		self.unitvector = crossProduct(pq, pr)
		print("vector = " + str(self.unitvector))
		
		# now divide the unit vector by the distance from the light source/viewer to the centre
		for i in range(len(self.unitvector)):
			self.unitvector[i] = float(self.unitvector[i] / self.lightdistance)

		print("vector = " + str(self.unitvector))
	def setIntensity(self):
		# set intensity to the dot product of vp and uv
		self.intensity = dot(self.unitvector, self.light)
		print("I = " + str(self.intensity) + "\n\n")
	
	def get_coordinates(self):
		array = []
		
		for v in self.vertices:
			array.append(v.get_coordinates)
		
		return array
	
	def getUnitVector(self):
		return self.unitvector
	
	def getCentre(self):
		return self.centre
	
	def getLight(self):
		return self.light
	
	def getIntensity(self):
		return self.intensity

def crossProduct(pq, pr):
	return [(pq[0]*pr[1]-pq[1]*pr[0]), 
		(-1 * (pq[0]*pr[2]-pq[2]*pr[0])), 
		(pq[1]*pr[2]-pq[2]*pr[1])]

def dot(first, second):
	return ((first[0]*second[0]) + (first[1]*second[1]) + (first[2]*second[2]))
	
def pointDistance(first, second):
	x = second[0]-first[0]
	y = second[1]-first[1]
	z = second[2]-first[2]
	return math.sqrt(x*x + y*y + z*z)

def get_input(filename):
	input = open(sys.argv[1], "r")
	i = 0
	num_vertices = 0
	count = 0
	name = ""
	for line in input:
		# print(line)
		
		if (i == 0):
			name = line
			print("name = " + name)
		if (i == 1):
			num_vertices = int(line)
			print("There are " + str(num_vertices) + " vertices.")
		if (i >= 2) & (i < (2 + num_vertices)):
			splitted = line.split(" ")
			edges = []
			# print(splitted)
			for j in splitted:
				curr = int(j)
				if (curr >= 0):
					edges.append(curr)
			# print(edges)
			vertices.append(edges)
		if (i > 2 + num_vertices):
			splitted = line.split("  ")
			# print(splitted)
			coords = []
			
			for j in splitted:
				curr = float(j)
				coords.append(curr)
			# print(coords)
			coordinates.append(coords)
		i=i+1
	
	print("Vertices = " + str(vertices))
	print("Coordinates = " + str(coordinates))

def get_edges():
	i = 0
	for vertex in vertices:
		if i > 0:
			for v in vertex:
				edge = [i]
				edge.append(v)
				if not duplicate_present(edge):
					edges.append(edge)
		i = i+1
	print("Edges = " + str(edges))
	
def duplicate_present(edge):
	reverse = reverse_list(edge)
	present = 0
	# print("Reverse: ", reverse)
	for curr in edges:
		if list_equals(reverse, curr):
			present = 1
	return present

def list_equals(first, second):
	equal = 0
	length = len(first)
	
	temp = []	
	for item in second:
		temp.append(item)
	
	for check in first:
		# print(first)
		# print("Check = " + str(check))
		for j in range(len(temp)):
			# print(temp[j])
			if temp[j] == check:
				# print("removing " + str(check))
				# first.remove(check)
				temp.pop(j)
				length = length-1
				# print(first)
				# print(temp)
				break

	if len(temp) == 0 and length == 0:
		equal = 1
	
	return equal
	
def reverse_list(list):
	reversed = []
	for item in list:
		reversed.insert(0, item)
	
	return reversed
	
def get_vertices():
	i = 0
	vertex_list = []
	for vertex in vertices:
		if i > 0:
			vertex_list.append(Vertex(i))
			for connection in vertex:
				vertex_list[i-1].addVertex(connection)
		i = i+1
	i = 0
	for vertex in coordinates:
		if i > 0:
			for coordinate in vertex:
				vertex_list[i-1].insert_coordinates(coordinate)
		i = i + 1

	for vertex in vertex_list:
		print(vertex.toString())

	return vertex_list

# Edges = [[1, 7], [1, 4], [1, 2], [2, 3], [2, 8], [3, 4], [3, 5], [4, 6], [5, 8], [5, 6], [6, 7], [7, 8]]
# faces = []
def get_faces():
	# print(edges)
	for i in range(0, 100):
		for edge in edges:
			for node in edge:
				vertex = vertices[int(node-1)]
				find_face(vertex.copy())
	# edge = edges[0]
	# for node in edge:
		# print("node = " + str(node))
		# vertex = vertices[int(node-1)]
		# find_face(vertex.copy())
	
	# edge = edges[1]
	# for node in edge:
		# print("node = " + str(node))
		# vertex = vertices[int(node-1)]
		# find_face(vertex.copy())
	
	# go through the list of faces and eliminate any faces that are tolong
	out = []
	for i in range(len(faces)):
		for j in range(i, len(faces)):
			first = faces[i]
			second = faces[j]
			first_is_subset = 0
			second_is_subset = 0

			if len(first) < len(second):
				first_is_subset = list_contains(first, second)
				
				if first_is_subset:
					out.append(second)
			elif len(first) > len(second):
				second_is_subset = list_contains(second, first)
				
				if second_is_subset:
					out.append(first)
	
	# remove any set found in out from faces
	for item in out:
		if item in faces:
			faces.remove(item)
			
	length = []
	total = 0;
	# get the average face length, remove any face that is unusualllong
	for face in faces:
		total = total + len(face)
	
	average = total / len(faces)
	average = int(average)
	print(average)
	
	out = []
	for face in faces:
		if len(face) > average:
			out.append(face)
	
	for item in out:
		if item in faces:
			faces.remove(item)

	for i in range(len(faces)):
		faces[i] = Face(faces[i])

	print(len(faces))

# starting with vertex attempt to create one or more new faces
def find_face(vertex):
	vertex_list = Vertex_List(vertex)
	edge_list = []
	
	# copy list of edges
	for edge in edges:
		edge_list.append(edge)
	# connections = vertex_list.get_connections() # get copy of the list's connections
	connections = vertex.get_connections()
	
	# print(vertex.toString())
	# prev = vertex
	# print("prev = " + str(prev.get_name()))
	# for i in range(2):
		# random = randint(0,len(connections)-1)
		# print("i = " + str(i) + ", random = " + str(random) + ", length = " + str(len(connections)))
		# v = vertices[int(connections[random])-1]
		# connections.remove(int(v.get_name()))
		# curr = v.copy()
		# vertex_list.addVertex(curr)
		# remove_edge(edge_list, Node(prev.get_name(), 1), Node(curr.get_name(), 1))
	
	# connections = vertex_list.get_connections()
	# a face needs at least three vertices, so first attempt to complete a face
	connected = 0
	# connected = finish_face(vertex_list, edge_list)

	while not connected:
		vertex_names = vertex_list.get_names()
		# if not possible, find another vertex
		index = vertex_list.get_best_connection()
		con = vertices[index-1].copy()
		# print(con.get_name())
		vertex_list.addVertex(con)
		
		# determine which edge was used to connect the new vertex
		# print("list = " + str(edge_list))
		for v in vertex_names:
			if remove_edge(edge_list, Node(v, 1), Node(con.get_name(), 1)):
				break
			# test = [int(v), int(con.get_name())]
			# reverse = [int(con.get_name()), int(v)]
			# if test in edge_list:
				# print("Removing " + str(test))
				# edge_list.remove(test)
				# break
			# elif reverse in edge_list:
				# print("Removing " + str(reverse))
				# edge_list.remove(reverse)
				# break
		# print("list = " + str(edge_list))
		
		# attempt to connect face
		connected = finish_face(vertex_list, edge_list)

	# simplify_connection()
	# print(vertex_list.toString() + " is connected")
	add_face(vertex_list.get_names())
	# print("Found " + str(vertex_list.get_vertices_number()) + " vertices in face.") 
	# print(vertex_list.toString())
	# print(edge_list)
	# print("\n\n")
	
		
def remove_edge(edges_list, first, second):
	success = 0

	first = int(first.get_name())
	if type(first) is not int:
		first = int(first)

	second = int(second.get_name())
	if type(second) is not int:
		second = int(second)

	seeking = [first, second]
	reverse = [second, first]
	
	found = (seeking in edges_list) or (reverse in edges_list)
	if found:
		# print("The edge: " + str(seeking) + " is present in " + str(edges_list))
		for i in range(len(edges_list)):
			if (edges_list[i] == seeking) or (edges_list[i] == reverse):
				edges_list.pop(i)
				success = 1
				break
	
	# print("Seeking = " + str(seeking))
	# print("Edge_list = " + str(edges_list))
	return success
	
# go through the edges that are left for one that connects two vertices in vertex_list
def finish_face(vertex_list, edge_list):
	# print("Attempting to finish face")
	connected = 0
	vertex_names = []
	
	for vertex in vertex_list.get_names():
		vertex_names.append(int(vertex))
		
	# print("vertex_list = " + str(vertex_names) + ", edge_list = " + str(edge_list))
	for edge in edge_list:
		node1, node2 = edge
		if node1 in vertex_names and node2 in vertex_names: 
			# if the edge connects two previously visited vertices we have a cycle
			connected = 1
			# print("Connected list: " + str(vertex_names))
			edge_list.remove(edge)
			break
	return connected

def add_face(proposed_face):
	already_present = 0
	for face in faces:
		if list_equals(proposed_face, face):
			already_present = 1
			break

	if not already_present:
		faces.append(proposed_face)

# determine if sub is a subset of full
def list_contains(sub, full):
	contains = 1

	# if any item isn't in array then contains is false
	for item in sub:
		if item not in full:
			contains = 0

	return contains

# draw the faces with a positive intensity value	
def draw_tet():
	c.delete(ALL)
	draw = []
	
	for face in faces:
		if face.getIntensity() > 0:
			draw.append(face)
	
	print("Drawing " + str(len(draw)) + " faces.")
	
	# go through the vertices for the visible faces and project them to the visual plane using pixel coordinates
	for face in draw:
		coords = face.get_coordinates()
		
		# get projected pixel coordinates
		proj(coords)
		
		color = "#"
		for i in range(len(col)):
			color = color + str((col[i] * face.getIntensity()))
		
		c.create_polygon(coords, fill=col, outline='black')

	coordinates = []
	for each in vertices:
		coordinates.append(each.get_coordinates())
	# print("Coordinates = " + str(coordinates))

	coordinates = convert_to_four_dimensions(coordinates)
	
	count_vertices = len(coordinates[0])
	width = c.winfo_width()+1
	height = c.winfo_height()+1
	# print("Width = " + str(width) + "\nHeight = " + str(height))

	for face in faces:
		print("face = " + str(face))
		face_coordinates = []
		for vertex in face:
			index = vertex-1 # get index for vertex
			translate(coordinates[0][index], coordinates[1][index], width, height, face_coordinates)
		print("face = " + str(face_coordinates))
		c.create_polygon(face_coordinates, fill=col, outline='black')

# take the coordinates of the face and return the pixel coordinates for the face on the visual plane in the same array
def proj(coords):
	print("L")

def convert_to_four_dimensions(coordinates):
	m = len(coordinates[0])+1
	n = len(coordinates)
	
	out = create_Zero_Matrix(m, n)

	for i in range(m-1):
		for j in range(n):
			out[i][j] = coordinates[j][i]
	out[m-1] = [1] * n

	return out

def create_Zero_Matrix(m, n):
	out = [0] * m

	for i in range(m):
		out[i] = [0] * n

	return out

# doesn't account for z axis at all yet
def translate(x, y, width, height, array):
	scale = 150
	array.append(scale*(x+width))
	array.append(scale*(y+height))

if len(sys.argv) > 1:
	top = Tk()
	c = Canvas(top, bg="white", height=600, width=1000)
	c.pack(fill=BOTH, expand=YES)
	
	# the viewer is initially located at [-100, 0, 0]
	vp = [-100, 0, 0]
	col = [20, 0, 199]

	vertices = [[]]
	coordinates = [[]]
	edges = []
	get_input(sys.argv[1])
	get_edges()
	print("The number of edges = " + str(len(edges)))
	vertices = get_vertices()
	faces = []
	get_faces()
	
	# next, get pixel coordinates for the faces
	draw_tet()
	top.mainloop()
# first = [1, 2, 3, 4]
# second = [3, 4, 1, 2]
# print(list_equals(first, second))

# for i in range(0, 100):
	# print(randint(0, 2))