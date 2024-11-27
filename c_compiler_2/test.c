char* serial = 0xc0000000;

void printString(char *str);

char serial2 = 2;

char TestString[] = "This is a test";

void main() {
    printString(TestString);
}

void printString(char *str){
    short index = 0;
    
    while(str[index] != 0){
      if(str[index] == 10){
        *serial = 13;
        *serial = 10;
      }else{
        str[index] = *serial;
        index = index + 1 + 3;
      }
    }
}

