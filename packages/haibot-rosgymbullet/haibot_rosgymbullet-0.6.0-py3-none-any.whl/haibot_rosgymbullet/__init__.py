from gym.envs.registration import register
register(
    id='HaIBotEnv-v6.0', 
    entry_point='haibot_rosgymbullet.envs:DiffBotDrivingEnv'
)