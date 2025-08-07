#include "DRV8825.h"

// Cambiar dependiendo de las conexiones que se hagan con la placa
#define DIR_X  2
#define STEP_X 3 
#define DIR_Y  5
#define STEP_Y 6

const uint8_t POSITIVE_X = 0;  //  LOW
const uint8_t NEGATIVE_Y = 1;  //  HIGH
const uint8_t POSITIVE_Y = 0;  //  LOW
const uint8_t NEGATIVE_Y = 1;  //  HIGH

DRV8825 stepper_x;
DRV8825 stepper_y;

void setup() {
  Serial.begin(115200);
  stepper_x.begin(DIR_X, STEP_X);
  stepper_y.begin(DIR_Y, STEP_X);
  stepper_x.setDirection(POSITIVE_X);
  stepper_y.setDirection(POSITIVE_Y);
  delay(1000);
}


void loop() {
  if (Serial.available()) {
    String input = Serial.readStringUntil('\n');
    // String input = "1,1,1,1,0";
    input.trim();

    int c1 = input.indexOf(',');
    int c2 = input.indexOf(',', c1 + 1);
    int c3 = input.indexOf(',', c2 + 1);
    int c4 = input.indexOf(',', c3 + 1);
    String step_x = input.substring(0, c1);
    String dir_x = input.substring(c1 + 1, c2);
    String step_y = input.substring(c2 + 1, c3);
    String dir_y = input.substring(c3 + 1, c4);
    String s = input.substring(c4 + 1);

    stepper_x.setDirection((dir_x == "1") ? POSITIVE_X : NEGATIVE_X);
    stepper_x.setDirection((dir_y == "1") ? POSITIVE_Y : NEGATIVE_Y);
    
    if (step_x == "1")
      stepper_x.step()
    if (step_y == "1")
      stepper_y.step()

}
