-- Port of the robot-side 2D mapping parameters into stock cartographer_ros.
--
-- Unsupported custom keys from the robot fork are kept as comments only:
--   revert_scan, submap_pub_debug, laser_angle_max/min,
--   POSE_GRAPH.constraint_builder.buildmap_mode
--
-- TF note (PC bag replay):
--   On the real robot: published_frame="odom", provide_odom_frame=false,
--   because the chassis already publishes odom->base_footprint on /tf.
--   On PC we do NOT replay /tf (it contains map->odom and would conflict),
--   so Cartographer must publish map->odom->base_footprint itself.

include "map_builder.lua"
include "trajectory_builder.lua"

options = {
  map_builder = MAP_BUILDER,
  trajectory_builder = TRAJECTORY_BUILDER,
  map_frame = "map",
  tracking_frame = "base_footprint",
  published_frame = "base_footprint",
  odom_frame = "odom",
  provide_odom_frame = true,
  publish_frame_projected_to_2d = true,
  use_pose_extrapolator = true,
  use_odometry = true,
  use_nav_sat = false,
  use_landmarks = false,
  num_laser_scans = 1,
  num_multi_echo_laser_scans = 0,
  num_subdivisions_per_laser_scan = 1,
  num_point_clouds = 0,
  lookup_transform_timeout_sec = 0.4,
  submap_publish_period_sec = 0.3,
  pose_publish_period_sec = 0.05,
  trajectory_publish_period_sec = 30e-3,
  rangefinder_sampling_ratio = 1.,
  odometry_sampling_ratio = 1.,
  fixed_frame_pose_sampling_ratio = 1.,
  imu_sampling_ratio = 1.,
  landmarks_sampling_ratio = 1.,
  -- revert_scan = false,          
  -- submap_pub_debug = false,    
  -- laser_angle_max = 1.8,        
  -- laser_angle_min = -1.8,      
}

MAP_BUILDER.use_trajectory_builder_2d = true

TRAJECTORY_BUILDER_2D.submaps.num_range_data = 50
TRAJECTORY_BUILDER_2D.min_range = 0.1
TRAJECTORY_BUILDER_2D.max_range = 25.
TRAJECTORY_BUILDER_2D.missing_data_ray_length = 10.
TRAJECTORY_BUILDER_2D.use_imu_data = false
TRAJECTORY_BUILDER_2D.use_online_correlative_scan_matching = true
TRAJECTORY_BUILDER_2D.motion_filter.max_angle_radians = math.rad(5.)
TRAJECTORY_BUILDER_2D.ceres_scan_matcher.occupied_space_weight = 100.
TRAJECTORY_BUILDER_2D.ceres_scan_matcher.translation_weight = 20.
TRAJECTORY_BUILDER_2D.ceres_scan_matcher.rotation_weight = 20.
TRAJECTORY_BUILDER_2D.submaps.grid_options_2d.resolution = 0.05

POSE_GRAPH.optimize_every_n_nodes = 20
POSE_GRAPH.constraint_builder.log_matches = false
POSE_GRAPH.constraint_builder.min_score = 0.5
POSE_GRAPH.constraint_builder.global_localization_min_score = 0.65
POSE_GRAPH.constraint_builder.max_constraint_distance = 20.
-- POSE_GRAPH.constraint_builder.buildmap_mode = "build"  -- robot-fork only

return options
