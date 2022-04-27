/***************************************************************************/
// File       [final_project.ino]
// Author     [Erik Kuo]
// Synopsis   [Code for managing main process]
// Functions  [setup, loop, Search_Mode, Hault_Mode, SetState]
// Modify     [2020/03/27 Erik Kuo]
/***************************************************************************/

//#define DEBUG // debug flag 

// for BlueTooth
#include<SoftwareSerial.h>
// for RFID
#include <SPI.h>
#include <MFRC522.h>

/*===========================define pin & create module object================================*/
// BlueTooth
#define RX 13
#define TX 12
SoftwareSerial BT(RX,TX);   // TX,RX on bluetooth module, 請按照自己車上的接線寫入腳位
// L298N, 請按照自己車上的接線寫入腳位(左右不一定要跟註解寫的一樣)
#define MotorL_I1     14 //定義 I1 接腳（右）
#define MotorL_I2     3  //定義 I2 接腳（右）
#define MotorL_PWML   4  //定義 ENA (PWM調速) 接腳


#define MotorR_I3     16 //定義 I3 接腳（左）
#define MotorR_I4     15 //定義 I4 接腳（左）
#define MotorR_PWMR   2  //定義 ENB (PWM調速) 接腳

// 循線模組, 請按照自己車上的接線寫入腳位
#define L2   33  // Define Left Most Sensor Pin
#define L1   34  // Define Left Middle Sensor Pin
#define M    35
#define R1   36  // Define Right Middle Sensor Pin
#define R2   37  // Define Right Most Sensor Pin
// RFID, 請按照自己車上的接線寫入腳位
#define RST_PIN      7        // 讀卡機的重置腳位
#define SS_PIN       53       // 晶片選擇腳位
MFRC522 mfrc522(SS_PIN, RST_PIN);  // 建立MFRC522物件
/*===========================define pin & create module object===========================*/
char *dir_array;
int node_num;

/*============setup============*/
void setup()
{
   //bluetooth initialization
   BT.begin(9600);
   //Serial window
   Serial.begin(9600);
   //RFID initial
   SPI.begin();
   mfrc522.PCD_Init();
   //L298N pin
   pinMode(MotorL_I1,   OUTPUT);
   pinMode(MotorL_I2,   OUTPUT);
   pinMode(MotorR_I3,   OUTPUT);
   pinMode(MotorR_I4,   OUTPUT);
   pinMode(MotorL_PWML, OUTPUT);
   pinMode(MotorR_PWMR, OUTPUT);
   //tracking pin
   pinMode(R2, INPUT); 
   pinMode(R1, INPUT);
   pinMode(M, INPUT);
   pinMode(L1, INPUT);
   pinMode(L2, INPUT);
#ifdef DEBUG
  Serial.print("Setup!\n");
#endif

}
/*============setup============*/

/*=====Import header files=====*/
// #include "RFID.h"
#include "bluetooth.h"
#include "track.h"


// #include "node.h"
/*=====Import header files=====*/

/*===========================initialize variables===========================*/
int _Tp=220; //set your own value for motor power
bool state=false; //set state to false to halt the car, set state to true to activate the car
bool autoControll = true;
bool _init = 1;
BT_CMD dir = NOTHING;
BT_CMD _cmd = NOTHING; //enum for bluetooth message, reference in bluetooth.h line 2
/*===========================initialize variables===========================*/

/*===========================declare function prototypes===========================*/
void Search();// search graph
void SetState();// switch the state
void ask_action();
void loop();
/*===========================declare function prototypes===========================*/



/*===========================define function===========================*/
void loop(){
    SetState();
    if(_init){
      delay(500);
      ask_action();
      _init = 0;
    }
    if(!state) MotorWriting(0,0);
    else Search();
    
    // if(autoControll){
    //   if(!state) MotorWriting(0,0);
    //   else Search();
    // }
    // else{
    //   Turn(dir);
    // }
    send_RFID();
    
}

void SetState(){
  BT_CMD action = ask_BT();
  if(action == NOTHING)return;
  if(action == Start){
    send_sentance("Start!",strlen("Start!"));
    state=true;
    // if(autoControll){
    //   send_sentance("Start!",strlen("Start!"));
    //   state=true;
    // }
    // else{
    //   send_sentance("Please change to autoControlled mode first",strlen("Please change to autoControlled mode first"));
    // }
  }
  else if(action == Escape){
    state=false;
    dir = NOTHING;
    // autoControll = !autoControll;
    // if(autoControll){
    //   send_sentance("Switch to autoControlled mode",strlen("Switch to autoControlled mode"));
    // }
    // else{
    //   send_sentance("Switch to manual Controlled mode",strlen("Switch to manual Controlled mode"));
    // }
  }
  else{
    dir = action;
  }
  // TODO:
  // 1. Get command from bluetooth 
  // 2. Change state if need
}

void Search(){
  tracking();
  // send_RFID();
  // TODO: let your car search graph(maze) according to bluetooth command from computer(python code)
}

String dir_string;
void ask_action(){
  // char ready;
  
//  send_msg('N');
//  send_msg('\n');
  while(!BT.available())continue;
  
  //[dir]
  dir_string = BT.readString();


  #ifdef DEBUG
  Serial.println("action list:");
  Serial.println(dir_string);
  Serial.print("total: ");
  Serial.println(dir_string.length());
  #endif
  
  node_num = dir_string.length();
  init_action_list(dir_string,node_num);

}
/*===========================define function===========================*/
