#include <AccelStepper.h>

AccelStepper motor_x(AccelStepper::DRIVER, 2, 5); // Using motorX on CNC Shield V3: pin 2 = step, pin 5 = direction
AccelStepper motor_y(AccelStepper::DRIVER, 3, 6); // Using motorY on CNC Shield V3: pin 3 = step, pin 6 = direction

const byte enablePin = 8;

void setup()
{
   pinMode(enablePin, OUTPUT);
   digitalWrite(enablePin, LOW);

   // motor_x.setSpeed(500);
   motor_x.setMaxSpeed(5000);
   motor_x.setAcceleration(1000);
   motor_x.moveTo(2000);
   
   motor_y.setMaxSpeed(5000);
   motor_y.setAcceleration(1000);
   motor_y.moveTo(-50000);
}

void loop()
{
  // .run is non-blocking
  motor_x.run();
  motor_y.run();

  // Change direction at the limits
  if (motor_x.distanceToGo() == 0)
      motor_x.moveTo(-motor_x.currentPosition());
  
  // motor_x.runSpeed();

  // runToNewPosition is blocking
  // motor_x.runToNewPosit0ion(0);
  // motor_x.runToNewPosition(5000);
  // motor_x.runToNewPosition(100);
  // motor_x.runToNewPosition(120);
}
