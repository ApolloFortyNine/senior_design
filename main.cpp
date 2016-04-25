#include "mbed.h"
#include "rtos.h"
#include "LSM9DS0.h"
#define LSM9DS0_XM  0x1D // Would be 0x1E if SDO_XM is LOW
#define LSM9DS0_G   0x6B // Would be 0x6A if SDO_G is LOW
#include <mbed.h>
#include <string>
#include <math.h>
#include <list>
#include <mpr121.h>
#include <numeric>

#define PI 3.14159

Serial pc(USBTX, USBRX);
Serial port(p13, p14);

Ticker flipper;
AnalogIn flex1(p16);
AnalogIn flex2(p17);
AnalogIn flex3(p18);
AnalogIn flex4(p19);
AnalogIn flex5(p20);
DigitalOut led1(LED1);
DigitalOut led2(LED2);
DigitalOut led3(LED3);
DigitalOut led4(LED4);
DigitalIn PB1(p12);
I2C i2c(p9, p10);
InterruptIn interrupt(p26);

// Setup the Mpr121:
// constructor(i2c object, i2c address of the mpr121)
Mpr121 mpr121(&i2c, Mpr121::ADD_VSS);

// Create an instance of the LSM9DS0 library called `dof` the
// parameters for this constructor are:
// pins,[gyro I2C address],[xm I2C add.]
LSM9DS0 dof(p28, p27, LSM9DS0_G, LSM9DS0_XM);
DigitalIn DReady(p23);

void readGyro();
void readAccel();
void readFlexSensor();

float imu_gx;
float imu_gy;
float imu_gz;

float imu_ax;
float imu_ay;
float imu_az;

float imu_mx;
float imu_my;
float imu_mz;

float t_f;
float i_f;
float m_f;
float r_f;
float p_f;

int capValue;
int t_c;
int i_cu;
int i_cl;
int i_co;
int m_cu;
int m_cl;
int r_cu;
int r_cl;
int p_cu;
int p_cl;

int N;
list<float> mov_det;
list<float> flex_det;
float mov_chk;
float flex_chk;
float mov_avg;
float flex_avg;
bool idle;

bool command(const char *cmd)
{
    char result[240];
    strcpy(result,"assert(loadfile(\"send_sock.lua\"))(\"");
    strcat(result,cmd);
    strcat(result,"\")\r\n");
    pc.printf(result);
    led2 = !led2;
//    char *result = "assert(loadfile(\"send_sock.lua\"))(\"stuffthis\")\r\n";
    for (int i = 0; i<strlen(result); i++) {
        port.putc(result[i]);
        pc.putc(result[i]);
    }
    return true;
}

void setup()
{
    pc.baud(115200); // Start serial at 115200 bps
    // Use the begin() function to initialize the LSM9DS0 library.
    // You can either call it with no parameters (the easy wimu_imu_imu_imu_imu_imu_imu_imu_imu_imu_imu_imu_imu_imu_imu_imu_ay):
    uint16_t status = dof.begin();

    //Set the threshold for electrode touch/release sensing
    for(int e = 0; e <= 11; e++) {
        mpr121.setElectrodeThreshold(e, 0x30, 0x3F);
    }
    //mpr121.setProximityMode(true);
    mpr121.setProximityMode(false);
    // Or call it with declarations for sensor scales and data rates:
    //uint16_t status = dof.begin(dof.G_SCALE_2000DPS,
    //                            dof.A_SCALE_6G, dof.M_SCALE_2GS);

    // begin() returns a 16-bit value which includes both the gyro
    // and accelerometers WHO_AM_I response. You can check this to
    // make sure communication was successful.
    pc.printf("LSM9DS0 WHO_AM_I's returned: 0x");
    pc.printf("%x\n",status);
    pc.printf("Should be 0x49D4\n");
    pc.printf("\n");
    
    //IDLE CHECKER INITIALIZATION
    //Initialize checking variables
    N = 10; //Sample size of rolling average
    
    //Populate rolling average arrays
    for(int i = 0; i < N; i++)
    {
        readGyro();
        readAccel();
        mov_det.push_back(sqrt(pow(abs(imu_ax)+1,2)+pow(abs(imu_ay)+1,2)+pow(abs(imu_az)+1,2)+
                pow(abs(imu_gx)+1,2)+pow(abs(imu_gy)+1,2)+pow(abs(imu_gz)+1,2)));
                
        readFlexSensor();
        flex_det.push_back(pow(t_f,2)+pow(i_f,2)+pow(m_f,2)+pow(r_f,2)+pow(p_f,2));        
    }
    mov_chk = accumulate(mov_det.begin(), mov_det.end(), 0.0f);
    flex_chk = accumulate(flex_det.begin(), flex_det.end(), 0.0f);
}

