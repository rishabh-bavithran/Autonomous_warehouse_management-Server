
# objects_status = ["Picked" "Picked" "Picked" "Unpicked" "Unpicked" "Picked" "Unpicked"]

# object_unpicked_indices = [o for o, x in enumerate(objects_status) if x == "Unpicked"]

# print(object_unpicked_indices)
robots_status = ["NR", "Ready", "NR", "NR" ,"Ready"]
robot_ready_index = robots_status.index("Ready")
print(robot_ready_index)
