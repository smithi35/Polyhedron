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

	def set_coordinates(self, coordinates):
		self.coordinates = []

		for c in coordinates:
			self.coordinates.append(c)

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

		self.orderVertices()
		self.setCentre()
		self.setLight()
		self.setOrthogonalVector()
		self.setIntensity()
	
	# ensure that the vertices are in the proper order
	def orderVertices(self):
		# if there are less than 4 vertices don't bother
		if len(self.vertices) > 3:
			length = len(self.vertices)
			copy = []

			for i in range(len(self.vertices)):
				copy.append(self.vertices[i].copy())

			# determine whether the vertices are in the right order by ensuring there is an edge between vertices adjacent in self.vertices
			connected = 1

			for i in range(len(self.vertices)):
				first = self.vertices[i-1].get_name()
				second = self.vertices[i].get_name()
				target = [first, second]
				reverse = [second, first]
				found = 0

				for e in edges:
					if (e == target) or (e == reverse):
						found = 1

				if not found:
					connected = 0
					break

			self.vertices = [copy[0]]
			copy.pop(0)

			# go through copy and insert connected vertices into self.vertices
			while copy:
				# curr is the last item in self.vertices
				curr = self.vertices[-1] 

				insert = 0
				# go through copy and find a vertex that curr is connected to 
				for i in range(len(copy)):
					if int(copy[i].get_name()) in curr.get_connections():
						self.vertices.append(copy[i])
						insert = 1
						copy.pop(i)
						break

			if len(self.vertices) != length:
				exit("Fucked up and have the wrong number of vertices")

		# print the vertices
		v_string = "self.vertices = "
		for v in self.vertices:
			v_string = v_string + " " + v.get_name()
		# print(v_string)

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

		# print("centre = " + str(self.centre))
		# get the distance from the light source/viewer to the centre

	# assume that the light source is far to the negative side of the x-axis
	# and get the vector of the light source from self.centre
	def setLight(self):
		self.light = []
		
		for i in range(len(vp)):
			self.light.append(vp[i])
			# -self.centre[i]
		
		# print("Light vector = " + str(self.light))
		self.lightdistance = pointDistance(vp, self.centre)
		# print("distance = " + str(self.lightdistance))

	def setOrthogonalVector(self):
		# set vectors for face
		first = self.vertices[0].get_coordinates()
		second = self.vertices[1].get_coordinates()
		third = self.vertices[2].get_coordinates()
		
		pq = []
		pr = []
		for i in range(0, 3):
			pq.append(first[i] - second[i])
			pr.append(first[i] - third[i])

		# determine orthogonal vector for face
		self.unitvector = crossProduct(pq, pr)
		# print("vector = " + str(self.unitvector))	

		# now divide the unit vector by the distance from the light source/viewer to the centre
		for i in range(len(self.unitvector)):
			self.unitvector[i] = float(self.unitvector[i] / self.lightdistance)
		# print("vector = " + str(self.unitvector))

		if points_at_origin(self.unitvector, first):
			# print("multiplying unit vector by -1")
			# needs to be pointing away from the tetrahedron and the origin
			opposite = []

			for i in range(len(self.unitvector)):
				opposite.append((-1 * self.unitvector[i]))

			self.unitvector = opposite
			# print("vector = " + str(self.unitvector))

	def setIntensity(self):
		# set intensity to the dot product of vp and uv
		# print("light vector = " + str(self.light))
		self.intensity = dot(self.unitvector, self.light)
		# print("I = " + str(self.intensity) + "\n\n")
	
	def get_coordinates(self):
		array = []

		for v in self.vertices:
			array.append(v.get_coordinates())

		return array
	
	def getUnitVector(self):
		return self.unitvector

	def getCentre(self):
		return self.centre

	def getLight(self):
		return self.light

	def getIntensity(self):
		return self.intensity

	def getDistance(self):
		return self.lightdistance

	# returns the string representation of the vertices
	def getVerteces(self):
		out = []

		for i in range(len(self.vertices)):
			out.append(self.vertices[i].get_name())

		return out

# returns the cross product of two 3-dimensional vectors
def crossProduct(pq, pr):
	out = None

	if (len(pr) == 3) and (len(pq) == 3):
		out = []
		out.append(((pq[1]*pr[2]) - (pq[2]*pr[1])))
		out.append((-1 * (pq[0]*pr[2]) - (pq[2]*pq[0])))
		out.append(((pq[0]*pr[1]) - (pq[1]*pr[0])))

	return out
		
# get the scalar dot product of the two vectors
def dot(first, second):
	tally = 0

	if len(first) == len(second):
		for i in range(len(first)):
			tally = tally + (first[i] * second[i])
	else:
		exit("Cannot compute dot product of different sized arrays")
	return tally

