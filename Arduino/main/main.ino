int BAUD_RATE = 9600;
int TIME_OUT = 1000;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(BAUD_RATE);
  Serial.setTimeout(TIME_OUT);
}

void loop() {
  // put your main code here, to run repeatedly:
      // Serial.println(Serial.read());
      // Serial.println("hola");
      delay(2000);
    
}
