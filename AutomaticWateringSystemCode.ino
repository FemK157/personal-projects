int senseMoisture = 7;
int activatePump = 2;

void setup() {
  // naming and designating pins as inputs/outputs
  pinMode(senseMoisture, INPUT);
  pinMode(activatePump, OUTPUT);
}


void loop() {
  int run_num;
  int max_runs = 20; // overrides conditional statement to turn off water pump after ~10 seconds
  while(run_num < max_runs) {
    // when soil is dry
    if(digitalRead(senseMoisture) == HIGH) {
      digitalWrite(activatePump, HIGH);
      delay(500);
    // when soil is wet
    } else {
      digitalWrite(activatePump, LOW);
      delay(500);
    }
    run_num++; 
  }
  digitalWrite(activatePump, LOW);
  delay(600000); // 10-minute interval between checks 
}

