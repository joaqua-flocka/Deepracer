import math

class Reward:
    def __init__(self, verbose=False, track_time=False):
        self.next_waypoint = 1
        #self.prev_speed = 0
        
    def reward_function(self, params):
        waypoints = params['closest_waypoints']
        #speed = params['speed']
        reward = 0
        
        #if(speed > self.prev_speed):
            #reward += 3.0
        if(waypoints[0] == self.next_waypoint):
            self.next_waypoint = waypoints[1]
            reward += 15.0
        return reward

reward_object = Reward()

def reward_function(params):
    # Example of rewarding the agent to follow center line

    reward = .01 #initialize reward

    # Read input parameters
    track_width = params['track_width']
    distance_from_center = params['distance_from_center']
    on_track = params['all_wheels_on_track']
    abs_steering = abs(params['steering_angle'])
    speed = params['speed']

    # Calculate 3 markers that are at varying distances away from the center line
    marker_1 = 0.05 * track_width
    marker_2 = 0.1 * track_width
    marker_3 = 0.2 * track_width
    marker_4 = 0.3 * track_width
    marker_5 = 0.4 * track_width

    # Give higher reward if the car is closer to center line and vice versa
    if distance_from_center <= marker_1:
        reward = 5.0
    elif distance_from_center <= marker_2:
        reward = 4.0
    elif distance_from_center <= marker_3:
        reward = 3.0
    elif distance_from_center <= marker_4:
        reward = 2.0
    
    reward += reward_object.reward_function(params)
    
    if(speed < 4.7):
        reward *= .6
    if(speed >= 4.8):
        reward += speed * 4
    if(speed >= 5.0):
        reward += 35
    
    if(on_track == False): #penalize if off track
        reward *= .7
    ABS_STEERING_THRESHOLD = 20.0
    if abs_steering > ABS_STEERING_THRESHOLD: # penalize if turning too sharply
        reward *= 0.85
        
    waypoints = params['waypoints']
    closest_waypoints = params['closest_waypoints']
    heading = params['heading']

    # Initialize the reward with typical value

    # Calculate the direction of the center line based on the closest waypoints
    next_point = waypoints[closest_waypoints[1]]
    prev_point = waypoints[closest_waypoints[0]]

    # Calculate the direction in radius, arctan2(dy, dx), the result is (-pi, pi) in radians
    track_direction = math.atan2(next_point[1] - prev_point[1], next_point[0] - prev_point[0])
    # Convert to degree
    track_direction = math.degrees(track_direction)

    # Calculate the difference between the track direction and the heading direction of the car
    direction_diff = abs(track_direction - heading)
    if direction_diff > 180:
        direction_diff = 360 - direction_diff

    # Penalize the reward if the difference is too large
    DIRECTION_THRESHOLD = 8.0
    if direction_diff > DIRECTION_THRESHOLD:
        reward *= 0.5
    
    return float(reward)
