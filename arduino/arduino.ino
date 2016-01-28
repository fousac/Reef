#include <Wire.h> 
#include <LiquidCrystal_I2C.h>
#include <DS3232RTC.h>
#include <OneWire.h>
#include <DallasTemperature.h>
#include <SPI.h>
#include <Bridge.h>
#include <YunServer.h>
#include <YunClient.h>
#include <Console.h>

#define ONE_WIRE_BUS 37   // teplota

LiquidCrystal_I2C lcd(0x27, 2, 1, 0, 4, 5, 6, 7, 3, POSITIVE);
OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);
YunServer server;

byte minutaOld = -1;
byte minuta;
int TLAC_PODSVICENI = 30;
bool TLAC_PODSVICENI_STAV = TRUE;
int TLAC_REFRESH = 31;
bool TLAC_REFRESH_STAV = TRUE;

int pocetPristupu;
String teplota;
String cas;
String datum;

void setup()
{
  //setTime(1, 5, 00, 23, 01, 2016);   //set the system time to 23h31m30s on 13Feb2009
  //RTC.set(now()); 
  lcd_init();
  lcd.print("Startuji");

  setup_init();
  web_init();

  delay(500);
  lcd.clear();
}

void setup_init() {
  sensors.begin();  

  pinMode(TLAC_REFRESH, INPUT);
  pinMode(TLAC_PODSVICENI, INPUT);    

  Bridge.begin();
  Console.begin(); 

  
}

void loop()
{
  if (digitalRead(TLAC_PODSVICENI)) {
    TLAC_PODSVICENI_STAV = !TLAC_PODSVICENI_STAV;
    while (digitalRead(TLAC_PODSVICENI)) delay(50);
  }

  if (digitalRead(TLAC_REFRESH)) {
    TLAC_REFRESH_STAV = !TLAC_REFRESH_STAV;
    while (digitalRead(TLAC_REFRESH)) delay(50);
  }

  setSyncProvider(RTC.get);
  minuta = minute();
  if(minutaOld != minuta || TLAC_REFRESH_STAV) {
    sensors.requestTemperatures();
    teplota = String((int)floor(sensors.getTempCByIndex(0)))+"."+String((int)round(fmod(sensors.getTempCByIndex(0), 1)*10));    
    cas     = getCas(false);
    datum   = getDatum(true);
    Bridge.put("teplota", teplota);
    Bridge.put("cas", cas);
    Bridge.put("datum", datum);
  }  

  lcd_loop();
  web_loop();  

  if(minutaOld != minuta || TLAC_REFRESH_STAV) {
    minutaOld = minuta;
    TLAC_REFRESH_STAV = !TLAC_REFRESH_STAV;  
  }  
  
  delay(10);
} 

String getCas(bool sekundy)
{
  char oddelovac  = ':';
  int cas[3];
  String casString[3];
  
  cas[0] = hour();
  cas[1] = minute();
  cas[2] = second();

  for(int i = 0; i < 3; i++){
    if(cas[i] < 10) {
      casString[i] = "0" + String(cas[i]);
    } else {
      casString[i] = String(cas[i]);
    }
  } 

  if(sekundy) {
    return casString[0] + oddelovac + casString[1] + oddelovac +  casString[2]; 
  } else {
    return casString[0] + oddelovac + casString[1];
  }  
}

String getDatum(bool rok)
{
  char oddelovac  = '.';
  int datum[3];
  String datumString[3];
  
  datum[0] = day();
  datum[1] = month();
  datum[2] = year();

  for(int i = 0; i < 3; i++){
    if(datum[i] < 10) {
      datumString[i] = "0" + String(datum[i]);
    } else {
      datumString[i] = String(datum[i]);
    }
  } 

  if(rok) {
    return datumString[0] + oddelovac + datumString[1] + oddelovac +  datumString[2]; 
  } else {
    return datumString[0] + oddelovac + datumString[1];
  }  
}
