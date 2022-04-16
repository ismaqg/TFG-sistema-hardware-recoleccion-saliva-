// TEMPERATURE SENSOR: DS18B20

 
#include <OneWire.h> //https://hacksterio.s3.amazonaws.com/uploads/attachments/229743/OneWire.zip  (download and unzip it at ~/Arduino/Libraries)
#include <DallasTemperature.h> //https://github.com/milesburton/Arduino-Temperature-Control-Library  (git clone it at ~/Arduino/Libraries)


// Data wire of the temperature sensor into pin 2 on the Arduino 
#define ONE_WIRE_BUS 2

// Output pin of the Infrared sensor into pin 4 of the Arduino
#define IR_SENSOR 4

// identifiers of the different actions that can be requested to this arduino
#define GET_TEMP_IDENTIFIER '0'
#define START_CHECKING_IF_SAMPLE_SUBMITTED '1'
#define GET_IF_SAMPLE_SUBMITTED '2'
#define STOP_CHECKING_IF_SAMPLE_SUBMITTED '3'

// Setup a oneWire instance to communicate with any OneWire devices (used by temperature sensor)   
OneWire oneWire(ONE_WIRE_BUS); 

// Pass our oneWire reference to Dallas Temperature. 
DallasTemperature sensors(&oneWire);

// Sample delivery variables:
bool can_check_if_sample_submitted;
bool sample_submitted;

void setup(void) {
  // start up the serial communication
  Serial.begin(9600);
  // start up the temperature sensor library:
  sensors.begin();
  // get directly data from the output pin of the IR sensor:
  pinMode (IR_SENSOR, INPUT);
  // initial value of the sample delivery variables:
  can_check_if_sample_submitted = false;
  sample_submitted = false;
}

void loop(void) {
  
  if (Serial.available()) {
      // Serial.read() empties the buffer, so we CAN'T use the function in all the if-elses, we need to use it once and keep the value:
      char value_read = Serial.read();

      // TEMPERATURE REQUEST:
      if(value_read == GET_TEMP_IDENTIFIER) {
          sensors.requestTemperatures(); // read temp
          Serial.print(sensors.getTempCByIndex(0)); // send temp value to the raspberry
      }

      // USER SUBMITTING SAMPLE ASSOCIATED REQUESTS:
      else if(value_read == START_CHECKING_IF_SAMPLE_SUBMITTED) {
          can_check_if_sample_submitted = true;
          sample_submitted = false;  //redundant.
      } else if(value_read == GET_IF_SAMPLE_SUBMITTED) {
          if( not sample_submitted ) Serial.print('0');
          else {
              Serial.print('1');
              // reset sample_submissions variables for the next time that an user wants to delivery a sample:
              can_check_if_sample_submitted = false;  //redundant.
              sample_submitted = false;  
          } 
      } else if(value_read == STOP_CHECKING_IF_SAMPLE_SUBMITTED) {  // if an error has occurred (the user indicates that he has delivered a sample but the sensor has not detected it) the raspberry will ask the sensor to stop looking if a sample is detected
          can_check_if_sample_submitted = false;
          sample_submitted = false;  //redundant.
      } 
      
  }

  // constantly check if sample submission is detected (starts when the user reaches the submit sample screen and stops when the submission is detected or when the user indicates that it has already been submitted (which would mean that the sensor didn't detected the sample, but user has ended his session so the sensor doesn't need to still be checking):
  if (can_check_if_sample_submitted) {
      int status_IRsensor = digitalRead (IR_SENSOR);
      if (status_IRsensor == LOW){ // Has detected an object
          sample_submitted = true;
          can_check_if_sample_submitted = false; // cuando ya hemos visto que se ha entregado la muestra, no necesitamos seguir leyendo el sensor
      }
  }
  
}

/* FLOW OF ACTIONS WHEN USER SUBMITTING A SAMPLE:
- Raspberry indicates arduino that can start checking if a sample is delivered
- When arduino sees a sample delivering, activates a flag
- Periodically, Raspberry asks Arduino if sample has been delivered:
  - if the sample has been delivered, Arduino will indicate this to the Raspberry, so raspberry will logout the user and the Arduino will stop checking sample delivering until Raspberry indicates it in the next user.
  - if the sample hasn't been delivered, Arduino will indicate this to the Raspberry but will be still checking if a sample delivery occur to indicate this to the Raspberry the next time that the raspberry asks.
- In the Raspberry, the user can indicate explicitly that a sample has been delivered (if arduino was not able to detect it for any reason). In this case, Raspberry will indicate arduino to stop checking if a sample delivery occurs for this user, and will indicate to an operator that user indicated sample submission when arduino didn't detect it.
*/
