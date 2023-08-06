(*) DiffBot RosGymBullet instruction:
-----------------------------------------------------------------------------------------------
- reset(): state constructor, returns the corresponding observation for each initialized state;
- step(): action selection function, considered as input vsf used for the environment, instructing the kernel to act in the environment to go to the new state.
This function returns 4 values:
    +) observation: corresponds to the current state;
    +) reward: the reward received from interacting with the environment when performing an action;
    +) done: when the state limit is reached, if True, the simulation ends, False resets the simulation;
    +) info: a dictionary that returns additional information about the returned environment.
- render(): display simulation window of Gym environment;
- close(): close the simulation window.