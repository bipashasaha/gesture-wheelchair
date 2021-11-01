# Gesture based wheelchair with Arduino Nano 33 BLE Sense
Arduino based gesture controlled wheelchair. Simulation with Python3.


# Requirements

### Hardware
  * Arduino Nano 33 BLE Sense
  * USB to Micro USB connector

### Software
  
  * Arduino IDE
    * Library: Arduino_LSM9DS1
    * Board: Arduino Nano 33 BLE Sense
  
  * Python 3
  * PIP module
    * pyserial
    * pygame


# Setup

* Download and install all the requirements.
  * For Arduino, install them through Arduino IDE.
  * For Python3, install them through [requirements.txt](requirements.txt) 
    
    ```
    python3 -m pip install -r requirements.txt
    ```

* Compile and flash [gesture.ino](./gesture.ino) through Arduino IDE.
* Close Arduino IDE serial monitor before next step.
* Run [main.py](./main.py)
  ```
  python3 main.py
  ```