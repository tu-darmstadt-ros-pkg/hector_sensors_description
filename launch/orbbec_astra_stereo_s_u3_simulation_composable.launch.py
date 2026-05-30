from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import LoadComposableNodes
from launch_ros.descriptions import ComposableNode
from tf_transformations import quaternion_from_euler

# Note that the container needs to be created before the composable node of this launch file can be created.


def generate_launch_description():
    camera_name = LaunchConfiguration("camera_name")
    container_name = LaunchConfiguration("container_name")

    # Define the transforms using list concatenation for substitutions
    transforms = [
        {
            "x": 0.0,
            "y": 0.0,
            "z": 0.0,
            "roll": 0.0,
            "pitch": 0.0,
            "yaw": 0.0,
            "parent": "_link",
            "child": "_depth_frame",
        },
        {
            "x": 0.0,
            "y": 0.0,
            "z": 0.0,
            "roll": -1.5708,
            "pitch": 0.0,
            "yaw": -1.5708,
            "parent": "_depth_frame",
            "child": "_depth_optical_frame",
        },
        {
            "x": 0.0,
            "y": -0.01,
            "z": 0.0,
            "roll": 0.0,
            "pitch": 0.0,
            "yaw": 0.0,
            "parent": "_depth_frame",
            "child": "_color_frame",
        },
        {
            "x": 0.0,
            "y": 0.0,
            "z": 0.0,
            "roll": -1.5708,
            "pitch": 0.0,
            "yaw": -1.5708,
            "parent": "_color_frame",
            "child": "_color_optical_frame",
        },
    ]

    composable_nodes = []
    for tf in transforms:
        q = quaternion_from_euler(tf["roll"], tf["pitch"], tf["yaw"])

        composable_nodes.append(
            ComposableNode(
                package="tf2_ros",
                plugin="tf2_ros::StaticTransformBroadcasterNode",
                name=[camera_name, tf["parent"], "_to_", camera_name, tf["child"]],
                parameters=[
                    {
                        "translation.x": tf["x"],
                        "translation.y": tf["y"],
                        "translation.z": tf["z"],
                        "rotation.x": q[0],
                        "rotation.y": q[1],
                        "rotation.z": q[2],
                        "rotation.w": q[3],
                        "frame_id": [camera_name, tf["parent"]],
                        "child_frame_id": [camera_name, tf["child"]],
                    }
                ],
                remappings=[("/tf_static", "tf_static")],
            )
        )

    return LaunchDescription(
        [
            DeclareLaunchArgument(
                "camera_name", default_value="orbbec_astra_stereo_s_u3"
            ),
            DeclareLaunchArgument(
                "container_name", default_value="static_tf_publisher_container"
            ),
            LoadComposableNodes(
                target_container=[container_name],
                composable_node_descriptions=composable_nodes,
            ),
        ]
    )