# get the distance between the two three-dimensional points
def pointDistance(first, second):
	x = second[0]-first[0]
	y = second[1]-first[1]
	z = second[2]-first[2]
	return math.sqrt(x*x + y*y + z*z)

# returns 0 if vector does not point in the direction of the origin
def points_at_origin(vector, point):
	# assume that the vector doesn't point to the origin
	origin = 0

	small_vector = []
	for i in range(len(vector)):
		small_vector.append((vector[i] / 10))

	# the vector has to be very small
	# print("point = " + str(point))

	# apply the vector to the point and see if it is closer to the origin
	next_point = [point[0] + small_vector[0], 
		point[1] + small_vector[1], 
		point[2] + small_vector[2]]

	# print("next_point = " + str(next_point))

	# determine distances from origin
	point_distance = pointDistance(point, [0,0,0])
	next_point_distance = pointDistance(next_point, [0,0,0])

	# print("point distance = " + str(point_distance))
	# print("next_point_distance = " + str(next_point_distance))

	if point_distance > next_point_distance:
		origin = 1

	return origin

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
			# print("name = " + name)

		if (i == 1):
			num_vertices = int(line)
			# print("There are " + str(num_vertices) + " vertices.")

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
	# print("Edges = " + str(edges))
	
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
	# get the average face length, remove any face that is unusually long
	for face in faces:
		total = total + len(face)

	average = total / len(faces)
	average = int(average)
	# print(average)

	out = []
	for face in faces:
		if len(face) > average:
			out.append(face)
	
	for item in out:
		if item in faces:
			faces.remove(item)

	print("Faces = " + str(faces) + ", there are " + str(len(faces)) + " of them")

	# print(len(faces))

# starting with vertex attempt to create one or more new faces
def find_face(vertex):
	vertex_list = Vertex_List(vertex)
	edge_list = []
	
	# copy list of edges
	for edge in edges:
		edge_list.append(edge)
	# connections = vertex_list.get_connections() # get copy of the list's connections
	connections = vertex.get_connections()

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

# if the face is unique, add it to the list of faces
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

	originals = []
	for i in range(len(faces)):
		originals.append(faces[i])
		faces[i] = Face(faces[i])

	for face in faces:
		# if face.getIntensity() > -0.1:
		draw.append(face)

	# sort started with the most distant face
	# print("Drawing " + str(len(draw)) + " faces")
	draw = sort_faces(draw)

	# print("Drawing " + str(len(draw)) + " faces.")

	# go through the vertices for the visible faces and project them to the visual plane using pixel coordinates
	for face in draw:
		# print("\nDrawing face: " + str(face.getVerteces()))
		coords = face.get_coordinates()
		# print("I = " + str(face.getIntensity()))

		# get projected pixel coordinates
		projected = proj(coords)

		color = "#"
		for i in range(len(col)):
			if (face.getIntensity() < 1) and (face.getIntensity() > 0) :
				intensity = int(col[i] * face.getIntensity())
				intense_string = "{0:03X}".format(intensity)
			elif face.getIntensity() < 0:
				intensity = int(col[i] * 0.1)
				intense_string = "{0:03X}".format(intensity)
			else :
				intense_string = str(col[i])

			# print(intense_string)
			color = color + intense_string
		# print("col = " + str(color))

		c.create_polygon(projected, fill=color, outline='black')

	for i in range(len(originals)):
		faces[i] = originals[i]

# insertion sort because it is simple and there won't be many faces to sort
def sort_faces(face_list):
	out = []

	# for each iteration of the loop find the most distant and insert to the end of out
	do_continue = 1
	while face_list:
		distant = 0
		most_distant_item = face_list[0]
		index = 0

		for i in range(len(face_list)):
			if face_list[i].getDistance() > distant:
				index = i
				distant = face_list[i].getDistance()
				most_distant_item = face_list[i]

		out.append(most_distant_item)
		face_list.pop(index)

	return out

# take the coordinates of the face and return the pixel coordinates for the face on the visual plane in the same array
def proj(coords):
	out = []

	for i in range(len(coords)):
		v = [vp[0], vp[1], vp[2], 1]
		# get coordinates of each vertex and project
		# vp is the viewpoint and is predefined, as is the plane, plane

		P = []
		for item in coords[i]:
			P.append(item)
		P.append(1)
		# print("P = " + str(P))

		psigma = dot(P,plane)
		vsigma = dot(v,plane)
		quotient = psigma/vsigma

		for i in range(len(v)):
			v[i] = v[i] * quotient
		# print("v = " + str(v))
		projection = []
		for i in range(len(v)):
			projection.append((P[i] - v[i]))

		if projection[3] != 1:
			for i in range(len(projection)):
				projection[i] = projection[i] / projection[3]

		# print("projection = " + str(projection))
		# get pixel coordinates by shifting up and to the right, and multiply by a scalar to increase the size of the shape

		# print("projection[1] = " + str(projection[0]))
		# print("projection[2] = " + str(projection[1]))	

		if scale > 0 :
			array = []
			array.append((projection[2] * scale * 200) + (width / 2))
			array.append((projection[1] * 200 * scale) + (height / 2))
		else :
			array = []
			array.append((projection[2] * 200) + (width / 2))
			array.append((projection[1] * 200) + (height / 2))
		# print("Array = " + str(array))
		out.append(array)
 
	return out

