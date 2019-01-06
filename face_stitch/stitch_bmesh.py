import bpy
import bmesh
import pickle

bpy.ops.object.delete(use_global=False)
bpy.ops.import_mesh.ply(filepath='/Users/Roshan/Documents/Academics/BTP/Blenders/face_stitch/backHead2.ply')
bpy.ops.import_mesh.ply(filepath='/Users/Roshan/Documents/Academics/BTP/Blenders/face_stitch/newBestMesh.ply')
bpy.ops.object.join()

# Get the active mesh
obj = bpy.context.editable_objects[0]
me = obj.data

bpy.ops.object.mode_set(mode="EDIT")
# Get a BMesh representation
bm = bmesh.from_edit_mesh(me)

bm.faces.active = None

with open('/Users/Roshan/Documents/Academics/BTP/Blenders/face_stitch/edge_loops', 'rb') as f:
     toBeSelected = pickle.load(f)
     
with open('/Users/Roshan/Documents/Academics/BTP/Blenders/face_stitch/border_verts', 'rb') as f:
     toBeSelectedVerts = pickle.load(f)

bm.verts.ensure_lookup_table()
bm.edges.ensure_lookup_table()

lst = []
# Modify the BMesh, can do anything here...
for v in bm.verts:
    v.select = False
    
for e in bm.edges:
    e.select = False
    
for index in toBeSelectedVerts:
    bm.verts[index].select = True
    
for index in toBeSelected:
    bm.edges[index].select = True

# Show the updates in the viewport
# and recalculate n-gon tessellation.
bmesh.update_edit_mesh(me, True)

bpy.ops.mesh.bridge_edge_loops()
bpy.ops.object.mode_set(mode="OBJECT")
bpy.ops.object.shade_smooth()