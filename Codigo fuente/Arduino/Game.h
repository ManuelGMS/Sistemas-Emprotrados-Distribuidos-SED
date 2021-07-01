bool userHasTime = true;

void timesUp() {
  userHasTime = false;
}

class Game {

  private:

    // *******************************************
    // Variables de control del juego.
    int hits; // Aciertos (ronda actual).
    String results; // Resultados obtenidos.
    String selected; // Elecciones realizadas.
    // *******************************************
    // Parámetros de la partida (Serial)
    String encoder; // Codificador.
    String code; // Codigo.
    String decoder; // Decodificador.
    bool clues; // Con pistas.
    bool sounds; // Efectos de sonido.
    int answer; // Tiempo para responder.
    int memory; // Tiempo para memorizar.
    int rounds; // Total rondas de la partida.
    int round; // Ronda actual de la partida.
    // *******************************************

    void setTimer() {
      
      if(this->answer != 0) {
        Timer1.initialize();
        Timer1.attachInterrupt(timesUp);
        Timer1.setPeriod(this->answer * 1000000);
        Timer1.stop();
      }
      
    }

    void lcdFeedback() {

      lcd.clear();
      lcd.print("Ronda: ");
      lcd.print(round);
      lcd.setCursor(0, 1);
      lcd.print("Pulsado > ");
      
    }

    void restartTimer() {
      
      if(this->answer != 0) {
        userHasTime = true;
        Timer1.restart();
        Timer1.start();
      }
      
    }

    void userSelection() {

      // El usuario realiza sus selecciones.
      while(this->selected.length() < 4 && userHasTime) {

        char keyPressed = keyBoard.getKey();
        
        if(keyPressed >= 48 && keyPressed <= 57) {
          this->selected += keyPressed;
          lcd.print(keyPressed);
        }
          
      }

    }

    void stopTimer() {
      
      if(this->answer != 0)
        Timer1.stop();
      
    }

    void ledsFeedback() {

      // Reseteamos los aciertos del usuario.
      this->hits = 0;

      // Comprueba las selecciones del usurio.
      for(int i = 0 ; i < 4 ; ++i)
        
        if(this->selected[i] == this->code[i]) {
  
          this->hits += 1; // Incrementar aciertos.
          this->results += "C"; // Correcta (posicion).
          led[i].showRGB(LOW, HIGH, LOW); // Acierto, luz verde.
          
        } else {

          if(this->clues) {
            
            bool colorInOtherPosition = false;
          
            for(int j = 0 ; j < 4 && !colorInOtherPosition ; ++j)
              if(i != j && this->selected[i] == this->code[j])
                colorInOtherPosition = true;
            
            if(colorInOtherPosition) {
              this->results += "O"; // Otra (posicion). 
              led[i].showRGB(LOW, LOW, HIGH); // Desplazado, luz azul.  
            } else {
              this->results += "N"; // No (posicion).
              led[i].showRGB(HIGH, LOW, LOW); // Fallo, luz roja.
            }
          
          } else {

            this->results += "M"; // Mal
            led[i].showRGB(HIGH, LOW, LOW); // Fallo, luz roja.
            
          }
          
        }

    }

    void soundFeedback() {

      // ¿Están los sonidos habilitados?
      if(this->sounds) {

        // Sonido a emitir en función de si hay o no algún acierto. 
        (this->hits > 0)? point.play() : fail.play();

        // Melodía para el final de partida.
        if(this->hits == 4 || this->round == this->rounds) {
          delay(1000);
          (this->hits == 4)? victory.play() : gameOver.play();
        }
        
      }

    }

    void transmitData() {
      
      Serial.println(this->round);
      Serial.println(this->selected);
      Serial.println(this->results);
    
    }

    void prepareNextRound() {

      // Tiempo para memorizar.
      delay(this->memory * 1000);

      // Apaga los LEDS - RGB.
      for(int i = 0 ; i < 4 ; ++i)  
        led[i].turnOff();

      // ¿Se han advinado los 4 caracteres?
      if(this->hits < 4) this->hits = 0;

      // Reinicia las selecciones y los resultados.
      this->results = "";
      this->selected = "";
      
    }

    void showTheWinner() {

      lcd.clear();
      lcd.print("Victoria para:");
      lcd.setCursor(0, 1);
      lcd.print( (this->hits == 4)? this->decoder : this->encoder );
      delay(6000);
      
    }

  public:

    Game() {

      int param = 0;
      this->hits = 0;

      while(param < 9) {
    
        switch(param) {
          case 0:
            if(Serial.available()) {
              this->encoder = Serial.readStringUntil('\n');
              param++;
            }
          break;
          case 1:
            if(Serial.available()) {
              this->code = Serial.readStringUntil('\n');
              param++;
            }
          break;
          case 2:
            if(Serial.available()) {
              this->decoder = Serial.readStringUntil('\n');
              param++;
            }
          break;
          case 3:
            if(Serial.available()) {
              this->clues = Serial.readStringUntil('\n').equals("1");
              param++;
            }
          break;
          case 4:
            if(Serial.available()) {
              this->sounds = Serial.readStringUntil('\n').equals("1");
              param++;
            }
          break;
          case 5:
            if(Serial.available()) {
              this->answer = Serial.readStringUntil('\n').toInt();
              param++;
            }
          break;
          case 6:
            if(Serial.available()) {
              this->memory = Serial.readStringUntil('\n').toInt();
              param++;
            }
          break;
          case 7:
            if(Serial.available()) {
              this->rounds = Serial.readStringUntil('\n').toInt();
              param++;
            }
          break;
          case 8:
            if(Serial.available()) {
              this->round = Serial.readStringUntil('\n').toInt();
              param++;
            }
          break;
        }

      }
      
    }

    void loop() {

      this->setTimer();

      for( ; this->round <= this->rounds && this->hits < 4 ; ++this->round) {

        this->lcdFeedback();

        this->restartTimer();
        
        this->userSelection();

        this->stopTimer();

        this->ledsFeedback();

        this->soundFeedback();

        this->transmitData();

        this->prepareNextRound();

      }

      this->showTheWinner();

    }

};
