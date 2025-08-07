#define STEP_X 2
#define DIR_X  5
#define X_PER_STEP 1
#define PLUS_X 1
#define MINUS_X 0
#define X_STEP_MAX 2150

#define STEP_Y 3
#define DIR_Y  6
#define Y_PER_STEP 1
#define PLUS_Y 0
#define MINUS_Y 1
#define Y_STEP_MAX 1400


#define STEPS_LIMIT 50
#define T_INIT 2000 // ms
#define T_STEP 900 // us
#define T_DIR  5 // ms

#define LS_X 9
#define LS_Y 10

#define LASER 11

float STATE[2];

void setup() {
  Serial.begin(115200);
  pinMode(STEP_X, OUTPUT);
  pinMode(STEP_Y, OUTPUT);
  pinMode(DIR_X, OUTPUT);
  pinMode(DIR_Y, OUTPUT);
  pinMode(LS_X, INPUT_PULLUP);
  pinMode(LS_Y, INPUT_PULLUP);
  pinMode(LASER, OUTPUT);
  digitalWrite(STEP_X, 0);
  digitalWrite(STEP_Y, 0);
  digitalWrite(DIR_X, PLUS_X);
  digitalWrite(DIR_Y, PLUS_Y);
  delay(T_INIT);
}

void loop() {
  analogWrite(LASER, 75);

  calibrate_X();
  calibrate_Y();

  // change_dir(DIR_X, PLUS_X);
  // for (int i=0; i<X_STEP_MAX; i++){
  //   change_dir(DIR_Y, MINUS_Y);
  //   for (int i=0; i<Y_STEP_MAX; i++){
  //     step_pulse(STEP_Y);
  //   }
  //   step_pulse(STEP_X);
  //   change_dir(DIR_Y, PLUS_Y);
  //   for (int i=0; i<Y_STEP_MAX; i++){
  //     step_pulse(STEP_Y);
  //   }
  //   step_pulse(STEP_X);
  // }

  change_dir(DIR_X, PLUS_X);
  for (int i=0; i<X_STEP_MAX; i++)
    step_pulse(STEP_X);
  change_dir(DIR_Y, MINUS_Y);
  for (int i=0; i<Y_STEP_MAX; i++)
    step_pulse(STEP_Y);
  change_dir(DIR_X, MINUS_X);
  for (int i=0; i<X_STEP_MAX; i++)
    step_pulse(STEP_X);
  change_dir(DIR_Y, PLUS_Y);
  for (int i=0; i<Y_STEP_MAX; i++)
    step_pulse(STEP_Y);


}


void step_pulse(int step_pin) {
  // if ( step_pin == STEP_X )
  //   if ( digitalRead(DIR_X) == PLUS_X )
  //     STATE[0] += X_PER_STEP;
  //   else 
  //     STATE[0] -= X_PER_STEP;
  // else if ( step_pin == STEP_Y )
  //   if ( digitalRead(DIR_Y) == PLUS_Y )
  //     STATE[1] += Y_PER_STEP;
  //   else
  //     STATE[1] -= Y_PER_STEP;
  digitalWrite(step_pin, 1);
  delayMicroseconds(T_STEP/2);
  digitalWrite(step_pin, 0);
  delayMicroseconds(T_STEP/2);

  // Serial.print("X:");
  // Serial.print(STATE[0]);
  // Serial.print(",");
  // Serial.print("Y:");
  // Serial.println(STATE[1]);
}

void change_dir(int dir_pin, bool dir_val) {
  if ( digitalRead(dir_pin) == dir_val)
    return; 
  delay(T_DIR/2);
  digitalWrite(dir_pin, dir_val);
  delay(T_DIR/2);
}

void calibrate_X(){
  change_dir(DIR_X, MINUS_X);
  while ( digitalRead(LS_X)){
    step_pulse(STEP_X);
  }
  change_dir(DIR_X, PLUS_X);
  delay(500);
  for (int i; i<STEPS_LIMIT; i++){
    step_pulse(STEP_X);
  }
  STATE[0] = 0;
}

void calibrate_Y(){
  change_dir(DIR_Y, PLUS_Y);
  while ( digitalRead(LS_Y)){
    step_pulse(STEP_Y);
  }
  change_dir(DIR_Y, MINUS_Y);
  delay(500);
  for (int i; i<STEPS_LIMIT; i++){
    step_pulse(STEP_Y);
  }
  STATE[1] = Y_STEP_MAX;
}