void readGyro()
{
    dof.readGyro();
    imu_gx = dof.calcGyro(dof.gx);
    imu_gy = dof.calcGyro(dof.gy);
    imu_gz = dof.calcGyro(dof.gz);
    //pc.printf("imu_gx = %f\r\n", imu_gx);
    //pc.printf("imu_gy = %f\r\n", imu_gy);
    //pc.printf("imu_gz = %f\r\n", imu_gz);
}

void readAccel()
{
    dof.readAccel();
    imu_ax = dof.calcAccel(dof.ax);
    imu_ay = dof.calcAccel(dof.ay);
    imu_az = dof.calcAccel(dof.az);
    //pc.printf("imu_ax = %f\r\n", imu_ax);
    //pc.printf("imu_ay = %f\r\n", imu_ay);
    //pc.printf("imu_az = %f\r\n", imu_az);
}

void readMag()
{
    dof.readMag();
    imu_mx = dof.calcMag(dof.mx);
    imu_my = dof.calcMag(dof.my);
    imu_mz = dof.calcMag(dof.mz);
    //pc.printf("imu_mx = %f\r\n", imu_mx);
    //pc.printf("imu_my = %f\r\n", imu_my);
    //pc.printf("imu_mz = %f\r\n", imu_mz);
}

void readFlexSensor()
{
    int delta = 0.01;
    p_f = flex1.read();
    p_f = p_f+(1/((1-pow((double)p_f,0.5))+delta));
    r_f = flex2.read();
    r_f = r_f+(1/((1-pow((double)r_f,0.5))+delta));
    m_f = flex3.read();
    m_f = m_f+(1/((1-pow((double)m_f,0.5))+delta));
    i_f = flex4.read();
    i_f = i_f+(1/((1-pow((double)i_f,0.5))+delta));
    t_f = flex5.read();
    t_f = t_f+(1/((1-pow((double)t_f,0.5))+delta));
    //pc.printf("thumb_flex = %f \n\r", t_f);
    //pc.printf("index_flex = %f \n\r", i_f);
    //pc.printf("middle_flex= %f \n\r", m_f);
    //pc.printf("ring_flex = %f \n\r", r_f);
    //pc.printf("pinky_flex = %f \n\r", p_f);
}

void readCap()
{
    capValue=mpr121.read(0x00);
    //pc.printf("%d\n\r",capValue);
    capValue +=mpr121.read(0x01)<<8;
    //pc.printf("value = %d \n\r", capValue);//p_cl, p_cu, r_cl, r_cu, m_cl, m_cu, i_co, i_cl, i_cu, t_c
    led1 = !led1;
    t_c = (capValue & 0x1);
    i_cu = (capValue & 0x1<<1)>>1;
    i_cl = (capValue & 0x1<<2)>>2;
    i_co = (capValue & 0x1<<3)>>3;
    m_cu = (capValue & 0x1<<4)>>4;
    m_cl = (capValue & 0x1<<5)>>5;
    r_cu = (capValue & 0x1<<6)>>6;
    r_cl = (capValue & 0x1<<7)>>7;
    p_cu = (capValue & 0x1<<8)>>8;
    p_cl = (capValue & 0x1<<9)>>9;

    /*
    pc.printf("t_c = %d\r\n", t_c);
    pc.printf("i_cu = %d\r\n", i_cu);
    pc.printf("i_cl = %d\r\n", i_cl);
    pc.printf("i_co = %d\r\n", i_co);
    pc.printf("m_cu = %d\r\n", m_cu);
    pc.printf("m_cl = %d\r\n", m_cl);
    pc.printf("r_cu = %d\r\n", r_cu);
    pc.printf("r_cl = %d\r\n", r_cl);
    pc.printf("p_cu = %d\r\n", p_cu);
    pc.printf("p_cl = %d\r\n", p_cl);
    */
}

