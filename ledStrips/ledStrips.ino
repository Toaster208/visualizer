#include <Adafruit_NeoPixel.h>


#define NUMPIXELS 8
Adafruit_NeoPixel one(NUMPIXELS, 6, NEO_GRB + NEO_KHZ800);
Adafruit_NeoPixel two(NUMPIXELS, 5, NEO_GRB + NEO_KHZ800);
Adafruit_NeoPixel three(NUMPIXELS, 4, NEO_GRB + NEO_KHZ800);
Adafruit_NeoPixel four(NUMPIXELS, 3, NEO_GRB + NEO_KHZ800);
Adafruit_NeoPixel five(NUMPIXELS, 2, NEO_GRB + NEO_KHZ800);
Adafruit_NeoPixel pixels[] = {one, two, three, four, five};
#define DELAYVAL 0
int num;

void setup() {
  // Initialize serial communication
  Serial.begin(9600);
  Serial.setTimeout(1/0.3);
//  one.begin();
//  two.begin();
  for (int i=0; i<5; i++) {
    pixels[i].begin();
  }
}

void loop() {
  if (Serial.available() > 0) {
    String strengths=Serial.readString();
    for (int i=2; i<10; i+=2) {
      pixels[i/2-1].clear();
//      one.clear();
//      two.clear();
//      String strengths=Serial.readString();
      num=String(strengths[i+1]).toInt();
      if (num != 0) {
        pixels[i/2-1].fill(pixels[i/2-1].Color(0,255,0), 0, num);
//        one.fill(one.Color(0,255,0), 0, num);
//        two.fill(two.Color(0,255,0), 0, num);
      }
      pixels[i/2-1].show();
//      one.show();
//      two.show();
    }
  }
}
