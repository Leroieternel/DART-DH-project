import os
import sys
import trimesh
import mesh2sdf
import numpy as np
import json
from pathlib import Path

def generate_scene_sdf(input_obj_path, output_dir, size=256, mesh_scale=0.8):
    """
    Generate scene SDF files following DART official code
    
    Parameters:
        input_obj_path: Input scene OBJ file path (could be scene with floor)
        output_dir: Output directory path
        size: SDF grid size
        mesh_scale: Mesh scaling factor
    """
    print(f"Processing scene: {input_obj_path}")
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Load original mesh
    mesh = trimesh.load(input_obj_path, force='mesh')
    print(f"Original mesh: {len(mesh.vertices)} vertices, {len(mesh.faces)} faces")
    
    
    # 2. Normalize mesh
    scene_with_floor = trimesh.load(input_obj_path, force='mesh')
    vertices = scene_with_floor.vertices
    bbmin = vertices.min(0)
    bbmax = vertices.max(0)
    center = (bbmin + bbmax) * 0.5
    scale = 2.0 * mesh_scale / (bbmax - bbmin).max()
    print(f"Center point: {center.tolist()}")
    print(f"Scale factor: {scale}")
    
    # 3. Apply normalization
    normalized_vertices = (vertices - center) * scale
    
    # 4. Compute SDF
    print(f"Starting SDF computation (size: {size})...")
    level = 1.0 / size
    sdf, fixed_mesh = mesh2sdf.compute(
        normalized_vertices, scene_with_floor.faces, 
        size=size, 
        fix=True,  # Fix mesh
        level=level, 
        return_mesh=True
    )
    print(f"SDF computation completed!")
    
    # 5. Restore mesh to original scale
    fixed_mesh.vertices = fixed_mesh.vertices / scale + center
    
    # 6. Save output files
    output_paths = {
        'obj': os.path.join(output_dir, "scene_sdf.obj"),
        'npy': os.path.join(output_dir, "scene_sdf.npy"),
        'json': os.path.join(output_dir, "scene_sdf.json")
    }
    
    # Save fixed mesh
    fixed_mesh.export(output_paths['obj'])
    print(f"Fixed mesh saved to: {output_paths['obj']}")
    
    # Save SDF data
    np.save(output_paths['npy'], sdf)
    print(f"SDF data saved to: {output_paths['npy']}")
    
    # Save SDF configuration
    with open(output_paths['json'], 'w') as f:
        json.dump({
            'center': center.tolist(),
            'scale': float(scale),
            'level': float(level),
            'size': size,
        }, f, indent=2)
    print(f"SDF configuration saved to: {output_paths['json']}")
    
    # 7. Validate output files
    print("\nValidating SDF data:")
    sdf_data = np.load(output_paths['npy'])
    print(f"SDF shape: {sdf_data.shape}")
    print(f"SDF value range: min {sdf_data.min():.4f}, max {sdf_data.max():.4f}")
    print(f"SDF negative values: {np.sum(sdf_data < 0)}, positive values: {np.sum(sdf_data > 0)}")


if __name__ == "__main__":
    # Input and output paths
    input_obj_path = '/home/user/Desktop/DART/egobody_mesh/processed_mesh/cab_g_benches/cab_g_benches_scene_with_floor_small.obj'
    output_dir = '/home/user/Desktop/DART/egobody_mesh/processed_mesh/cab_g_benches/'
    
    # Generate SDF files
    generate_scene_sdf(input_obj_path, output_dir, size=256, mesh_scale=0.8)
    
    print("\nProcessing complete!")