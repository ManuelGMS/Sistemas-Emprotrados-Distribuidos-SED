class LedRGB {

  private:

    int redPin;
    int greenPin;
    int bluePin;
  
  public:

    LedRGB() {}
    
    LedRGB(int redPin, int greenPin, int bluePin) {
      this->redPin = redPin;
      this->greenPin = greenPin;
      this->bluePin = bluePin;
      pinMode(this->redPin, OUTPUT);
      pinMode(this->greenPin, OUTPUT);
      pinMode(this->bluePin, OUTPUT);
      this->turnOff();
    }

    void showRGB(bool red, bool green, bool blue) {
      digitalWrite(this->redPin, red);
      digitalWrite(this->greenPin, green);
      digitalWrite(this->bluePin, blue);
    }

    void turnOff() {
      digitalWrite(this->redPin, LOW);
      digitalWrite(this->greenPin, LOW);
      digitalWrite(this->bluePin, LOW);
    }

};

LedRGB led[4];
