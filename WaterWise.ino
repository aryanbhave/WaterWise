/*
   -------------------------------------------------------------------------------------
   HX711_ADC
   Arduino library for HX711 24-Bit Analog-to-Digital Converter for Weight Scales
   Olav Kallhovd sept2017
   -------------------------------------------------------------------------------------
*/

/*
   Settling time (number of samples) and data filtering can be adjusted in the config.h file
   For calibration and storing the calibration value in eeprom, see example file "Calibration.ino"

   The update() function checks for new data and starts the next conversion. In order to acheive maximum effective
   sample rate, update() should be called at least as often as the HX711 sample rate; >10Hz@10SPS, >80Hz@80SPS.
   If you have other time consuming code running (i.e. a graphical LCD), consider calling update() from an interrupt routine,
   see example file "Read_1x_load_cell_interrupt_driven.ino".

   This is an example sketch on how to use this library
*/

#include <HX711_ADC.h>
#include <WiFi.h>
#include <HTTPClient.h>

#if defined(ESP8266) || defined(ESP32) || defined(AVR)
#include <EEPROM.h>
#endif

const char *ssid = "Smit's Pixel 7";
const char *password = "smit1234";
char *bottleID = "mytest1";
float measurement = 0.0;
float prevMeasurement = 0.0;
unsigned long millisecondsToNotify = 7200000; // 2hrs
// unsigned long millisecondsToNotify = 30000 // for tesing 30secs once
unsigned long timer = 0 

// pins:
const int HX711_dout = 4; // mcu > HX711 dout pin
const int HX711_sck = 16; // mcu > HX711 sck pin

// HX711 constructor:
HX711_ADC LoadCell(HX711_dout, HX711_sck);

const int calVal_eepromAdress = 0;
unsigned long t = 0;

void setup()
{
  pinMode(27, OUTPUT);
  Serial.begin(57600);
  delay(10);
  Serial.println();
  Serial.println("Starting...");

  // Start LoadCell
  LoadCell.begin();

  // Connect to Wi-Fi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi!");

  // LoadCell.setReverseOutput(); //uncomment to turn a negative output value to positive
  float calibrationValue;    // calibration value (see example file "Calibration.ino")
  calibrationValue = 102.48; // uncomment this if you want to set the calibration value in the sketch
#if defined(ESP8266) || defined(ESP32)
  // EEPROM.begin(512); // uncomment this if you use ESP8266/ESP32 and want to fetch the calibration value from eeprom
#endif
  // EEPROM.get(calVal_eepromAdress, calibrationValue); // uncomment this if you want to fetch the calibration value from eeprom

  unsigned long stabilizingtime = 10000; // preciscion right after power-up can be improved by adding a few seconds of stabilizing time
  boolean _tare = true;                  // set this to false if you don't want tare to be performed in the next step
  LoadCell.start(stabilizingtime, _tare);
  if (LoadCell.getTareTimeoutFlag())
  {
    Serial.println("Timeout, check MCU>HX711 wiring and pin designations");
    while (1)
      ;
  }
  else
  {
    LoadCell.setCalFactor(calibrationValue); // set calibration value (float)
    Serial.println("Startup is complete");
  }
}

void loop()
{
  static boolean newDataReady = 0;
  const int serialPrintInterval = 10000; // increase value to slow down serial print activity

  // check for new data/start next conversion:
  if (LoadCell.update())
    newDataReady = true;

  // get smoothed value from the dataset:
  if (newDataReady)
  {
    if (millis() > t + serialPrintInterval)
    {
      float i = LoadCell.getData();
      Serial.print("Load_cell output val: ");
      Serial.println(i);
      newDataReady = 0;
      measurement = i;
      if (measurement > 50.0 && measurement < 2500.0)
      {
        // Water Got Refilled
        if (measurement - prevMeasurement >= 20.0)
        {
          prevMeasurement = measurement;
        }
        // Water used
        else if (prevMeasurement - measurement >= 20.0)
        {
          float diff = prevMeasurement - measurement;
          prevMeasurement = measurement;
          callWeb2(diff);
          timer = millis();
          ledControl(false)
        }
        // callWeb2();
      }
      if(millis() > timer + millisecondsToNotify){
        ledControl(true)
      }
      t = millis();
    }
    
  }

  // receive command from serial terminal, send 't' to initiate tare operation:
  if (Serial.available() > 0)
  {
    char inByte = Serial.read();
    if (inByte == 't')
      LoadCell.tareNoDelay();
  }

  // check if last tare operation is complete:
  if (LoadCell.getTareStatus() == true)
  {
    Serial.println("Tare complete");
  }
}

void callWeb2(float diff)
{
  Serial.println("reached Web client");

  WiFiClient client;
  const char *host = "waterwise315.online";
  const char *url = "/logging/";
  // const char* params = "?bottleID="+bottleID.c_str()+"&measurement="+measurement;

  const uint16_t port = 80;
  String requestUrl = String(url) + String("?bottleID=") + String(bottleID) + String("&measurement=") + String(diff);
  String readRequest = String("GET ") + requestUrl + " HTTP/1.1\r\n" + "Host: " + host + "\r\n" + "Connection: close\r\n\r\n";
  Serial.println(readRequest);
  if (!client.connect(host, port))
  {
    return;
  }
  Serial.println("connected");
  client.print(readRequest);
  readResponse(&client);
}

// read the page and print onto the browser of the client

void readResponse(WiFiClient *client)
{
  Serial.println("writing to Page");
  unsigned long timeout = millis();
  while (client->available() == 0)
  {
    if (millis() - timeout > 5000)
    {
      Serial.println(">>> Client Timeout !");
      client->stop();
      return;
    }
  }

  while (client->available())
  {
    String line = client->readStringUntil('\r\n\r\n');
    Serial.print(line);
  }
  // for closing connection

  Serial.println();

  // webclient.stop();
  Serial.println("Client Disconnected.");

  Serial.println("\nClosing connection\n\n");
}

void ledControl(bool setCondition){
   if(setCondition){
    digitalWrite(27, HIGH);
   }else{
    digitalWrite(27, LOW)
   } 
}
