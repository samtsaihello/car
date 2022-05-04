/***************************************************************************/
// File			  [track.h]
// Author		  [Erik Kuo]
// Synopsis		[Code used for tracking]
// Functions  [MotorWriting, MotorInverter, tracking]
// Modify		  [2020/03/27 Erik Kuo]
/***************************************************************************/
#ifndef _TRACK_
#define _TRACK_

#include <SoftwareSerial.h>
#include <Wire.h>
#include "bluetooth.h"
/*if you have no idea how to start*/
/*check out what you have learned from week 1 & 6*/
/*feel free to add your own function for convenience*/

/*===========================import variable===========================*/
int extern _Tp;
//char* extern dir_array;


//void extern SetState();
/*===========================import variable===========================*/
void MotorWriting(double,double);
void SensorRead();
void NodeDetected();
void Turn(BT_CMD);
void tracking();

double error;
int count;

BT_CMD direct[11]={Right,Right,Return,Right,Right,Return,Left,Front,Left,Stop,Stop};

int now_at=0;
bool map_end=0;

double dErr = 0;
double sumErr = 0 ;
double err_history[100]={0};
//double corr_history[100]={0};
double prev_correction=0;
double prev_correction_L=0;
double prev_correction_R=0;
int times=0;

double adj_R=(233.0/255.0)+2*0.001, adj_L=1;
// Write the voltage to motor.
void MotorWriting(double vL, double vR) {
  vL = adj_L*vL;
  vR = adj_R*vR;
  
  if (vR>= 0) {
    digitalWrite(MotorR_I3, LOW);
    digitalWrite(MotorR_I4, HIGH);
  } 
  else if (vR< 0) {
  digitalWrite(MotorR_I3, HIGH);
  digitalWrite(MotorR_I4, LOW);
  vR= -vR;
  }
  
  if (vL>= 0) {
    digitalWrite(MotorL_I1, LOW);
    digitalWrite(MotorL_I2, HIGH);
  } 
  else if (vL< 0) {
    digitalWrite(MotorL_I1, HIGH);
    digitalWrite(MotorL_I2, LOW);
    vL= -vL;
  }

  if(vL==0&&vR==0){
    digitalWrite(MotorL_I1, LOW);
    digitalWrite(MotorL_I2, LOW);
  }
  
  analogWrite(MotorL_PWML, vL);
  analogWrite(MotorR_PWMR, vR);
}// MotorWriting

//change error & count
void SensorRead(){
  int sensor_value[5];
  error=0;
  count=0;
  for(int i=0;i<5;i++){
    sensor_value[i]=digitalRead(33+i); //L2->L1->M->R1->R2
    error += (i-2)*sensor_value[i];
    count +=sensor_value[i];
  }
}

BT_CMD* direction_arr;
void init_action_list(String dir_string,int node_num){
  send_sentance(dir_string,node_num);
  direction_arr = new BT_CMD[node_num];
  for(int i=0;i<node_num;i++){
    direction_arr[i] = Convert_msg(dir_string[i]);
  }
}

void NodeDetected(){
//  send_msg('N');
  Turn(direction_arr[now_at]);
  
  if(direction_arr[now_at]==Front || direction_arr[now_at+1]==Front){
    _Tp = 250;
  }
  else{
    _Tp = 220;
  }
  now_at++;
  if(now_at+1>node_num){
    now_at=node_num-1;
    map_end=1;
  }
}

void Turn(BT_CMD dir){
  int vR,vL;
  int delay_time=350;
  if(dir==Left){
    vR= 250;
    vL= 94;//94
    MotorWriting(vL, vR);
    delay(delay_time);
    do{
      MotorWriting(vL, vR);
      SensorRead();
    }while(digitalRead(35)!=1||count!=1);
//    delay(delay_time);
    
  }
  else if(dir==Right){
    vR= 94;//94
    vL= 250;
    MotorWriting(vL, vR);
    delay(delay_time);
    do{
    MotorWriting(vL, vR);
    SensorRead();
    }while(digitalRead(35)!=1||count!=1);
//    delay(delay_time);
    
  }
  else if(dir==Front){ //直行
    
    vR= _Tp;
    vL= _Tp;
    MotorWriting(vL, vR);
    delay(100);
    do{
        delay(10);
        SensorRead();
      }while(count!=1);
  }
  else if(dir==Return){ //迴轉
    // MotorWriting(_Tp, _Tp);
    // delay(100);
    double temp = _Tp*0.9;
    vR= temp;
    vL= -temp;
    MotorWriting(vL, vR);
    delay(50);
    do{
        delay(1);
        SensorRead();
      }while(count!=1);     
  }
  else{
    vR=0;
    vL=0;
    MotorWriting(0, 0);
    delay(10000);     
  }
  prev_correction_L = vL-_Tp;
  prev_correction_R = vR-_Tp;
  
}

// P/PID control Tracking
void tracking(){
  double powerCorrection;
  double powerCorrection_L;
  double powerCorrection_R;
  
  bool allBlack=0;
  //read sensor value
  SensorRead();
  if(count!=0)error = error/double(count);
  
  
  int vR,vL;

  if(count==5){ //如果全黑
    allBlack=1;
    MotorWriting(_Tp, _Tp);
    delay(50);
//    MotorWriting(0,0);
//    delay(10);
    SensorRead();  
  }
  bool T_open=1;
  //如果全白，維持前一時刻的轉向
  if(count==0){
     //判斷T端點，先原地迴轉(左)，到找到黑線後再開始 
    if(allBlack && T_open){
      do{
        vR= _Tp;
        vL= -_Tp;
        MotorWriting(vL, vR);
        delay(10);
        SensorRead();
      }while(count==0);
      allBlack=0;
    }

    powerCorrection_L=prev_correction_L;
    powerCorrection_R=prev_correction_R;
  }
  else if(count==5){
//    do{
//        vR= _Tp;
//        vL= _Tp;
//        MotorWriting(vL, vR);
//        delay(10);
//
//        SensorRead();
//    }while(count==5);
//
//    MotorWriting(_Tp, _Tp);
//    delay(40);//原200,150

    NodeDetected();
    powerCorrection_L=prev_correction_L;
    powerCorrection_R=prev_correction_R;
  }
  else{
    dErr = error-err_history[(times+99)%100];
    sumErr += error-err_history[times%100];
    err_history[times%100]=error;
    times++;
    times = (times+100)%100;

    double Kp= 40;
    double Kd= 40; //40
    double Ki= 10; //原本 -1 -10
//    sumErr=0; //if comment => PID
//    dErr=0;

    powerCorrection = Kp* error + Ki*sumErr/100.0 + Kd*dErr;
    powerCorrection_R = -powerCorrection;
    powerCorrection_L = powerCorrection;
    
  }
  
  
  vR= _Tp+powerCorrection_R;
  vL= _Tp+powerCorrection_L;
  
  if(vR>255) vR= 255;
  if(vL>255) vL= 255;
  if(vR<-255) vR= -255;
  if(vL<-255) vL= -255;

  prev_correction=powerCorrection;
  prev_correction_L=powerCorrection_L;
  prev_correction_R=powerCorrection_R;
  MotorWriting(vL, vR);
}// tracking

#endif
