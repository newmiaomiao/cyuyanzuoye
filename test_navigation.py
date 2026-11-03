
# -*- coding: utf-8 -*-
import time
from naoqi import ALProxy
import math

ROBOT_IP = "10.4.61.64"
PORT = 9559

# 已标记的三个导航点
POINTS = [
    ("Laboratory", -1.07132887840271, 1.7643171548843384),
    ("Entrance", -1.9958480596542358, 3.31475830078125),
    ("Stairs", -2.3443186283111572, 4.20186710357666)
]


def main():
    navigation = ALProxy("ALNavigation", ROBOT_IP, PORT)
    motion = ALProxy("ALMotion", ROBOT_IP, PORT)

    # 停止自主关注，避免与导航底盘控制冲突
    awareness = ALProxy("ALBasicAwareness", ROBOT_IP, PORT)
    awareness.stopAwareness()
    navigation.stopLocalization()
    # 唤醒机器人
    motion.wakeUp()
    path = "/home/nao/.local/share/Explorer/2014-04-04T014047.973Z.explo" #path of the map (previously made) - Paste your path here
    navigation.loadExploration(path) #loads the map
    navigation.startLocalization()
    navigation.getMetricalMap()
    navigation.relocalizeInMap([0, 0, 0])

    # 检查地图定位是否有效
    try:
        position = navigation.getRobotPositionInMap()[0]
        print("Current position:", position)
    except Exception as e:
        print("Localization unavailable:", e)
        print("Please load the map and localize first.")
        return

    # 逐个导航
    try:
        for name, x, y in POINTS:
            print("\nNext target:", name)
            print("Target position:", x, y)

            # 人工确认后再开始
            command = raw_input(
                "Press Enter to navigate, or q to quit: "
            )

            if command.lower() == "q":
                break

            # 地图坐标导航
            navigation.startLocalization()
            result = navigation.navigateToInMap([float(x), float(y), 0.0])
            time.sleep(2)
            print("Navigation result:", result)

            if result != 0:
                print("Navigation returned code:", result)
                break

            # 读取到达位置
            current = navigation.getRobotPositionInMap()[0]
            print("Current position:", current)
            dx = current[0] - x
            dy = current[1] - y
            distance = math.sqrt(dx * dx + dy * dy)
            print("Distance to target: %.3f m" % distance)
            error = math.sqrt(dx * dx + dy * dy)
            print("Position error: %.3f m" % error)

    except KeyboardInterrupt:
        print("Navigation interrupted by user.")

    except Exception as e:
        print("Navigation error:", e)

    finally:
        motion.stopMove()
        print("Movement stopped.")


if __name__ == "__main__":
    main()
