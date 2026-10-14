#include <Arduino.h>

#define RLEDPIN 11
#define YLEDPIN 12
#define GLEDPIN 13
#define STARTSENSORPIN 4
#define ENDSENSORPIN 5

elapsedMicros raceTime;     // 
elapsedMillis blinkTime;     //
bool y_blink = false;

bool timer_ready = false;
bool system_ready = false;
bool race_running = false;     

int long finishTime;

void setup() {
  // put your setup code here, to run once:
  
  // configure LED pins
  pinMode(RLEDPIN, OUTPUT);
  pinMode(YLEDPIN, OUTPUT);
  pinMode(GLEDPIN, OUTPUT);
  // configure pullups on sensor pins
  pinMode(STARTSENSORPIN, INPUT_PULLUP);      // turn on the pullup
  pinMode(ENDSENSORPIN, INPUT_PULLUP);      // turn on the pullup
  
  // open serial to host
  Serial.begin(9600);

  // set local ready
  timer_ready = true;
  // add check if host system is ready
  system_ready = true;

}

void loop() {

  // check start condition
  if (digitalRead(STARTSENSORPIN) && timer_ready && system_ready && !race_running)
  {
    // start race! let's gooooo
    // get start time
    raceTime = 0;
    // set race_running
    race_running = true;
    // set timer_ready = false
    timer_ready = false;
    // setup LED
    digitalWrite(YLEDPIN, HIGH);
                            
  }

  // check end condition
  if (digitalRead(ENDSENSORPIN) && race_running)
  {
    // race finished
    // get end time
    finishTime = raceTime;
    // mark race as finished
    race_running = false;
    // setup LED
    digitalWrite(YLEDPIN, LOW);
    // send race time
    Serial.print("t:");
    Serial.println(finishTime);
    // timer_ready = true;
    timer_ready = true;
  }

  // check serial
  if (Serial.available()) {
    char c = Serial.read();
      if (c == 'r') {
        system_ready = true;
      } else if (c == 'n') {
        system_ready = false;
      }
      else {
        ;
    }
  }
}
