
#define USE_TIMER_1  true  // needs to go before #include "TimerInterrupt.h"

#include "TimerInterrupt.h"

// Pin 2 connected to the Rele.
#define RELE_PIN 2

// Output pin of the Infrared sensor into pin 4 of the Arduino
#define IR_SENSOR 4

// identifiers of the different actions that can be requested to this arduino
#define DROP_KIT '0'
#define ACTION_FINISHED_WITH_SUCCESS '1'  // Kit dropped and sensor detected it
#define ACTION_FINISHED_WITH_FAILURE '2'  // Kit dropped but sensor didn't detect it (so motor stopped because of the timer interruption)

// relé states
#define MOTOR_ON LOW  // a LOW to the relé is used to close the circuit (and, therefore, give 12V to the motor)
#define MOTOR_OFF HIGH

// timer interruption interval:
#define TIMER_INTERRUPTION   8000L  // 8s

// variable to control if our motor stopped by a sensor detection or by timeout. Volatile to not make any optimization (this variable will change in an ISR and will be readed in the main loop)
volatile bool timeout_reached = false;


// Timer Interrupt Handler (Interrupt Service Routine)
void timeout_ISR() {
  // if timer interrupt was activated
  timeout_reached = true;  // this will detonate some actions in the main loop, look there.
}

void setup() {
  // start up the serial communication:
  Serial.begin(9600);
  while (!Serial);
  // get directly data from the output pin of the IR sensor:
  pinMode (IR_SENSOR, INPUT);
  // don't move the motor (LOW into the rele pin):
  pinMode (RELE_PIN, OUTPUT);
  digitalWrite (RELE_PIN, MOTOR_OFF);
  // init object ITimer1 (TimerInterrupt library)  (this doesn't mean to start any interruption countdown)
  ITimer1.init(); 
}

void loop() {
  
  if (Serial.available()) {
    
      char value_read = Serial.read();
      if(value_read == DROP_KIT) {

         // start moving the motor:
         digitalWrite (RELE_PIN, MOTOR_ON);

         // set timeout_reached to false (it will turn into true only if timeout is reached for this present kit request):
         timeout_reached = false;

         // program a timer interruption (to stop the motor in case that the sensor didn't detect the kit fall)
         ITimer1.attachInterruptInterval(TIMER_INTERRUPTION, timeout_ISR);  
         
         // wait until kit has dropped (sensor outputs HIGH while an object is not being detected) or until timeout is reached:
         int status_IRsensor = digitalRead (IR_SENSOR);  
         while (status_IRsensor == HIGH  &&  !timeout_reached){  // status_IRsensor == HIGH means anything detected by the sensor
            status_IRsensor = digitalRead (IR_SENSOR);
         }

         // stop the timer interruption (until another kit is requested by another user):
         ITimer1.detachInterrupt();
         
         // stop moving the motor:   
         digitalWrite (RELE_PIN, MOTOR_OFF);  

         // communicate to the Raspberry that the process has end (with success if sensor detected the kit or with failure if timeout of the motor was reached (it is, sensor didnt work)):
         if (timeout_reached)
             Serial.print(ACTION_FINISHED_WITH_FAILURE);
         else    
             Serial.print(ACTION_FINISHED_WITH_SUCCESS);


         // note that, for all the kit requests, timeout_reached is setted to false and a new interruption is reprogramated
         // (and when the kit is dropped or we have got a timeout, interrupt is detached until next user)
      }
  }

}
