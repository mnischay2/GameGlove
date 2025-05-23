#include <Wire.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
Adafruit_MPU6050 mpu;
const int flex_index = 35;  // Analog pin for flex sensor
const int touchSensorPin = 4;  // Digital pin for touch sensor
void setup() {
    Serial.begin(9600);
    Wire.begin();  
    if (!mpu.begin()) {
        while (1);    }
    mpu.setAccelerometerRange(MPU6050_RANGE_8_G);
    mpu.setGyroRange(MPU6050_RANGE_500_DEG);
    mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);
    pinMode(flex_index, INPUT);
    pinMode(touchSensorPin, INPUT);
    delay(1000);
}
void loop(){
  String fd="";
 if (digitalRead(touchSensorPin) == HIGH) {  // Only send data if the glove is worn
    sensors_event_t a, g, temp;
    mpu.getEvent(&a, &g, &temp);
    float ax=a.acceleration.x;
    float ay=a.acceleration.y;
    int indexflexValue = analogRead(flex_index);
    String Tilt=detectTilt(ax,ay);
    fd+=Tilt;
    if (indexflexValue > 990) {  // Adjust threshold based on testing
      fd+="INDEX";
    }}
 else{    fd+="OFF"; }
  Serial.println(fd); 
  delay(200);
}
String detectTilt(float ax, float ay) {
    String tilt="";
    if (ay < -5.5)  tilt+="FRONT,";
    if (ay > 5.5) tilt+="BACK,";
    if (ax > 5.5) tilt+="LEFT,";
    if (ax < -5.5) tilt+="RIGHT,";
    if(((ay > -5.5) && (ay < 5.5)) && ((ax < 5.5) && (ax > -5.5) ) ) tilt+="None,";
    return tilt;
}


