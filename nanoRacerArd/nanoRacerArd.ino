#include <Arduino.h>
#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

// create the pwm object to control the sero and the esc
Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();


// data structure to hold the wheel angles and motor speeds
struct Data
{ // The struct and bytes[] share same memory location
  uint8_t angles[3];
  int16_t speeds[3];
};

// data structure to send a packet back to the Nano 
struct Packet
{
  // send first
  uint16_t start_seq; // 0x0210, 0x10 will be sent first
  uint8_t len;        // length of payload
  struct Data tx_data;
  uint8_t checksum;
  uint16_t end_seq;   // 0x0310, 0x10 will be sent first
  // send last
};

struct Packet tx_packet; // store packet to be sent
struct Data rx_data; // store received data

/*
  Calculate checksum by XOR-ing all the byte where the pointer "data" points to
  @param data starting address of the data
  @param len length of the data
  @return caculated checksum
*/
uint8_t calc_checksum(void *data, uint8_t len)
{
  uint8_t checksum = 0;
  uint8_t *addr;
  for(addr = (uint8_t*)data; addr < (data + len); addr++){
    // xor all the bytes
    checksum ^= *addr; // checksum = checksum xor value stored in addr
  }
  return checksum;
}

/*
  Read packet from serial buffer
  @return whether a packet is received successfully
*/
bool readPacket()
{
  uint8_t payload_length, checksum, rx;
  while(Serial.available() < 15){
    // not enough bytes to read
  }
  char tmp[15];

  if(Serial.read() != 0x10){
    // first byte not DLE, not a valid packet
    return false;
  }

  // first byte is DLE, read next byte
  if(Serial.read() != 0x02){
    // second byte not STX, not a valid packet
    return false;
  }

  // seems to be a valid packet
  payload_length = Serial.read(); // get length of payload

  // can compare payload length or extra packet type byte to decide where to write received data to
  if(payload_length == 9){
    if(Serial.readBytes((uint8_t*) &rx_data, payload_length) != payload_length){
      // cannot receive required length within timeout
      return false;
    }
  }else{
    // invalid data length
    return false;
  }

  checksum = Serial.read();

  if(calc_checksum(&rx_data, payload_length) != checksum){
    // checksum error
    return false;
  }

  if(Serial.read() != 0x10){
    // last 2nd byte not DLE, not a valid packet
    return false;
  }

  // last 2nd byte is DLE, read next byte
  if(Serial.read() != 0x03){
    // last byte not ETX, not a valid packet
    return false;
  }

  // Yeah! a valid packet is received

  return true;
}

/* 
 * Function to send a packet back to the Nano
 */
void send_packet(){
  tx_packet.len = sizeof(struct Data);

  // mimick actual output
  tx_packet.tx_data.angles[0] = rx_data.angles[0] ;
  tx_packet.tx_data.angles[1] = rx_data.angles[1] ;
  tx_packet.tx_data.angles[2] = rx_data.angles[2] ;
  tx_packet.tx_data.speeds[0] = rx_data.speeds[0] ;
  tx_packet.tx_data.speeds[1] = rx_data.speeds[1] ;
  tx_packet.tx_data.speeds[2] = rx_data.speeds[2] ;

  tx_packet.checksum = calc_checksum(&tx_packet.tx_data, tx_packet.len);
  Serial.write((char*)&tx_packet, sizeof(tx_packet)); // send the packet
}


/* setTurn(int angle)
 *  
 * Function to set the turn angle on the wheels
 * 0 - hard left 
 * 127.5 - neutral
 * 255 - hard right
 */
void setTurn(int angle)
{
  // map the values of 0 to 255 to the values of the servo pulse length between 260 and 330
  int pwmTarget = map(angle,0,255,260,330);

  pwm.setPWM(0, 0, pwmTarget);

}


/* setSpeed(int speed)
 *  
 * Function to set motor speed
 * 0 - stall
 * 40 - lowest speed possible without jitter
 * 255 - high speed
 */
void setSpeed(int speed)
{
  int pwmTarget = map(speed,0,255,300,260);

  pwm.setPWM(1, 0, pwmTarget);

  
}


void setup()
{ // initalize for serial communication with the Nano
  Serial.begin(9600);
  Serial.setTimeout(5000);  // give up waiting if nothing can be read in 2s

  // init tx packet
  tx_packet.start_seq = 0x0210;
  tx_packet.end_seq = 0x0310;

  while(!Serial){
    // wait until Serial is ready
  }


  // intialize the parameters of the pwm
  pwm.begin();
  pwm.setOscillatorFrequency(27000000);
  pwm.setPWMFreq(50);  // Analog servos run at ~50 Hz updates

  delay(10);
}

void loop()
{

  
  if(readPacket()){

    int newAngle = rx_data.angles[0] ;
    int newSpeed = rx_data.speeds[0] ;


    // set the wheel turn angle
    setTurn(newAngle);

    // set the speed
    setSpeed(newSpeed);

    
    // valid packet received, pack new data in new packet and send it out
    send_packet();
  }
}
