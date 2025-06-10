import trimesh
import numpy as np

def simplify_scene_mesh(input_path, output_path, target_faces=10000):
    
    print(f"Load mesh file: {input_path}")
    mesh = trimesh.load(input_path, force='mesh')
    
    print(f"Original mesh:")
    print(f"  - Vertices: {len(mesh.vertices):,}")
    print(f"  - Faces: {len(mesh.faces):,}")
    print(f"  - Bounds: {mesh.bounds}")
    
    mesh.remove_duplicate_faces()
    mesh.remove_degenerate_faces() 
    mesh.merge_vertices()
    
    print(f"Initially compressed mesh:")
    print(f"  - Vertices: {len(mesh.vertices):,}")
    print(f"  - Faces: {len(mesh.faces):,}")
    
    if len(mesh.faces) > target_faces:
        ratio = target_faces / len(mesh.faces)
        
        # quadric decimation
        try:
            print("Try quadric decimation compressing")
            simplified = mesh.simplify_quadric_decimation(target_faces)
            print(f"Quadric decimation succeed")
        except Exception as e:
            print(f"Quadric decimation failed: {e}")
            
            try:
                print("Try vertex clustering...")
                voxel_size = np.max(mesh.extents) / 100 
                simplified = mesh.voxelized(pitch=voxel_size).marching_cubes
                print(f"Vertex clustering succeed")
            except Exception as e2:
                print(f"Vertex clustering failed: {e2}")
                simplified = mesh
    else:
        print("No need to compress the scene mesh")
        simplified = mesh
    
    print(f"Compressed mesh:")
    print(f"  - Vertices: {len(simplified.vertices):,}")
    print(f"  - Faces: {len(simplified.faces):,}")
    print(f"  - Bounds: {simplified.bounds}")
    print(f"  - Ratio: {len(simplified.faces)/len(mesh.faces):.4f}")
    
    # save compressed mesh
    simplified.export(output_path)
    print(f"saved compressed mesh at: {output_path}")
    
    return simplified

if __name__ == "__main__":
    input_file = "/home/user/Desktop/DART/egobody_mesh/processed_mesh/cab_g_benches/cab_g_benches_scene_with_floor.obj"
    output_file = "/home/user/Desktop/DART/egobody_mesh/processed_mesh/cab_g_benches/cab_g_benches_scene_with_floor_small.obj"
    
    print("Starting compressing...")
    
    target_faces = 200000
    
    try:
        simplified_mesh = simplify_scene_mesh(input_file, output_file, target_faces=target_faces)
        print("Compressing done!")
        print(f"Compressed scene mesh is saved at: {output_file}")
        
    except Exception as e:
        print(f"Error: {e}")