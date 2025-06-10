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
        input_obj_path: Input scene OBJ file path
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
    
    # # Check coordinate system and adjust floor height
    # vertices = mesh.vertices
    # y_range = vertices[:, 1].max() - vertices[:, 1].min()
    # z_range = vertices[:, 2].max() - vertices[:, 2].min()
    
    # if y_range > z_range:
    #     print("Detected y-up coordinate system, converting to z-up...")
    #     rotation = trimesh.transformations.rotation_matrix(np.radians(-90), [1, 0, 0])
    #     mesh.apply_transform(rotation)
    #     vertices = mesh.vertices
    
    # # Adjust floor height to z=0
    # floor_z = np.percentile(vertices[:, 2], 1)
    # translation = np.eye(4)
    # translation[2, 3] = -floor_z
    # mesh.apply_transform(translation)
    # print(f"Floor height adjusted to z=0, original floor height: {floor_z}")
    
    # Save adjusted scene
    # scene_path = os.path.join(output_dir, 'scene.obj')
    # mesh.export(scene_path)
    # print(f"Adjusted scene saved to: {scene_path}")
    
    # Create floor and merge with scene
    vertices = mesh.vertices
    bounds_min = vertices.min(axis=0)
    bounds_max = vertices.max(axis=0)
    margin = 0.5
    
    floor_vertices = np.array([
        [bounds_min[0]-margin, bounds_min[1]-margin, 0],
        [bounds_max[0]+margin, bounds_min[1]-margin, 0],
        [bounds_max[0]+margin, bounds_max[1]+margin, 0],
        [bounds_min[0]-margin, bounds_max[1]+margin, 0]
    ])
    floor_faces = np.array([[0, 1, 2], [0, 2, 3]])
    floor_mesh = trimesh.Trimesh(vertices=floor_vertices, faces=floor_faces)
    
    scene_with_floor = trimesh.util.concatenate([mesh, floor_mesh])
    scene_with_floor_path = os.path.join(output_dir, 'seminar_g110_scene_with_floor.obj')
    scene_with_floor.export(scene_with_floor_path)
    print(f"Scene with floor saved to: {scene_with_floor_path}")


def create_navigation_config(scene_info, output_path):
    """Create navigation configuration file, using scene information to set reasonable start and end points"""
    center = scene_info['center']
    bounds_min = scene_info['bounds_min']
    bounds_max = scene_info['bounds_max']
    
    # Calculate reasonable start and end points using scene info
    # Start point: near one end of the scene but slightly off center
    start_x = bounds_min[0] + (bounds_max[0] - bounds_min[0]) * 0.25
    start_y = center[1]
    start_z = 0.9  # Human standing height
    
    # End point: near the other end of the scene
    end_x = bounds_min[0] + (bounds_max[0] - bounds_min[0]) * 0.75
    end_y = center[1] + (bounds_max[1] - bounds_min[1]) * 0.3  # Slightly off center line
    end_z = 0.9
    
    # Create navigation configuration
    navigation_config = {
        "scene_dir": scene_info['output_dir'],
        "floor_height": 0.0,
        "interaction_name": "egobody_navigation",
        "interactions": [
            {
                "text_prompt": "walk*20",
                "init_joints": [
                    [start_x, start_y, start_z],
                    [start_x + 0.1, start_y, start_z],  # Right hip joint
                    [start_x - 0.1, start_y, start_z]   # Left hip joint
                ],
                "goal_joints": [[end_x, end_y, end_z]]
            }
        ]
    }
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Save navigation configuration
    with open(output_path, 'w') as f:
        json.dump(navigation_config, f, indent=2)
    
    print(f"Navigation configuration saved to: {output_path}")
    print(f"- Start point: [{start_x:.2f}, {start_y:.2f}, {start_z:.2f}]")
    print(f"- End point: [{end_x:.2f}, {end_y:.2f}, {end_z:.2f}]")
    
    return navigation_config

if __name__ == "__main__":
    # Input and output paths
    input_obj_path = '/home/user/Desktop/DART/egobody_mesh/original_mesh/cab_g_benches_fixed.obj'
    output_dir = '/home/user/Desktop/DART/egobody_mesh/processed_mesh/cab_g_benches/'
    # nav_config_path = '/home/user/Desktop/DART/data/optim_interaction/egobody_kitchen_navigation.json'
    
    # Generate SDF files
    generate_scene_sdf(input_obj_path, output_dir, size=256, mesh_scale=0.8)
    
    # Create navigation configuration file
    # create_navigation_config(scene_info, nav_config_path)
    
    print("\nProcessing complete! Ready to run DART...")
    print("You can run DART navigation generation with the following commands:")
    print("cd ~/Desktop/DART")
    print("source ./demos/egobody_scene.sh")