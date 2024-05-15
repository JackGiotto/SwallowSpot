![SwallowSpot logo](./static/images/swallowspot_footer_icon.png)

# SwallowSpot - Documentazione
---
---
# Introduzione

---
# Frontend

---
# Backend

## Database


### Richieste della consegna

Realizzare un database che contenga le seguenti informazioni: 
- Path dei file dei bollettini nel server
- Storico dei rischi nella zona di Bassano
- Dati relativi agli utenti che si registrano
- Diversi ruoli per admin e utenti normali

Il sito web deve permettere: 
- Registrazione, attraverso nome utente, password, zona in cui si vive
- Possibilità per gli utenti registrati di scaricare l'ultimo bollettino
- Possibilità per gli utenti di ricevere una notifica in caso la loro zona sia a rischio
- Possibilità di filtrare per zona e vedere lo storico dei rischi di quella zona (Esempio: Vene-B 12/06 rischio idraulico giallo, 14/06 rischio idrogeologico giallo, ecc…)
- Possibilità di filtrare per giorni (che rischi ci sono stati il 14/06?) e tabella riguardo all'ultimo bollettino per quel giorno 
- Possibilità di filtrare per tipo di rischio
- Gestione bollettini per neve e gelate

Lato admin: 
- Può interfacciarsi con il sito per ricevere tramite un bot telegram un messaggio che andrà poi mandato nel canale telegram del comune. L'admin inserirà un contatto telegram al quale 	verrà mandato il messaggio da parte del server il quale potrà essere modificato dall'admin (o accettato/rifiutato) 
- Cancellare o creare nuovi account admin (Tenendo di conto account super admin nostro)
- Può caricare eventuali nuovi bollettini che non arrivano in maniera automatica dal server 

### Richieste da parte dei colleghi

- Elenco delle città insieme alle relative zone di appartenenza per dare all'utente uno schema di riferimento per quanto riguarda la propria area di rischio
- Elenco degli ID assegnati dai bot di Telegram relativi solamente agli admin
- Sapere quali dati preleviamo dagli utenti per indicare all’interno dell’informativa dei cookie
- Separare i bollettini riguardanti rischi idraulici e idrogeologici da quelli per neve e valanghe

### Considerazioni

Dalle seguenti richieste possono derivare le seguenti entità (relazioni):
1. **Area** (zona)
2. **Risk** (rischio)
3. **Role** (ruolo)
4. **Color** (colore)
5. **Altitude** (altitudine)
6. **Report** (bollettino)
7. **Criticalness** (criticità prevista)
8. **Snow_report** (bollettino rischi per neve)
9. **Snow_criticalness** (criticità prevista per neve)
10. **Topology** (topologia)
11. **User** (utente)
12. **Admin** (utente amministratore)

I nomi delle tabelle saranno indicati al singolare per rendere più immediata la lettura.

Nella relazione **Area** verranno inseriti i dati relativi alle zone:
- ***ID_area***: codice identificativo delle zone
- *area_name*: nome della zona divisa dai bollettini

Nella relazione **Risk** verranno inseriti i dati relativi ai rischi possibili:
- ***ID_risk***: identificatore univoco associato ad ogni rischio
- *risk_name*: nome del rischio

Nella relazione **Role** verranno raccolti i dati relativi ai ruoli quindi:
- ***ID_role***: codice univoco assegnato ad ogni ruolo
- *role_name*: nome del ruolo (admin, super-admin)

Nella relazione **Color** verranno raccolti i vari colori possibili da presentare nelle criticità:
- ***ID_color***: codice colore
- *color_name*: nome del colore

Nella relazione **Altitude** verranno raccolte le varie altitudini possibili presenti nelle criticità per neve:
- ***ID_altitude***: codice altitudine
- *height*: valore dell’altezza

Nella relazione **Report** verranno raccolti i dati relativi ad ogni bollettino come:
- ***ID_report***: codice univoco per ogni bollettino
- *starting_date*: data di inizio della presenza dei rischi
- *ending_date*: data di fine della presenza dei rischi
- *path*: percorso del bollettino nel server

Nella relazione **Criticalness** verranno raccolti i dati relativi alle criticità previste in un determinato bollettino:
- ***ID_issue***: codice univoco relativo alla criticità
- *ID_area*: codice della zona dei bollettini (presa da **Area**)
- *ID_risk*: codice del tipo di rischio (preso da **Risk**)
- *ID_color*: codice del colore (preso da **Color**)
- *ID_report*: codice del bollettino (preso da **Report**)

Nella relazione **Snow_report** verranno raccolti i dati relativi ad ogni bollettino per le aree di montagna a rischio come:
- ***ID_snow_report***: codice univoco per ogni bollettino
- *date*: data di inizio della presenza dei rischi
- *path*: percorso del bollettino nel server

