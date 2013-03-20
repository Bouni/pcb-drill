/*

PCBdrill improved

 */

// coil states for the stepper motor
int states[8][4] = {
                    {HIGH,LOW,LOW,LOW},
                    {HIGH,HIGH,LOW,LOW},
                    {LOW,HIGH,LOW,LOW},
                    {LOW,HIGH,HIGH,LOW},
                    {LOW,LOW,HIGH,LOW},
                    {LOW,LOW,HIGH,HIGH},
                    {LOW,LOW,LOW,HIGH},
                    {HIGH,LOW,LOW,HIGH}
                   };

void setup() {
  Serial.begin(9600);
  pinMode(10, OUTPUT);
  pinMode(11, OUTPUT);
  pinMode(12, OUTPUT);
  pinMode(13, OUTPUT);
}

void loop() {
  while(Serial.read() == -1) {}
  turn(4
  );  

}

void turn(int _delay) { 
  for(int i = 0; i < 50; i++) {
    for(int state = 0; state < 8; state++) {
      for(int pin = 0; pin < 4; pin++) {
        digitalWrite(pin + 10,states[state][pin]);
      }
      delay(_delay);
    }
  }
}


