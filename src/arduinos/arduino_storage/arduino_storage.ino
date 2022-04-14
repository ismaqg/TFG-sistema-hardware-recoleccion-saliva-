// TEMPERATURE SENSOR: DS18B20

 
#include <OneWire.h> //https://hacksterio.s3.amazonaws.com/uploads/attachments/229743/OneWire.zip  (download and unzip it at ~/Arduino/Libraries)
#include <DallasTemperature.h> //https://github.com/milesburton/Arduino-Temperature-Control-Library  (git clone it at ~/Arduino/Libraries)


// Data wire of the temperature sensor into pin 2 on the Arduino 
#define ONE_WIRE_BUS 2

#define GET_TEMP_IDENTIFIER '0'

// Setup a oneWire instance to communicate with any OneWire devices   
OneWire oneWire(ONE_WIRE_BUS); 

// Pass our oneWire reference to Dallas Temperature. 
DallasTemperature sensors(&oneWire);


void setup(void) {
  // start up the serial communication
  Serial.begin(9600);
  // start up the library:
  sensors.begin();  
}

void loop(void) {
  if (Serial.available() && Serial.read() == GET_TEMP_IDENTIFIER) {
      sensors.requestTemperatures(); // read temp
      Serial.print(sensors.getTempCByIndex(0)); // send temp value to the raspberry
  }  
}