Nella relazione **Snow_criticalness** verranno raccolti i dati relativi alle criticità previste in un determinato bollettino:
- ***ID_snow_issue***: codice univoco relativo alla criticità per neve
- *date*: data di inizio della presenza del rischio per neve
- *percentage*: valore della percentuale del livello di neve
- *ID_area*: codice della zona dei bollettini (presa da **Area**)
- *ID_snow_report*: codice del tipo di rischio (preso da **Snow_report**)

Nella relazione **Topology** verranno inseriti i dati relativi alle città e alle zone corrispondenti:
- ***ID_city***: codice univoco della città
- *city_name*: nome della città (univoca)
- *ID_area*: codice che identifica la zona (presa da **Area**)

Nella relazione **User** verranno raccolti tutti i dati relativi agli utenti tra cui: 
- ***ID_user***: identificativo univoco assegnato ad ogni utente 
- *username*: nome che l'utente sceglie ma che deve essere univoco
- *password*: hash a 64 bit della password dell'utente
- *ID_area*: zona in cui l’utente vive (presa da **Area**)
- *ID_role*: codice del ruolo dell’utente all’interno del sito (preso da **Role**)


Nella relazione **Admin** verranno raccolti i dati relativi agli admin tra cui:
- ***ID_telegram***: identificativo univoco raccolto per inviare messaggi su Telegram
- *groupID*: identificativo univoco del gruppo su Telegram
- *ID_user*: identificativo univoco dell’utente assegnato dal DB (preso da **User**)

Alcune entità sono nella forma ID_entità - nome_entità per favorire la gestione, la successiva normalizzazione e integrità referenziale.

### Ristrutturazione

Prima di procedere con la progettazione logica il diagramma E-R è stato ristrutturato in modo tale da essere rappresentabile anche all’interno del modello logico. In particolare è stata semplificata l’associazione molti a molti presente tra ***Snow_criticalness*** e ***Altitude*** con due associazioni uno a molti e una nuova entità ponte ***Snow_criticalness_altitude***.

Lo schema concettuale non necessità di altre modifiche dal momento che è stato progettato con un'ottica che tiene già in considerazione i limiti dello schema logico.
Nello schema difatti non erano presenti attributi multipli, composti, ridondanze, gerarchie o specializzazioni.

### Progettazione logica

In questa fase andremo a definire lo schema logico che evidenzia tutte le associazioni presenti all’interno del nostro database.

1. ***Area*** (**ID_area(PK)**, area_name)
2. ***Risk*** (**ID_risk(PK)**, risk_name)
3. ***Role*** (**ID_role(PK)**, role_name)
4. ***Color*** (**ID_color(PK)**, color_name)
5. ***Altitude*** (**ID_altitude(PK)**, height)
6. ***Report*** (**ID_report(PK)**, starting_date, ending_date, path)
7. ***Criticalness*** (**ID_issue(PK)**, ID_area(FK1), ID_risk(FK2), ID_color(FK3), ID_report(FK4))
    1. ID_area FK1 references to ***Area***.ID_area
    2. ID_risk FK2 references to ***Risk***.ID_risk
    3. ID_color FK3 references to ***Color***.ID_color
    4. ID_report FK4 references to ***Report***.ID_report
8. ***Snow_report*** (**ID_snow_report(PK)**, date, path)
9. ***Snow_criticalness*** (**ID_snow_issue(PK)**, date, percentage, ID_area(FK1), ID_snow_report(FK2))
    1. ID_area FK1 references to ***Area***.ID_area
    2. ID_report FK2 references to ***Snow_report***.ID_snow_report
10. ***Topology*** (**ID_city(PK)**, city_name, ID_area(FK1))
    1. ID_area FK1 references to ***Area***.ID_area
11. ***User*** (**ID_user(PK)**, username, password, ID_area(FK1), ID_role(FK2))
    1. ID_area FK1 references to ***Area***.ID_area
    2. ID_role FK2 references to ***Role***.ID_role
12. ***Admin*** (**ID_telegram(PK)**, groupID, ID_user(FK1))
    1. ID_user FK1 references to ***User***.ID_user
13. ***Snow_criticalness_altitude*** (**ID_snow_issue (PK, FK1)**, **ID_altitude (PK, FK2)**)
    1. ID_snow_issue FK1 references to ***Snow_issue***.ID_report
    2. ID_altitude FK2 references to ***Altitude***.ID_altitude

### Normalizzazione

Durante il processo di costruzione concettuale del DataBase si è tenuto conto della possibilità di evitare la creazione di dipendenze funzionali o dipendenze funzionali transitive.
Le relazioni rispettano già la prima forma normale perché esiste una chiave primaria per ogni tabella e non ci sono attributi composti.
Le relazioni rispettano anche la seconda forma normale perché non sono presenti dipendenze funzionali dal momento che le possibili dipendenze sono state separate a priori, durante la modellazione concettuale, in tabelle separate.
Le relazioni rispettano anche la terza forma normale perché non esistono dipendenze funzionali transitive, tutti gli attributi dipendono interamente dalla chiave primaria.

