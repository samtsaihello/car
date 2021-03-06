/***************************************************************************/
// File			  [bluetooth.h]
// Author		  [Erik Kuo]
// Synopsis		[Code for bluetooth communication]
// Functions  [ask_BT, send_msg, send_byte]
// Modify		  [2020/03/27 Erik Kuo]
/***************************************************************************/

/*if you have no idea how to start*/
/*check out what you have learned from week 2*/ 
#ifndef _BLUETOOTH_
#define _BLUETOOTH_

#include<SoftwareSerial.h>
#include<MFRC522.h>
#include <SPI.h>

enum BT_CMD {
  NOTHING,
  Right,
  Left,
  Return,
  Front,
  Stop,
  Start,
  Escape
  // TODO: add your own command type here
};

BT_CMD ask_BT();
BT_CMD Convert_msg(char);
void send_msg(const char&);
void send_byte(byte*, byte&);
void send_RFID();
void send_sentance(String,int);

BT_CMD ask_BT(){
    BT_CMD message=NOTHING;
    char cmd;
    if(BT.available()){
      // TODO:
      // 1. get cmd from SoftwareSerial object: BT
      // 2. link bluetooth message to your own command type
      cmd = BT.read();
      message = Convert_msg(cmd);
//      send_msg(cmd);
    }
    return message;
}// ask_BT

BT_CMD Convert_msg(char msg){
  BT_CMD message;
  switch (msg){
    case 'R':
      message = Right;
      break;
    case 'L':
      message = Left;
      break;
    case 'F':
      message = Front;
      break;
    case 'B':
      message = Return;
      break;
    case 'S':
      message = Stop;
      break;
    case 's':
      message = Start;
      break;
    case 'e':
      message = Escape;
      break;
    
    default:
      break;
    }
    
    #ifdef DEBUG
      Serial.print("cmd : ");
      Serial.println(msg);
    #endif
    return message;
}
// send msg back through SoftwareSerial object: BT
// can use send_byte alternatively to send msg back
// (but need to convert to byte type)
//please put "\n" at the end
void send_msg(const char& msg)
{ // TODO:
  BT.print(msg);
}// send_msg


void send_sentance(String msg,int len){
  for(int i=0;i<len;i++){
    BT.write(msg[i]);
  }
  BT.write('\n');
}// send_sentance

// send UID back through SoftwareSerial object: BT
void send_byte(byte *id, byte& idSize) {
  for (byte i = 0; i < idSize; i++) {  // Send UID consequently.
    if(id[i]<16)BT.print(byte(0),HEX);
    BT.print(id[i],HEX);
  }
//  BT.write("\n");
  
  #ifdef DEBUG
  Serial.print("Sent id: ");
  for (byte i = 0; i < idSize; i++) {  // Show UID consequently.
    Serial.print(id[i], HEX);
  }
  Serial.println();
  #endif
}// send_byte

void send_RFID(){
  if (mfrc522.PICC_IsNewCardPresent() && mfrc522.PICC_ReadCardSerial()) {
      byte *id = mfrc522.uid.uidByte;   // ???????????????UID
      byte& idSize = mfrc522.uid.size;   // ??????UID?????????

      //Serial.print("PICC type: ");      // ??????????????????
      // ?????????????????????SAK??????mfrc522.uid.sak?????????????????????
      //MFRC522::PICC_Type piccType = mfrc522.PICC_GetType(mfrc522.uid.sak);
      //Serial.println(mfrc522.PICC_GetTypeName(piccType));
      #ifdef DEBUG
      Serial.print("UID Size: ");       // ???????????????UID?????????
      Serial.println(idSize);   
      for (byte i = 0; i < idSize; i++) {  // ????????????UID???
        Serial.print("id[");
        Serial.print(i);
        Serial.print("]: ");
        Serial.println(id[i], HEX);
//        Serial.println(id[i]<10);// ???16????????????UID???  
      }
      Serial.println();
      #endif
      
      mfrc522.PICC_HaltA();  // ???????????????????????????
      send_sentance("UID",3);
      delay(10);
      send_byte(id, idSize);
  }
}
#endif
