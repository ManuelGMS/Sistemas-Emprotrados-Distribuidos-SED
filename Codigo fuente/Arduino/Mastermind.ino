#include <TimerOne.h>
#include <LiquidCrystal.h>

LiquidCrystal lcd(7,8,9,10,11,12);

#include "Sound.h"
#include "KeyPad.h"
#include "LedRGB.h"
#include "Game.h"

void setup() {

  // Configura e inicializa los LEDS - RGB
  led[3] = LedRGB(5, 4, 3);
  led[2] = LedRGB(26, 24, 22);
  led[1] = LedRGB(27, 25, 23);
  led[0] = LedRGB(32, 30, 28);
  
  // Configuración del LCD - Display.
  lcd.begin(16,2); // Habilita las 2 filas y las 16 columnas. 

  // Abre una conexión entre ARDUINO y el computador conectado a este.
  Serial.begin(9600); // Indica que la tasa de baudios es de 9600 por segundo.

}

void loop() {

  lcd.clear();
  lcd.print("En espera ...");

  while(Serial.available() == 0);

  Game game;
  game.loop();
  
}