---
# Bot Telegram

## Introduzione

Il **Bot Telegram** serve a mandare in modo automatico l’ultimo bollettino sia delle nevicate sia idrogeologico via messaggi Telegram solo per gli admin con la possibilità di inoltrare o cancellare il messaggio di allerta ricevuto; inoltre il **Bot Telegram** via chat privata offre la possibilità di effettuare un controllo manuale dell'ultimo bollettino caricato nel database.

## Funzionalità principali

### Invio automatico dei messaggi

Il Bot è configurato per inviare automaticamente messaggi ad un gruppo Telegram specifico. Utilizzando il *chat ID* del gruppo e un sistema di programmazione temporale, il bot può recapitare i messaggi in modo preciso e tempestivo.

### Gestione dei messaggi ricevuti

Il Bot è programmato per gestire diversi comandi tra cui anche bottoni dall’utente telegram:
1. un bottone  che comparirà con il comando `/start` serve per dare all’utente il suo *chat_id* per poi avere i privilegi di usare il Bot 
2. nella chat privata dopo aver collegato il Bot con il proprio account Telegram dal sito si potrà effettuare un controllo manuale dei tipi di bollettini dal database
3. il secondo è un comando che deve essere inviato nel gruppo Telegram che l’utente deve creare aggiungendo anche il Bot per scoprire il *chat_id* del gruppo Telegram sempre per ricevere l’invio delle allerte automatiche da parte del Bot Telegram
4. inoltre se l’utente non avrà collegato l'account Telegram con il suo account del sito non potrà usare nessun servizio del Bot Telegram

### Inoltro del messaggio

Quando nel bollettino per la zona interessata del bot telegram ci sarà un colore di allerta il bot inviare a tutti gli admin che hanno collegato il Bot riceveranno nel gruppo Telegram un messaggio con descritta il colore e la tipologia di allerta e sotto a questo messaggio ci saranno due bottoni con i quali l’admin potra decidere se inoltrare il messaggio ad il gruppo impostato o eliminare il messaggio

### Implementazione tecnica

Il Bot Telegram è stato sviluppato utilizzando le API di Telegram con il linguaggio di programmazione Python. È stato configurato per interagire con il server Telegram, utilizzando il *chat ID* per identificare gli utenti e i gruppi. Le funzionalità di invio automatico e di gestione dei messaggi sono state implementate attraverso script di automazione che elaborano i comandi degli utenti e inviano le risposte appropriate.

### Conclusioni

In conclusione, il Bot Telegram creato rappresenta un'efficace risorsa per mantenere gli utenti informati in modo tempestivo su nevicate e rischi idrogeologici. Grazie alla sua capacità di inviare automaticamente messaggi nei gruppi Telegram designati e di gestire i comandi degli utenti, offre un sistema efficiente per la diffusione delle informazioni critiche. L'implementazione tecnica utilizzando le API di Telegram e Python garantisce un funzionamento affidabile e stabile. Inoltre, la possibilità per gli amministratori di inoltrare o eliminare gli avvisi ricevuti aggiunge un livello di personalizzazione e controllo alla gestione dei messaggi. Nel complesso, il Bot si presenta come uno strumento indispensabile per migliorare la comunicazione e la condivisione di contenuti all'interno delle comunità online.

---
# Link utili

[GitLab](https://git.e-fermi.it/s02599/swallowspot)   
[Grafico di Gantt](https://docs.google.com/spreadsheets/d/168YbsE5HJkgGRd5wHwkwUqBXXFXx9UqvABOlmpB-spY/edit?usp=sharing)   
[Meeting formalizzati](https://docs.google.com/document/u/0/d/1sRinEKfY7cUU00rmCMdOnxzq7RYrK_BtL3HxiMQvskY/edit)   
[Monte ore](https://docs.google.com/spreadsheets/u/0/d/1Xwgcuj6wsa1bmwlAo48x7urjbYj1wkDkMTtX7W9GGvQ/edit)   
WBS   
PRENT   
[Project charter](https://docs.google.com/document/d/1s2t6DxKhILbeoxKxMlY8qBP8z9xPnwOq/edit?usp=sharing&ouid=108176821754793768186&rtpof=true&sd=true)   
[Informativa sulla privacy e sul trattamento dei dati personali](https://docs.google.com/document/d/1zuJWILUF4c712sJ3IW12un4LcLxyTNlbb49vMByV4iM/edit?usp=sharing)   
[Skill management](https://docs.google.com/document/d/1PyCQIAEj1DmMwY9xT3W8IKJT0NQssDxHBKveqqW169w/edit?usp=sharing)

# Crediti

*A questo Progetto hanno preso parte: Degetto Tommaso, La Rosa Leonardo, Maggiotto Giacomo, Martini Davide,Stefani Marco, Tosin Filippo.*