import trimesh
import numpy as np

def simplify_scene_mesh(input_path, output_path, target_faces=10000):
    """简化场景mesh到指定面数"""
    
    print(f"加载文件: {input_path}")
    mesh = trimesh.load(input_path, force='mesh')
    
    print(f"原始mesh:")
    print(f"  - 顶点数: {len(mesh.vertices):,}")
    print(f"  - 面数: {len(mesh.faces):,}")
    print(f"  - 边界: {mesh.bounds}")
    
    # 先进行基本清理
    print("进行基本清理...")
    mesh.remove_duplicate_faces()
    mesh.remove_degenerate_faces() 
    mesh.merge_vertices()
    
    print(f"清理后mesh:")
    print(f"  - 顶点数: {len(mesh.vertices):,}")
    print(f"  - 面数: {len(mesh.faces):,}")
    
    # 目标简化
    if len(mesh.faces) > target_faces:
        ratio = target_faces / len(mesh.faces)
        print(f"需要简化到 {ratio:.4f} 的比例 (目标: {target_faces:,} 面)")
        
        # 尝试quadric decimation简化
        try:
            print("尝试quadric decimation简化...")
            simplified = mesh.simplify_quadric_decimation(target_faces)
            print(f"Quadric简化成功!")
        except Exception as e:
            print(f"Quadric方法失败: {e}")
            print("尝试其他简化方法...")
            
            try:
                # 尝试使用更激进的简化
                print("尝试vertex clustering...")
                # 对于极其复杂的mesh，使用vertex clustering
                voxel_size = np.max(mesh.extents) / 100  # 自动计算合适的voxel大小
                simplified = mesh.voxelized(pitch=voxel_size).marching_cubes
                print(f"Vertex clustering成功!")
            except Exception as e2:
                print(f"Vertex clustering也失败: {e2}")
                print("使用基本清理的结果...")
                simplified = mesh
    else:
        print("mesh已经足够简单，不需要简化")
        simplified = mesh
    
    print(f"最终简化后mesh:")
    print(f"  - 顶点数: {len(simplified.vertices):,}")
    print(f"  - 面数: {len(simplified.faces):,}")
    print(f"  - 边界: {simplified.bounds}")
    print(f"  - 简化比例: {len(simplified.faces)/len(mesh.faces):.4f}")
    
    # 保存简化后的mesh
    simplified.export(output_path)
    print(f"简化后的mesh保存到: {output_path}")
    
    return simplified

if __name__ == "__main__":
    input_file = "/home/user/Desktop/DART/egobody_mesh/processed_mesh/cab_g_benches/cab_g_benches_scene_with_floor.obj"
    output_file = "/home/user/Desktop/DART/egobody_mesh/processed_mesh/cab_g_benches/cab_g_benches_scene_with_floor_small.obj"
    
    print("开始简化复杂场景...")
    print("这可能需要几分钟时间，请耐心等待...")
    
    # 目标面数：5000面对于人体交互来说已经足够了
    target_faces = 200000
    
    try:
        simplified_mesh = simplify_scene_mesh(input_file, output_file, target_faces=target_faces)
        print("✅ 简化完成!")
        print(f"✅ 简化后文件已保存为: {output_file}")
        
    except Exception as e:
        print(f"❌ 简化过程出错: {e}")
        print("请检查输入文件是否正确")