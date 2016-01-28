void web_init() {
  server.listenOnLocalhost();
  server.begin();  
}

void web_loop() {
  YunClient client = server.accept(); //check new clients
  String msg;
   
  if(client) {
    client.setTimeout(5);    
    String command = client.readString();
    command.trim();
    Console.println("prikaz: "+command);
    if (command == "msg") {      
       msg = client.readStringUntil('/');             // read the incoming data
       client.print("ahoj");       
       Console.println("zprava: "+msg);
    }
    
    if (command == "getCas") {      
       client.print(cas);       
    }   

    if (command == "getDatum") {      
       client.print(datum);       
    }       

    if (command == "getTeplota") {      
       client.print(teplota);       
    }     
    client.stop();   
  } 

}

