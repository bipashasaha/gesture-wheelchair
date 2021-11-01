/*
  Arduino LSM9DS1 - Simple Accelerometer

  This example reads the acceleration values from the LSM9DS1
  sensor and continuously prints them to the Serial Monitor
  or Serial Plotter.

  The circuit:
  - Arduino Nano 33 BLE Sense

  created 10 Jul 2019
  by Riccardo Rizzo

  This example code is in the public domain.
*/

#include <Arduino_LSM9DS1.h>

float x_threshold = 0.3;
float y_threshold = 0.3;

void setup() {
  Serial.begin(9600);
  while (!Serial);

  if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU!");
    while (1);
  }
}

void loop() {
  float ax, ay, az;

  if (IMU.accelerationAvailable()) {
    IMU.readAcceleration(ax, ay, az);
    
    if (ax<=-x_threshold && ay>-y_threshold && ay<y_threshold){
      Serial.print("FORWARD");  
    }
    else if (ax<=-x_threshold && ay<=-y_threshold){
      Serial.print("FORWARD_RIGHT");  
    }
    else if (ax<=-x_threshold && ay>=y_threshold){
      Serial.print("FORWARD_LEFT");  
    }
    else if (ax>=x_threshold && ay>-y_threshold && ay<y_threshold){
      Serial.print("BACKWARD");  
    } 
    else if (ax>=x_threshold && ay<=-y_threshold){
      Serial.print("BACKWARD_RIGHT");  
    } 
    else if (ax>=x_threshold && ay>=y_threshold){
      Serial.print("BACKWARD_LEFT");  
    } 
    else if (ay<=-y_threshold && ax>-x_threshold && ax<x_threshold){
      Serial.print("ROTATE_RIGHT");  
    }
    else if (ay>=y_threshold && ax>-x_threshold && ax<x_threshold){
      Serial.print("ROTATE_LEFT");  
    }
    else {
      Serial.print("IDLE");    
    }
    
    Serial.print('\t');
    Serial.print(ax);
    Serial.print('\t');
    Serial.print(ay);
    Serial.print('\t');
    Serial.print(az);

    Serial.println();
    delay(20);
  }
}