void lcd_init() {
  lcd.begin(20,4);               // initialize the lcd   
  lcd.setCursor(0,0); //Start at character 0 on line 0
}

void lcd_loop() {
  if(TLAC_PODSVICENI_STAV) {
    lcd.backlight();
  } else {
    lcd.noBacklight();
  }
  if(minutaOld != minute() || TLAC_REFRESH_STAV) {
    lcd.clear();  
    lcd.setCursor(0,0);
    lcd.print(datum + "     " + cas);    
  
    lcd.setCursor(0,2);
    lcd.print("Teplota: " + teplota + (char)223 + "C");
  }  
}

