total_robots = 5
robots_list = []

for i in range(total_robots):
    print(i)
    robots = {'robot' : i+1 , 'Robot_tag' : None, 'status' : "Unplanned"}
    robots_list.append(robots)

print(robots_list[2])

print(robots_list[2].get('robot'))
robots_list[2]['Target'] = (45,13)
print(robots_list[2])

del robots_list[2]['Target']
print(robots_list[2])
# print(robots_list[2].get('Target'))

robots_list[4]['status'] = "Planned"

# #print(robots)

for i in range(total_robots):
    robot = robots_list[i]

    if robot.get('status') == "Planned":
        print(robot)
        break
