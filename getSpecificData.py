# Import mavutil
from pymavlink import mavutil

print("running...")
# Create the connection
master = mavutil.mavlink_connection(
    '/dev/serial0',
    baud=57600)



# Wait a heartbeat before sending commands
master.wait_heartbeat()

# Request parameter
master.mav.param_request_read_send(
    master.target_system, master.target_component,
    b'GPS_POS1_Y',
    -1
)

# Print parameter value
message = master.recv_match(type='PARAM_VALUE', blocking=True).to_dict()
print('name: %s\tvalue: %d' % (message['param_id'].decode("utf-8"), message['param_value']))
