boolean readFromSerial; //Booléen pour autoriser la lecture des données depuis Serial

//Pour la séquence d'inspiration
boolean inspi = 0; //Détermine si le lapin doit inspirer ou pas
double fan_voltage = 0; //Tension à fournir au ventilateur

//Fréquences obtenues par la génération de données
double frequence_cardiaque;
double frequence_respiratoire;
double frequence_diurese;

//Traduction des fréquences en périodes utilisables ici
double periodeBattements; // = 150 tic * 4ms par tick / 1000 = 0.6 secondes
double periodeRespi;
double valeurseuil = 500;

int dureeBattement = 10;

//Lecture depuis Serial
boolean choixFrequence;
char ser;
String frequence_cardiaque_lue;
String frequence_respi_lue;

double pourcentage;


//Pour liaison série
const int len = 60;
char my_str[len];
char pos;

int incomingbyte = 0;


//Pour automate arduino
int enable_pin = 7; //Pin d'activation du compresseur
int dir_pin = 51;   //Pin de direction du compresseur
int valve_pin = 8;  //Pin de commande de l'électrovanne
int coeur = 53;
int buzzer = 10;

void setup() {
  Serial.begin(38400);
  
  pinMode(dir_pin, OUTPUT);
  digitalWrite(dir_pin,LOW); //on impose la direction à 0 (pas de changement de direction ici)
  
  pinMode(enable_pin, OUTPUT);
  analogWrite(enable_pin,200);

  pinMode(buzzer, OUTPUT);
  //digitalWrite(buzzer,155);
  
  pinMode(valve_pin, OUTPUT);
  
  pinMode(coeur, OUTPUT);
  


//Interruption
  cli(); // Désactive l'interruption globale
  bitClear (TCCR2A, WGM20); // WGM20 = 0
  bitClear (TCCR2A, WGM21); // WGM21 = 0 
  TCCR2B = 0b00000110; // Clock / 256 soit 16 micro-s et WGM22 = 0
  TIMSK2 = 0b00000001; // Interruption locale autorisée par TOIE2
  sei(); // Active l'interruption globale

  readFromSerial = 0; //Ne passe à 1 que lors de l'interruption

}

int varCompteur = 0; // La variable compteur pour l'interruption
int varCompteurEntreBattements = 0; //Interruption pour contrôler le moteur haptique
int varCompteurRespi = 0; //Interruption pour contrôler la respiratio
int valeurDiurese = 0;


// Routine d'interruption
ISR(TIMER2_OVF_vect) 
{
  TCNT2 = 256 - 248; // 250 x 16 µS = 4 ms

// Gestion du coeur avec le moteur haptique
  if (varCompteurEntreBattements++ == int(periodeBattements - dureeBattement) )
  {
    digitalWrite(coeur,HIGH); //Coeur on
  }
  if (varCompteurEntreBattements > periodeBattements )
  {
    varCompteurEntreBattements = 0;
    digitalWrite(coeur,LOW); //Coeur off
  }

//Gestion de la Diurèse avec le buzzer

// Gestion du poumon avec la valve et la pompe
  if (varCompteurRespi++ == int(periodeRespi/2))
  {
    analogWrite(enable_pin,0); //Expiration
    analogWrite(valve_pin,255); //On ouvre l'électrovanne pour laisser échapper l'air
    inspi = 0; //On termine la séquence d'inspiration
    fan_voltage = 0;
    
  }
  if (varCompteurRespi > periodeRespi)
  {
    inspi = 1; //On déclenche la séquence d'inspiration
    analogWrite(valve_pin,0); //On ferme l'électrovanne pour gonfler le poumon
    varCompteurRespi = 0;
  }

  if ((inspi == 1) && (fan_voltage < 255))
  {
    fan_voltage += 255.0/((1.0/5)*(periodeRespi)); //Calcul de la quantité à incrémenter la tension toutes les 4 ms pour obtenir un gonflement doux
    analogWrite(enable_pin,fan_voltage);  
  }
}

void serialEvent(){
  if (Serial.available() > 0){
    incomingbyte = Serial.read();
    my_str[pos] = incomingbyte;
    pos++;

    if(incomingbyte ==10){
      splitCommaSeparated();
      
      for (int i;i<=len-1; i++){
        my_str[i] = 0;
      }
      pos=0;
    } 
  }
}

void splitCommaSeparated(){
  char * param;
  int paramNum = 1;

  param = strtok(my_str,",\n");

  while (param != NULL)
  {
    processParam(param, paramNum);
    param = strtok(NULL,",\n");
    paramNum++;
  }
}

void processParam(char * param, int paramNum){
    if(paramNum == 1){
      frequence_cardiaque = atoi(param);
      periodeBattements = (60*1000.0)/(4*frequence_cardiaque);
      Serial.println("constantes cardiaques : ");
      Serial.print("frequence cardiaque : ");
      Serial.print(frequence_cardiaque);
      Serial.print("  -  periode des battements : ");
      Serial.println(periodeBattements);
    }
    if(paramNum == 2){
      frequence_respiratoire = atoi(param);
      periodeRespi = (60*1000.0)/(4*frequence_respiratoire);
      Serial.println("constantes respiratoire : ");
      Serial.print("frequence_respiratoire : ");
      Serial.print(frequence_respiratoire);
      Serial.print("  -  periode respiratoire : ");
      Serial.println(periodeRespi);
    }
        if(paramNum == 3){
      valeurDiurese = atoi(param);
      Serial.print("valeur diurese : ");
      Serial.print(valeurDiurese);
      if (valeurDiurese > valeurseuil) 
      {
        digitalWrite(buzzer,HIGH);
        delay(100);
        digitalWrite(buzzer,LOW);
      }

    }
}

void loop() {

}
