import os
import pybullet as p
import time
import pybullet_data
import numpy as np
import math
import threading
import copy
import matplotlib.pyplot as plt
from modern_robotics import *
import numpy.linalg as lin

physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
planeID = p.loadURDF("plane.urdf")

TFID1 = p.loadURDF("C:/Users/whj03/Desktop/admittance/urdf/TFtest.urdf", [0, 0, 0.0])
boxID = p.loadURDF("C:/Users/whj03/Desktop/admittance/urdf/box.urdf", [0, 0, 0.65])
p.setGravity(0, 0, 0)
p.setTimeStep(1/240.)
time_step = 1/240.
p.resetDebugVisualizerCamera(cameraDistance=2, cameraYaw=0.0, cameraPitch=-5, cameraTargetPosition=[0.0, 0, 0.5])

Orientation = p.getQuaternionFromEuler([0, -3.14, 0])
arrowID = p.loadURDF("C:/Users/whj03/Desktop/admittance/urdf/abc.urdf", [0, -0.5, 2],Orientation)
cid = p.createConstraint(TFID1, 0, boxID, -1, p.JOINT_FIXED, [0, 0, 0.0], [0, 0, 0.65], [0, 0, 0])
p.changeConstraint(cid, maxForce=100)

if __name__ == "__main__":
	joint_list = [0];
	joint_states = [0];
	count = 0;
	wrench_list = []

	p.enableJointForceTorqueSensor(TFID1, 0)

	t = 0;
	t_list = [];
	for i in range(55):
		'''
		pos2 = np.array(p.getLinkState(boxID, 0, 1)[0])
		orn2 = np.array(p.getLinkState(boxID, 0, 1, 1)[1])
		Orientation = p.getQuaternionFromEuler([0, -3.14, 0])
		print(np.array(p.getLinkState(boxID, 1, 1, 1)[0]))
		position = [pos2[0], pos2[1], pos2[2] + 100]
		'''
		#if count >= 50 and count < 53:
		#	position = [0.3, -0.5, 1.31]
		#else:
		#	position = [0.5, 0.5, 1.3 + 1.6]
		#p.resetBasePositionAndOrientation(arrowID, position, Orientation)

		if count == 50:
			p.applyExternalForce(boxID, -1,  [0.0, 10.0, 10.0], [0.5, 0.5, 1.3], p.WORLD_FRAME)

		wrench = np.array(p.getJointState(cid , 0)[2])
		wrench2 = wrench
		wrench_list.append(wrench2)

		a = p.getContactPoints(boxID, -1)

		print(a)

		estimation_pos_x = [(wrench2[5]/wrench2[0]), -(wrench2[4]/wrench2[0])]
		estimation_pos_y = [(wrench2[5] / wrench2[1]), -(wrench2[3] / wrench2[1])]
		estimation_pos_z = [(wrench2[4] / wrench2[2]), -(wrench2[3] / wrench2[2])]

		print(count)

		print('moment ', np.array([wrench2[3], wrench2[4], wrench2[5]]))
		print('FORCE ', np.array([wrench2[0], wrench2[1], wrench2[2]]))

		#if count == 51:
		print('(y,z)', estimation_pos_x)
		print('(x,z)', estimation_pos_y)
		print('(x,y)', estimation_pos_z)

		t = t + time_step
		t_list.append(t)
		count = count + 1;
		p.stepSimulation();
		time.sleep(time_step)


list_size = len(wrench_list)
fig = plt.figure(figsize=(10, 7))
#X =np.arange(t_list)
ax = fig.add_subplot(221)
plt.plot(t_list, np.array([elem[3] for elem in wrench_list]), label='fx')
plt.plot(t_list, np.array([elem[4] for elem in wrench_list]), label='fy')
plt.plot(t_list, np.array([elem[5] for elem in wrench_list]), label='fz')
plt.ylim([-500, 300])
plt.xlabel('time[s]')
plt.ylabel('[N]')

plt.title("measured force/torque")

'''
list_size_1 = len(pos_list)
ay = fig.add_subplot(222)
plt.plot(t_list, np.array([pos_list[3] for pos_list in pos_list]), label='pos_x')
plt.plot(t_list, np.array([pos_list[4] for pos_list in pos_list]), label='pos_y')
plt.plot(t_list, np.array([pos_list[5] for pos_list in pos_list]), label='pos_z')
plt.xlabel('time[s]')
plt.ylabel('[m]')
plt.ylim([-0.1, 0.15])
plt.title("measured position")

plt.legend()
plt.show()
'''
