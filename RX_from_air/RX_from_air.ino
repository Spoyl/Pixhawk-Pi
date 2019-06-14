
// Notes: Consider the maximum size of the array!
// The timing of the transmission and reception matters...ill timing can clip and hide messages!
  
  #define SOP '<'
  #define EOP '>'
  char inData[80];
  byte index;
  bool started = false;
  bool ended = false;


void setup() {

Serial.begin(57600);
  
}

void loop() {


while (Serial.available() > 0) //while data is available to read
    {
      char inChar = Serial.read(); //read first character in Serial

      //check if start of string
      if (inChar == SOP)
      {
        index = 0; //reset position of character in string
        inData[index] = '\0'; //for arduino to handle string
        
        //track progress
        started = true;
        ended = false;
      }

      //check if end of string
      else if (inChar == EOP)
      {
        ended = true; //track progress
       
        break; //stop trying to read from Serial (no data left)
      }

      //between start and end
      else
      {
        if (index < 80) //within length of array
        {
          //append character read from Serial to array 'inData'
          inData[index] = inChar;
          index++;
          
          inData[index] = '\0'; //for string handling
        
        }
      }
  }
  
  Serial.print("The latest message received was: "); //print out the latest message and keep repeating it until new message is received 
  Serial.println(inData);
  delay(200);
}

