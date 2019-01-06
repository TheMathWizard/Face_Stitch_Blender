# This example assumes we have a mesh object in edit-mode

import bpy
import bmesh
import pickle

def wrt_base(mesh_index):
    print(mesh_index)

    # Get the active mesh
    obj = bpy.context.editable_objects[mesh_index]
    me = obj.data


    bpy.ops.object.editmode_toggle()
    # Get a BMesh representation
    bm = bmesh.from_edit_mesh(me)

    bm.faces.active = None


    maxx = minx = bm.verts[0].co.x 
    maxy = miny = bm.verts[0].co.y
    maxz = minz = bm.verts[0].co.z

    # Modify the BMesh, can do anything here...
    for v in bm.verts:
        if(v.co.x > maxx):
            maxx = v.co.x
        elif(v.co.x < minx):
            minx = v.co.x
        if(v.co.y > maxy):
            maxy = v.co.y
        elif(v.co.y < miny):
            miny = v.co.y
        if(v.co.z > maxz):
            maxz = v.co.z
        elif(v.co.z < minz):
            minz = v.co.z
            
    res = (maxx, minx, maxy, miny, maxz, minz)
    rx = maxx-minx
    ry = maxy-miny
    rz = maxz-minz
     
    with open('/Users/Roshan/Documents/Academics/BTP/Blenders/face_stitch/base_stats', 'rb') as fp:
        base = pickle.load(fp)
        
    bmaxx, bminx, bmaxy, bminy, bmaxz, bminz = base
    brx = bmaxx-bminx
    bry = bmaxy-bminy
    brz = bmaxz-bminz

    print(rx, brx)
    print(ry, bry)
    print(rz, brz)

    sx = rx/brx
    sy = ry/bry
    sz = (sx+sy)/2

    print(sx, sy, sz)
    
    return (sx, sy, sz)

    # Show the updates in the viewport
    # and recalculate n-gon tessellation.
    bmesh.update_edit_mesh(me, True)

if __name__ == '__main__':
    wrt_base(0)