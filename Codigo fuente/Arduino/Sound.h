class Sound {

  private:

    int notes;
    int* typeOfNote;
    int* frequencyOfNote;
  
  public:

    Sound() {}

    ~Sound() {
      delete typeOfNote;
      delete frequencyOfNote;
    }

    Sound(int num, ...) {

      this->notes = num / 2;
      this->typeOfNote = new int[notes];
      this->frequencyOfNote = new int[notes];
      
      va_list arguments;
      va_start(arguments, num);

      for(int i = 0 ; i < notes ; ++i)
        this->frequencyOfNote[i] = va_arg(arguments, int);

      for(int i = 0 ; i < notes ; ++i)
        this->typeOfNote[i] = va_arg(arguments, int);

      va_end(arguments);
      
    }

    void play() {
      for (int currentNote = 0 ; currentNote < notes ; ++currentNote) {
        tone(6, frequencyOfNote[currentNote], 1000 / typeOfNote[currentNote]);
        delay((1000 / typeOfNote[currentNote]) * 1.30);
        noTone(6);
      }
    }
      
};

Sound fail(2, 100, 4);
Sound point(2, 10, 1);
Sound gameOver(16, 262, 196, 196, 220, 196, 0, 247, 262, 4, 8, 8, 4, 4, 4, 4, 4);
Sound victory(18, 523, 523, 523, 523, 415, 466, 523, 466, 523, 4, 8, 8, 4, 4, 4, 4, 4, 4);