# go through the vertices and change them according to the rotaion matrix
def rotateTetrahedron(rotation_matrix):
	for vertex in vertices:
		# set vertex coordinates as matrix
		coords = vertex.get_coordinates()
		vertex_matrix = []

		for c in coords:
			vertex_matrix.append([c])

		vertex_matrix = matMul(rotation_matrix, vertex_matrix)

		if vertex_matrix:
			replacement = []

			# take matrix and replace coordinates with it as an array
			for array in vertex_matrix:
				for item in array:
					replacement.append(item)

			vertex.set_coordinates(replacement)

# returns the product of two matrices
def matMul(first, second):
	out = None
	# not all matrices can be multiplied
	if len(first[0]) == len(second):
		m = len(first)
		n = len(second[0])
		common = len(second)
		
		out = createZeroMat(m, n)
		
		for i in range(m):
			for j in range(n):
				for k in range(common):
					out[i][j] += first[i][k] * second[k][j]
	
	return out

# returns an empty matrix of size m*x	
def createZeroMat(m, n):
	out = [0] * m

	for i in range(m):
		out[i] = [0] * n

	return out

# make it look bigger or smaller by increasing or decreasing scale
def wheel(event):
	global scale
	scale = scale + (event.delta/120)
	draw_tet()

# increase or decrease the size of the tetrahedron
def resize(event):
	global height, width
	height = event.height
	width = event.width
	draw_tet()

def click(event):
	global prevX, prevY
	prevX = event.x
	prevY = event.y

def mouse_motion(event):
	global prevX, prevY
	dx = prevY - event.y
	theta = math.radians(dx)
	costheta = math.cos(theta)
	sintheta = math.sin(theta)
	z_rotation = [[costheta,(-1 * sintheta),0], [sintheta,costheta,0], [0,0,1]]
	rotateTetrahedron(z_rotation)

	dy = prevX - event.x
	theta = math.radians(dy)
	costheta = math.cos(theta)
	sintheta = math.sin(theta)
	y_rotation = [[costheta, 0, sintheta], [0, 1, 0], [-sintheta, 0, costheta]]
	rotateTetrahedron(y_rotation)
	draw_tet()
	click(event)

def right_mouse_motion(event):
	global prevZ
	# rotate the z-axis by using the y-rotation matrix
	dz = prevZ - event.x
	theta = math.radians(dz)
	costheta = math.cos(theta)
	sintheta = math.sin(theta)
	x_rotation = [[1,0,0], [0,costheta,(-1 * sintheta)], [0,sintheta,costheta]]
	rotateTetrahedron(x_rotation)
	draw_tet()

	prevZ = event.x
	click(event)

if len(sys.argv) > 1:
	height = 720
	width = 1280
	scale = 1
	top = Tk()
	c = Canvas(top, bg="white", height=height, width=width)
	c.pack(fill=BOTH, expand=YES)
	c.bind_all('<MouseWheel>', wheel)
	c.bind("<Configure>", resize)
	c.bind("<Button-1>", click)
	c.bind("<B1-Motion>", mouse_motion)
	c.bind("<Button-3>", right_mouse_motion)
	
	# the viewer is initially located at [-100, 0, 0]
	vp = [-100,0,0]
	col = [135,972,125]
	plane = [1,0,0,-1]
	nplane = [-300,0,0]
	prevY = 0
	prevX = 0
	prevZ = 0

	vertices = [[]]
	coordinates = [[]]
	edges = []
	get_input(sys.argv[1])
	get_edges()
	# print("The number of edges = " + str(len(edges)))
	vertices = get_vertices()
	faces = []
	get_faces()
	
	draw_tet()
	print("Rotate by the x and y axis by left-clicking and dragging")
	print("Rotate by the z axis by right-clicking and dragging")
	print("Use the mouse wheel to zoom in on the polyhedron")
	top.mainloop()
# first = [1, 2, 3, 4]
# second = [3, 4, 1, 2]
# print(list_equals(first, second))

# for i in range(0, 100):
	# print(randint(0, 2))