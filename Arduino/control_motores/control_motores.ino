// Cambiar dependiendo de las conexiones que se hagan con la placa
#define STEP_X 2 
#define DIR_X  3
#define STEP_Y 5
#define DIR_Y  6

#define STEP_DELAY 500  // microsegundos entre pasos
#define MAX_STEPS 1000  // límite de pasos por seguridad

void setup() {
  Serial.begin(115200);

  pinMode(STEP_X, OUTPUT);
  pinMode(DIR_X, OUTPUT);
  pinMode(STEP_Y, OUTPUT);
  pinMode(DIR_Y, OUTPUT);

  digitalWrite(STEP_X, LOW);
  digitalWrite(DIR_X, LOW);
  digitalWrite(STEP_Y, LOW);
  digitalWrite(DIR_Y, LOW);
}

void loop() {
  if (Serial.available()) {
    // String input = Serial.readStringUntil('\n');
    String input = "1,1,1,1,0";
    input.trim();

    int sep1 = input.indexOf(',');
    int sep2 = input.indexOf(',', sep1 + 1);

    if (sep1 > 0 && sep2 > sep1) {
      int x_dir = input.substring(0, sep1).toInt();
      int y_dir = input.substring(sep1 + 1, sep2).toInt();
      int steps = input.substring(sep2 + 1).toInt();

      // Validación de valores
      steps = constrain(abs(steps), 1, MAX_STEPS);
      
      if (x_dir != 0) moveStepper(DIR_X, STEP_X, x_dir, steps);
      if (y_dir != 0) moveStepper(DIR_Y, STEP_Y, y_dir, steps);
      
      Serial.println("Done"); // Confirmación de movimiento completado
    }
  }
}

void moveStepper(int dirPin, int stepPin, int direction, int steps) {
  digitalWrite(dirPin, direction > 0 ? HIGH : LOW);
  
  for(int i = 0; i < steps; i++) {
    digitalWrite(stepPin, HIGH);
    delayMicroseconds(STEP_DELAY);
    digitalWrite(stepPin, LOW);
    delayMicroseconds(STEP_DELAY);
    
    // Permitir procesar otros eventos si es necesario
    if (i % 100 == 0) {
      delay(0); // Yield para otras tareas
    }
  }
}