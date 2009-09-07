#include "WProgram.h"
extern "C" void __cxa_pure_virtual() {}  
void setup() {
  Serial.begin(9600);
}

void loop() {
  Serial.println("Hello World!");
}


int main(void)
{
	init();

	setup();
    
	for (;;)
		loop();
        
	return 0;
}

