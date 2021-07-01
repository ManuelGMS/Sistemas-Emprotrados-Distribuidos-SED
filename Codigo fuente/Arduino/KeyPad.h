#include <Keypad.h>

char charsOfKeys[4][4] = {
  {'1','2','3','A'},
  {'4','5','6','B'},
  {'7','8','9','C'},
  {'*','0','#','D'}
};

byte rowPins[4] = { 43, 41, 39, 37 }; // Filas 1 - 4
byte colPins[4] = { 35, 33, 31, 29 }; // Columnas 1 - 4

Keypad keyBoard = Keypad(makeKeymap(charsOfKeys), rowPins, colPins, 4, 4);
