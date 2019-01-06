import bpy
import pickle

#bpy.ops.object.delete(use_global=False)

#bpy.data.objects['Cube'].scale = (1.2, 0.5, 1.9)
'''bpy.ops.import_mesh.ply(filepath='/Users/Roshan/Documents/Academics/BTP/Blenders/face_stitch/backHead2.ply')
bpy.ops.import_mesh.ply(filepath='/Users/Roshan/Documents/Academics/BTP/Blenders/face_stitch/newBestMesh.ply')

bpy.ops.object.join()
bpy.ops.object.editmode_toggle()
bpy.ops.mesh.select_all(action='TOGGLE')

bpy.ops.mesh.bridge_edge_loops()
bpy.ops.object.shade_smooth()
'''
bpy.data.meshes['Cube'].vertices

lst = []
for i, vertex in enumerate(bpy.data.meshes['newBestMesh.001'].vertices):
    #print(i, vertex.select)
    if(vertex.select == True):
        lst.append(i)

print(len(lst))

with open('edge_loops', 'wb') as f:
     pickle.dump(lst, f)
