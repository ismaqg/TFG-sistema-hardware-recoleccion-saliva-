
// Pin 2 connected to the Rele.
#define RELE_PIN 2

// Output pin of the Infrared sensor into pin 4 of the Arduino
#define IR_SENSOR 4

// identifiers of the different actions that can be requested to this arduino
#define DROP_KIT '0'
#define ACTION_FINISHED '1'

void setup() {
  // start up the serial communication:
  Serial.begin(9600);
  // get directly data from the output pin of the IR sensor:
  pinMode (IR_SENSOR, INPUT);
  // don't move the motor (LOW into the rele pin):
  pinMode (RELE_PIN, OUTPUT);
  digitalWrite (RELE_PIN, LOW);
}

void loop() {
  
  if (Serial.available()) {
    
      char value_read = Serial.read();
      if(value_read == DROP_KIT) {
        
         // start moving the motor:
         digitalWrite (RELE_PIN, HIGH);
         
         // wait until kit has dropped (sensor outputs HIGH while an object is not being detected):
         int status_IRsensor = digitalRead (IR_SENSOR);  
         while (status_IRsensor == HIGH){  // will be waiting in this loop until object is detected (this means, until status_IRsensor == LOW).
            status_IRsensor = digitalRead (IR_SENSOR); 
         }
         
         // stop moving the motor:   
         digitalWrite (RELE_PIN, LOW);  

         // communicate to the Raspberry that the process has end:
         Serial.print(ACTION_FINISHED);
         
      }
  }

}
