import numpy as np

mesh = open("baseFace.ply", "r+")
lines = mesh.readlines()

class Vertex:
	def __init__(self, index, props):
		self.index = index
		self.props = props
		self.edges = []

	def add_edge(self, edge):
		self.edges.append(edge)

	def getLocation(self):
		return np.array(self.props[:3])

class Edge:
	def __init__(self, name):
		self.name = name
		self.v1_idx = int(name[:name.find(':')])
		self.v2_idx = int(name[name.find(':')+1:])
		verts[self.v1_idx].add_edge(self)
		verts[self.v2_idx].add_edge(self)
		self.faces = []

	def add_face(self, face):
		self.faces.append(face)

	def is_boundary(self):
		return (len(self.faces)==1)

	def retrieve_other_vert(self, vert):
		if(vert.index == self.v1_idx):
			return verts[self.v2_idx]
		elif(vert.index == self.v2_idx):
			return verts[self.v1_idx]


class Face:
	def __init__(self, index, vertices):
		self.index = index
		self.vert_indices = vertices


verts = {} #by index
edges = {} #by vertices - v1:v2
faces = {} #by index-
n_verts = 0
n_faces = 0
props = []
vert_begins = False
vert_index = 0
face_begins = False
face_index = 0


for line in lines:
	if("element vertex" in line):
		n_verts = int(line.split(' ')[2])
		print(n_verts)
		continue
	if("property" in line):
		props.append((line.split(' ')[1], line.split(' ')[2]))
		continue
	if("element face" in line):
		n_faces = int(line.split(' ')[2])
		continue
	if("end_header" in line):
		vert_begins = True
		continue
	if(vert_begins):
		verts[vert_index] = Vertex(vert_index, list(map(float, line.split(' '))))
		vert_index += 1
		print(vert_index)
		if(vert_index==n_verts):
			vert_begins = False
			face_begins = True
		continue
	if(face_begins):
		face_l = line.split(' ')[1:1+int(line.split(' ')[0])]
		face = Face(face_index, list(map(int, face_l)))
		faces[face_index] = face
		if(face_l[0]+":"+face_l[1] in edges):
			edges[face_l[0]+":"+face_l[1]].add_face(face)
		elif(face_l[1]+":"+face_l[0] in edges):
			edges[face_l[1]+":"+face_l[0]].add_face(face)
		else:
			edge = Edge(face_l[0]+":"+face_l[1])
			edge.add_face(face)
			edges[face_l[0]+":"+face_l[1]] = edge
		if(face_l[1]+":"+face_l[2] in edges):
			edges[face_l[1]+":"+face_l[2]].add_face(face)
		elif(face_l[2]+":"+face_l[1] in edges):
			edges[face_l[2]+":"+face_l[1]].add_face(face)
		else:
			edge = Edge(face_l[1]+":"+face_l[2])
			edge.add_face(face)
			edges[face_l[1]+":"+face_l[2]] = edge
		if(face_l[2]+":"+face_l[0] in edges):
			edges[face_l[2]+":"+face_l[0]].add_face(face)
		elif(face_l[0]+":"+face_l[2] in edges):
			edges[face_l[0]+":"+face_l[2]].add_face(face)
		else:
			edge = Edge(face_l[2]+":"+face_l[0])
			edge.add_face(face)
			edges[face_l[2]+":"+face_l[0]] = edge

		face_index += 1
		if(face_index==n_faces):
			face_begins = False

print(len(verts), len(faces), len(edges))

border_edges = {}
border_verts = {}
border_gradient = {}

for edge in edges:
	if(edges[edge].is_boundary()):
		border_edges[edge] = edges[edge]
		if(edges[edge].v1_idx not in border_verts):
			border_verts[edges[edge].v1_idx] = verts[edges[edge].v1_idx]
		if(edges[edge].v2_idx not in border_verts):
			border_verts[edges[edge].v2_idx] = verts[edges[edge].v2_idx]

for vert in border_verts:
	for edge in border_verts[vert].edges:
		grad = np.array((0,0,0), dtype='float64')
		if(edge.name not in border_edges):
			if(edge.v1_idx==vert):
				grad += verts[edge.v1_idx].getLocation() - verts[edge.v2_idx].getLocation()
			elif(edge.v2_idx==vert):
				grad += verts[edge.v2_idx].getLocation() - verts[edge.v1_idx].getLocation()
		norm = np.linalg.norm(grad)
		print(norm)
		grad = grad / norm
		border_gradient[vert] = grad

currentVerts = len(verts)

for vert in border_gradient:
	props = np.append(border_gradient[vert], np.array((255, 255, 255, 255), dtype='float64')).tolist()
	new_id = len(verts)
	verts[new_id] = Vertex(new_id, props)
	edges[str(new_id)+':'+str(vert)] = Edge(str(new_id)+':'+str(vert))



# Create Faces

done_edges = {}
for edge in border_edges:
	v1 = verts[border_edges[edge].v1_idx]
	for vert_edge in v1.edges:
		if(vert_edge.retrieve_other_vert(v1).index >= currentVerts):
			e1 = vert_edge
			v_next1 = vert_edge.retrieve_other_vert(v1)

	v2 = verts[border_edges[edge].v2_idx]
	for vert_edge in v2.edges:
		if(vert_edge.retrieve_other_vert(v2).index >= currentVerts):
			e2 = vert_edge
			v_next2 = vert_edge.retrieve_other_vert(v2)

	new_edge_name = str(v_next1.index)+':'+str(v_next2.index)
	edges[new_edge_name] = Edge(new_edge_name)

	e3 = border_edges[edge]
	e4 = edges[new_edge_name]

	face = Face(len(faces), (v1.index, v2.index, v_next2.index, v_next1.index))
	faces[len(faces)] = face

	e1.add_face(face)
	e2.add_face(face)
	e3.add_face(face)
	e4.add_face(face)


# Write to ply
f = open("face2.ply", "w+")
f.write('ply\n')
f.write('format ascii 1.0\n')
f.write('comment created by Parth \n')
f.write('element vertex '+str(len(verts))+'\n')
f.write('property float x\n')
f.write('property float y\n')
f.write('property float z\n')
f.write('property uchar red\n')
f.write('property uchar green\n')
f.write('property uchar blue\n')
f.write('property uchar alpha\n')
f.write('element face '+str(len(faces))+'\n')
f.write('property list uchar int vertex_indices\n')
f.write('end_header\n')

for vert in verts:
	f.write(' '.join(list(map(str, verts[vert].props[:3]))) +' ' + ' '.join(list(map(str, list(map(int, verts[vert].props[3:])))))+'\n')

for face in faces:
	indices = faces[face].vert_indices
	f.write(str(len(indices))+' '+' '.join(list(map(str, indices)))+'\n')

f.close()





		




