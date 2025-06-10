# Synthesizing Interactive Human Behaviors
## VolDART: DART with VolumetricSMPL Collision Optimizer

### [[website](https://voldart-dh.github.io/)]


# Getting Started

## Environment Setup
Setup conda env:
```
conda env create -f environment.yml
conda activate DART
```
Tested system:

Our experiments and performance profiling are conducted on based on two setups: the first one is a single RTX 4090 with 24 GiB memory, the second one is a single RTX 5070Ti with 16 GiB memory.

## Data and Model Checkpoints
* Please download this [google drive link](https://drive.google.com/drive/folders/1vJg3GFVPT6kr6cA0HrQGmiAEBE2dkaps?usp=drive_link) containing model checkpoints and necessary data, extract and merge it to the project folder.

* Please download the following data from the respective websites and organize as shown below:
  * [SMPL-X body model](https://download.is.tue.mpg.de/download.php?domain=smplx&sfile=smplx_lockedhead_20230207.zip)
  * [SMPL-H body model](https://download.is.tue.mpg.de/download.php?domain=mano&resume=1&sfile=smplh.tar.xz)
  * [AMASS](https://amass.is.tue.mpg.de/) (Only required for training, please down the gender-specific data for SMPL-H and SMPL-X)
  * [BABEL](https://download.is.tue.mpg.de/download.php?domain=teach&resume=1&sfile=babel-data/babel-teach.zip) (Only required for training)
  * [HumanML3D](https://github.com/EricGuo5513/HumanML3D)(Only required for training)

  
  * <details>

    <summary><b>Project folder structure of separately downloaded data:</b></summary>

    ```
      ./
      ├── data
      │   ├── smplx_lockedhead_20230207
      │   │   └── models_lockedhead
      │   │       ├── smplh
      │   │       │   ├── SMPLH_FEMALE.pkl
      │   │       │   └── SMPLH_MALE.pkl
      │   │       └── smplx
      │   │           ├── SMPLX_FEMALE.npz
      │   │           ├── SMPLX_MALE.npz
      │   │           └── SMPLX_NEUTRAL.npz
      │   ├── amass
      │   │   ├──  babel-teach
      │   │   │        ├── train.json
      │   │   │        └── val.json
      │   │   ├──  smplh_g
      │   │   │        ├── ACCAD
      │   │   │        ├── BioMotionLab_NTroje
      │   │   │        ├── BMLhandball
      │   │   │        ├── BMLmovi
      │   │   │        ├── CMU
      │   │   │        ├── CNRS
      │   │   │        ├── DanceDB
      │   │   │        ├── DFaust_67
      │   │   │        ├── EKUT
      │   │   │        ├── Eyes_Japan_Dataset
      │   │   │        ├── GRAB
      │   │   │        ├── HUMAN4D
      │   │   │        ├── HumanEva
      │   │   │        ├── KIT
      │   │   │        ├── MPI_HDM05
      │   │   │        ├── MPI_Limits
      │   │   │        ├── MPI_mosh
      │   │   │        ├── SFU
      │   │   │        ├── SOMA
      │   │   │        ├── SSM_synced
      │   │   │        ├── TCD_handMocap
      │   │   │        ├── TotalCapture
      │   │   │        ├── Transitions_mocap
      │   │   │        └── WEIZMANN
      │   │   └──  smplx_g
      │   │   │        ├── ACCAD
      │   │   │        ├── BMLmovi
      │   │   │        ├── BMLrub
      │   │   │        ├── CMU
      │   │   │        ├── CNRS
      │   │   │        ├── DanceDB
      │   │   │        ├── DFaust
      │   │   │        ├── EKUT
      │   │   │        ├── EyesJapanDataset
      │   │   │        ├── GRAB
      │   │   │        ├── HDM05
      │   │   │        ├── HUMAN4D
      │   │   │        ├── HumanEva
      │   │   │        ├── KIT
      │   │   │        ├── MoSh
      │   │   │        ├── PosePrior
      │   │   │        ├── SFU
      │   │   │        ├── SOMA
      │   │   │        ├── SSM
      │   │   │        ├── TCDHands
      │   │   │        ├── TotalCapture
      │   │   │        ├── Transitions
      │   │   │        └── WEIZMANN
      │   ├── HumanML3D
      │   │   ├── HumanML3D
      │   │   │   ├──...
      │   │   └── index.csv
    ```
    </details>


## Visualization 

### Pyrender Viewer
* We use `pyrender` for interactive visualization of generated motions by default. Please refer to [pyrender viewer](https://pyrender.readthedocs.io/en/latest/generated/pyrender.viewer.Viewer.html) for the usage of the interactive viewer, such as rotating, panning, and zooming.
* The [visualization script](./visualize/vis_seq.py) can render a generated sequence by specifying the `seq_path` argument. It also supports several optional functions, such as multi-sequence visualization, interactive play with frame forward/backward control using keyboards, and automatic body-following camera. More details of the configurable arguments can be found in the [vis script](https://github.com/zkf1997/DART/blob/7c1c922ae08f98b507eb7bdcc2e8029ed82e3b64/visualize/vis_seq.py#L375).
* The script can be slow when visualizing multiple humans together. You can choose to visualize only one human at a time by setting `--max_seq 1` in the command line, or use the blender visualization described below which is several times more efficient.

### Blender Visualization
* We also support exporting the generated motions as `npz` files and visualize in [Blender](https://www.blender.org/) for advanced rendering. To import one motion sequence into blender, please first install the [SMPL-X Blender Add-on](https://gitlab.tuebingen.mpg.de/jtesch/smplx_blender_addon#installation), and use the "add animation" feature as shown in this video. You can use the space key to start/stop playing animation in Blender.
 
  
  <details>

   <summary><b>Demonstration of importing motion into Blender:</b></summary>

    https://github.com/user-attachments/assets/a15fc9d6-507e-4521-aa3f-64b2db8c0252

  </details>

# Egobody Scene Mesh
* Please download this [google drive link](https://drive.google.com/drive/folders/1vJg3GFVPT6kr6cA0HrQGmiAEBE2dkaps?usp=drive_link) containing the EgoBody scene mesh in .obj format, then extract and merge it to the project folder `./DART/scene_mesh`.

# Scene Mesh Pre-processing
## Scene mesh compressing
If the original scene with floor mesh is too big, we provide a script that can effectively compress the scene mesh using quadratic decimation. For running the script, please use
```
python compress_scene.py
```
## Calculate scene sdf
We provide a script (adapted from the original dart) that can compute the scene sdf for the previous compressed scene with floor. For running the script, please use
```
python generate_sdf.py
```


## Human-Scene Interaction Synthesis
We provide multiple optimizer scripts for different tasks.

Given an input 3D scene and the text prompts specifying the actions and durations, we control the human to reach the goal joint location starting from an initial pose while adhering to the scene contact and collision constraints.
We show two examples of climbing downstairs and sitting to a chair in the demo below:
```
source ./demos/scene.sh
```
The generated sequences can be visualized using:
```
python -m visualize.vis_seq --add_floor 0 --seq_path './mld_denoiser/mld_fps_clip_repeat_euler/checkpoint_300000/optim/sit_use_pred_joints_ddim10_guidance5.0_seed0_contact0.1_thresh0.0_collision0.1_jerk0.1/sample_*.pkl'
```
```
python -m visualize.vis_seq --add_floor 0 --seq_path './mld_denoiser/mld_fps_clip_repeat_euler/checkpoint_300000/optim/climb_down_use_pred_joints_ddim10_guidance5.0_seed0_contact0.1_thresh0.0_collision0.1_jerk0.1/sample_*.pkl'
```

If you would like to use a Egobody scene, run the demo
```
source ./demos/egobody_scene.sh
```

Finally, to try out the high five optimizer, utilize the following demo.
```
source ./demos/run_high_five.sh
```


Our ball interaction optimizer can be run with
```
python -m mld.optim_scene_mld_ball_dart --denoiser_checkpoint './mld_denoiser/mld_fps_clip_repeat_euler/checkpoint_300000.pt' --interaction_cfg "data/optim_interaction/bouncing_ball_navigation.json" --optim_lr 0.01 --optim_steps 100 --batch_size 1 --guidance_param 5 --respacing "ddim10" --export_smpl 1  --use_predicted_joints 1  --optim_unit_grad 1  --optim_anneal_lr 1  --weight_jerk 0.1 --weight_collision 0.1  --weight_contact 0.1  --weight_skate 0.0  --contact_thresh 0.00  --load_cache 0  --init_noise_scale 0.1
```

The respective python files, used for improving upon DART's original optimizer can be found in the folder `mld` as the files `optim_scene_mld.py`, `optim_scene_mld_ball_dart.py`, `optim_scene_mld_dart_final.py` and `optim_scene_mld_volsmpl_ball.py`

To use a custom 3D scene, you need to first calculate the scene SDF for evaluating human-scene collision and contact constraints.
Please ensure the 3D scene is z-up and the floor plane has zero height.
We use [mesh2sdf](https://github.com/wang-ps/mesh2sdf) for SDF calculation, as shown in [this script](./scenes/test_sdf.py).
Example configuration files for an interaction sequence can be found [here](./data/optim_interaction). We currently initialize the human using a standing pose, with its location and orientation determined by the pelvis, left hip and right hip location specified using `init_joints`.
The goal joint locations are specified using `goal_joints`. The current [script](./mld/optim_scene_mld.py) only use pelvis as the goal joint, you can modify the goal joints to be another joint or multiple joints.
You may also tune the optimization parameters to modulate the generation, such as increasing the learning rate to obtain more diverse results, adjusting number of optimization steps to balance quality and speed, and adjusting the loss weights. 


[//]: # (## Sparse and Dense Joint locations Control)


# Acknowledgements
Our code is built upon many prior projects, including but not limited to:

[DNO](https://github.com/korrawe/Diffusion-Noise-Optimization), [MDM](https://github.com/GuyTevet/motion-diffusion-model), [MLD](https://github.com/ChenFengYe/motion-latent-diffusion), [FlowMDM](https://github.com/BarqueroGerman/FlowMDM), [text-to-motion](https://github.com/EricGuo5513/text-to-motion), [guided-diffusion](https://github.com/openai/guided-diffusion), [ACTOR](https://github.com/Mathux/ACTOR), [DIMOS](https://github.com/zkf1997/DIMOS)

[//]: # (# License)

[//]: # (* Our code and model checkpoints employ the MIT License.)

[//]: # (* Note that our code depends on third-party software and datasets that employ their respective licenses. Here are some examples:)

[//]: # (    * Code/model/data relevant to the SMPL-X body model follows its own license.)

[//]: # (    * Code/model/data relevant to the AMASS dataset follows its own license.)

[//]: # (    * Blender and its SMPL-X add-on employ their respective license.)

  

# Contact

If you run into any problems or have any questions, feel free to contact [Xiangyi Jia](mailto:jiaxia@student.ethz.ch) or create an issue.
