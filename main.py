import sensors
import wheels
#import PIDControls

while True:
    if True:
        if sensors.get_front() > 60:
            wheels.forward(0.6)
        else:
            wheels.stop()

    else:
        wheels.stop()