void checkIdle(void const* args)
{
    while(true)
    {
    readGyro();
    readAccel();
    if(mov_det.size() >= N)
        mov_det.pop_front();
    mov_det.push_back(sqrt(pow(abs(imu_ax/N)+1,2)+pow(abs(imu_ay/N)+1,2)+pow(abs(imu_az/N)+1,2)));//+
            //pow(abs(imu_gx)+1,2)+pow(abs(imu_gy)+1,2)+pow(abs(imu_gz)+1,2)));
    //mov_chk = mov_det.front();
           
    readFlexSensor();
    if(flex_det.size() >= N)
        flex_det.pop_front();
    flex_det.push_back(pow(t_f,2)+pow(i_f,2)+pow(m_f,2)+pow(r_f,2)+pow(p_f,2));
   // flex_chk = flex_det.front();
    
    mov_avg = accumulate(mov_det.begin(), mov_det.end(), 0.0f)/N;
    flex_avg = accumulate(flex_det.begin(), flex_det.end(), 0.0f)/N;
    
    //Implement check
    if(idle){
        idle = (sqrt(abs(pow(flex_chk,2)-pow(flex_avg,2))) > (flex_chk*9/10)) && 
            (flex_det.size() >= N) ? false : true;
        if(!idle)
        {
            mov_chk = mov_det.back();
            flex_chk = flex_det.back();
            
            mov_det.clear();
            flex_det.clear();   
        }
    }
    /*
    if(!idle)
    {
        mov_chk = mov_det.back();
        flex_chk = flex_det.back();
        
        mov_det.clear();
        flex_det.clear();   
    }*/
    wait(0.1);
    }
            
    //return idle;   
}

void flip()
{
    readFlexSensor();
    readGyro();
    readAccel();
    readMag();
    readCap();
    led3 = !led3;
}

int main()
{
    setup();
    interrupt.mode(PullUp);
    //set pushbutton
    PB1.mode(PullUp);
    wait(3);

    //flipper.attach(&flip,1);   
    
    //Main loop
    while(1) {

//        Thread thread(checkIdle);    //Comment this out to resume data collection/testing and change if statement to "PB1 == 0"
        if (true) {
            char buffer[240];
            readFlexSensor();
            readGyro();
            readAccel();
            readCap();
            led3 = !led3;
            sprintf(buffer, "{\\\"data\\\" : [%1.5f, %1.5f, %1.5f, %1.5f, %1.5f, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %1.5f, %1.5f, %1.5f, %1.5f, %1.5f, %1.5f]}", 
                t_f, i_f, m_f, r_f, p_f, t_c, i_cu, i_cl, i_co, m_cu, m_cl, r_cu, r_cl, p_cu, p_cl, imu_ax, imu_ay, imu_az, imu_gx, imu_gy, imu_gz);
            command(buffer);
            //If data is not being received, add wait here and restart huzzah (unplug)
            //We must wait at least 600ms before sending again
            // pc.printf("\r\n");
            wait(0.7);
        }
        
      //  pc.printf("\r\nMov Avg: %0.5f\t\tFlex Avg: %0.5f\r\nMov Chk: %0.5f\t\tFlex Chk: %0.5f\r\nIdle? \"%d\"\r\n",
        //mov_avg, flex_avg, mov_chk, flex_chk, idle);
        //if(!idle) idle = true;
       // wait(1);
    }

}
