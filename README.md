![SwallowSpot logo](./static/images/swallowspot_title_mini.png)

# SwallowSpot - Documentazione
---
---
# Introduzione

Benvenuti su **SwallowSpot**!

Il luogo ideale per ottenere informazioni aggiornate sulle condizioni meteorologiche della Regione Veneto.

Questo sito sarà il vostro punto di riferimento per accedere ai bollettini meteo ufficiali pubblicati dalla regione, garantendo così una visione chiara e completa delle previsioni e delle eventuali allerte presenti.

Il sito si occupa di monitorare diverse tipologie di situazioni meteorologiche che possono influenzare il territorio veneto, tra cui **nevicate**, situazioni **idrauliche** e **idrogeologiche**, nonché allerte specifiche legate ai **temporali**.

Grazie alla classificazione in quattro colori distinti - **Verde**, **Giallo**, **Arancione** e **Rosso** - potrà essere immediatamente valutato il livello di rischio associato a ciascuna situazione.

---
# Frontend

## Stile del sito

![color palette](./static/images/swallowspot_palette.png)
![swallow](./static/images/swallowspot_swallow.png)

La scelta della palette di colori blu e azzurro è stata finemente studiata, perché colori che trasmettono affidabilità e sicurezza, inoltre ricordano il colore di un cielo.

Inoltre la scelta della rondine come simbolo principale è data dal fatto che essa sia un animale dal facile adattamento e soprattutto dalla sua abilità di percepire i pericoli imminenti, cosa che caratterizza anche il nostro sito.

Per far si che l'intero progetto sia utilizzabile anche da dispositivi mobili è stato fatto utilizzo della libreria di stile Boostrap, che ha facilitato le operazioni per la realizzazione della responsività.

## Pagine

### Home page

Contiene tutti i link principali utili alla navigazione all'interno del sito. Inoltre riporta l'ultimo bollettino riguardante la zona specifica dell'utente attualmente registrato, oltre che presentare una descrizione generale del servizio.

### Ultimi bollettini

Questa pagina è divisa in due sezioni:

1. Bollettini idraulici
2. Previsioni sulle nevicate

La prima sezione contiene i bollettini **idraulici**, **idrogeologici** e **idrogeologici per temporali** relavivi a tutte le zone del Veneto (*VENE*) con tanto di colorazione specifica per ogni tipo di rischio:

- **Verde** - Livello di criticità non presente (Normalità): nessuna criticità prevista
- **Giallo** - Livello di criticità ordinaria (Fase di Vigilanza): assegnata a eventi minori, di difficile localizzazione e previsione temporale
- **Arancione** - Livello di criticità moderata (Fase di Attenzione): associata a fenomeni con possibili effetti sulla stabilità di versanti montani e sui corsi d'acqua
- **Rosso** - Livello di criticità elevata (Fase di Pre Allarme): associata a fenomeni di particolare intensità con conseguenti effetti al suolo rilevanti
- **Viola** - Livello di criticità molto elevata (Allarme): solitamente non visibile, utilizzata solo in caso di estrema emergenza

La seconda sezione invece, riporta le previsioni sulle nevicate relative al giorno stesso dell'uscita del bollettino, comprendendo i due giorni seguenti. Riporta in alto la percentuale di probabilità che si verifichi il fenomeno, mentre sotto sono presenti i centimetri previsti intorno a diversi livelli di altitudine, quali:

- 1000m
- 1500m
- 2000m e maggiori

Inoltre sul lato della pagina è presente un tasto per aprire un calendario (realizzato con l'aiuto della libreria Flatpickr) che permette di visualizzare e consultare i bollettini rilasciati in tutte le date precedenti, con la possibilità di scaricare il file PDF corrispondente.

### Info e legende sui rischi

Pagina informativa contenente tutte le informazioni relative ai rischi riportati nel sito e come leggere correttamente i dati, oltre che alle legende sui vari colori e misure.

### Profilo e impostazioni

In questa pagina è possibile modificare le proprie credenziali, comprendendo:

- Nome utente
- Password
- Città di residenza

È inoltre possibile effettuare l'eliminazione il proprio account.

Più in basso è invece presente uno switch che permette di cambiare la modalità di visualizzazione del tema del sito da chiaro a scuro.

### Sezione Admin

Se si è in possesso dei permessi amministrativi è possibile vsualizzare un ulteriore pulsante che dà accesso ad una pagina riservata agli amministratori. Qui le azioni possibili sono le seguenti:

- Caricamento manuale di PDF contenenti i bollettini
- Collegamento al proprio account Telegram ed ad un relativo gruppo, tramite inserimento dei rispettivi *chat_id*, in modo da collegarli con il **Bot Telegram** che invierà le notifiche in caso di allerta
- La possibilità di creare un nuovo utente amministratore da zero nel caso in cui ci fosse bisogno di assegnare un account ad un eventuale nuovo operatore. Oppure si può aggiungere tra gli amministratori un account già registrato in precedenza, nel caso un operatore si fosse creato autonomamente un nuovo profilo

È presente poi, per gli utenti aventi i permessi da **Super Amministratore**, un'ulteriore sezione dove è possibile effettuare un backup del database inserendo l'indirizzo IP della macchina su cui si vuole effettuarlo. Sotto ciò, si trova un pulsante per attivare e disattivare la modalità di **manutenzione**, che rende il sito inaccessibile a tutti coloro che non posseggono il ruolo da Super Amministratore (da utilizzare nei casi in cui siano necessarie modifiche al database o a parti specifiche dell'interfaccia).

### Snake Game

Nel menu laterale (o nella pagina di manutenzione) è presente un pulsante che conduce ad una pagina dedicata in cui giocare a **Snake**.

### Error 404

Abbiamo voluto personalizzare anche la pagina di errore in caso di pagine non trovate.

## Cookies

La creazione dei **Cookies** avviene attraverso funzioni JavaScript richiamate attraverso dei bottoni nel file *button.js*.

### Scelte dell'utente

La gestione delle scelte dell’utente avviene in un label che viene visualizzato se l’utente non ha mai effettuato l’accesso al sito. Questa verifica avviene tramite una funzione JavaScript situata in *layout.html*, in modo da essere accessibile in tutte le pagine del sito, con il confronto di una variabile nel localstorage.

### Informativa sulla privacy

Come sancito dal GDPR (Regolamento generale sulla protezione dei dati) ogni sito che utilizza gestisce dati sensibili deve stilare un'informativa visibile nel sito. Perciò è stato stilato un testo “*ad hoc*” per il sito, spiegando le finalità e le tecniche di archiviazione dei dati degli utenti. Seppur, esplicitamente, il sito non riferisca alcuna necessità di dato sensibile per l’archiviazione.

## Snake

### Descrizione

Il gioco **Snake** è stato sviluppato utilizzando HTML, CSS e JavaScript. Il gioco è progettato per essere giocato sia su dispositivi desktop che mobili, tramite la rilevazione automatica che adatta i controlli di conseguenza. Esso include una funzione di salvataggio del punteggio più alto effettuato dall’utente utilizzando il local storage del browser.

### Caratteristiche e funzionalità

#### Compatibilità multi-device e responsività

Tramite 3 controlli in JavaScript viene rilevato se il dispositivo è un dispositivo mobile oppure desktop. 
Il primo controllo rileva se il dispositivo supporta il *multi touch*.   
Il secondo controllo verifica se il dispositivo supporta il touch utilizzando una combinazione di "*ontouchstart*" in finestra e l'interfaccia *DocumentTouch*.   
Il terzo controllo invece si basa sulla larghezza del dispositivo. Se almeno in 2 dei 3 controlli risulta che il dispositivo supporta la tecnologia touchscreen, allora viene predisposto l’ascolto per i movimenti tramite lo swipe del dito.
Nel caso in cui i controlli rilevano che il dispositivo è di tipo desktop, i movimenti dello snake avverranno tramite la rilevazione degli input della tastiera.

#### Snake & food

Lo snake viene sempre generato al centro del campo di gioco, mentre il cibo viene generato casualmente, tranne nelle posizioni in cui vi è presente lo snake.

#### Salvataggio del punteggio personale

Il punteggio che l'utente ottiene viene confrontato con il punteggio più alto salvato nel local storage del browser. Nel caso in cui il nuovo punteggio superi quello salvato in memoria, allora viene sostituito altrimenti rimane inalterato.

#### Fine della partita

La partita può terminare in 2 occasioni:

- la prima se lo snake effettua una collisione contro se stesso;
- la seconda se lo snake va a collidere nei bordi del campo di gioco;

In questi casi la partita termina e viene mostrato un messaggio di fine partita e il punteggio che l’utente ha ottenuto.

#### HTML

Utilizzato per l'interfaccia utente che include una sezione per mostrare il punteggio corrente e il punteggio più alto, l'area di gioco principale e una schermata di Game Over.

#### JavaScript

Utilizzato per tutti i controlli sullo snake, sulle sue collisioni, sul cibo che viene generato casualmente (ma non dove vi è lo snake), aggiunta del corpo dello snake man mano che la partita prosegue, gestione movimenti dello snake, sia con gli input da tastiera, che con gli input touch.

#### CSS

Gli stili CSS sono stati utilizzati per creare un layout gradevole, le griglie CSS sono state impiegate per organizzare l'area di gioco, e le *media query* assicurano che il gioco sia ben visualizzato su dispositivi di diverse dimensioni.

---
# Backend

## Flask views

### App.py

Per avere un migliore ordine del codice il routing flask è diviso tramite l'utilizzo delle Blueprint.
Quindi in app.py sono presenti solo le chiamate alle Blueprint e le pagine per manutenzione e errore 404.

### Home

Home contiene il routing per:
- La pagina home
- La pagina snake
- Le principali richieste ajax(es. richiesta delle città per registrazione)

### Auth

Contiene le pagine per il login e il signup.

### Profile

Contiene le pagine per il profilo, compresa quella per l'admin.

### Reports

Contiene le pagine per i report più le funzioni utilizzate solo in quelle pagine.

### Info

Contiene la pagina di informazioni.

## Utils

In utils sono contenute i moduli usati in più file, in questo modo possono essere importati in altre parti del progetto.

### cfd_analyzer

Cfd analazyer viene utilizzato per leggere i bollettini. Per fare ciò basta istanziare una oggetto Pdf_reader, nel quale verranno eseguiti i controlli per vedere se il bollettino riguarda una nevicata o un rischio idrico.

In base al tipo di rischio verrà istanziata un'altro ogetto Snow o Hydro, in entrambe le classi sono scritte le funzioni che permettono di:

- Leggere il pdf tramite libreria camelot
- Inserire i dati ottenuti in un dizionario che segua la forma risk_templates_hydro.json o risk_template_snow.json
- Aggiungere i dati nel database

### DB backup

Funzioni per il backup del database, spiegato nella parte di Database.

### bulletins_utils

Funzioni per la lettura dei bollettini, sia per mail che inseriti manualmente.

Utilizza la classe **Pdf_reader** e salva i bollettini in static/bulletins in modo che possano essere scaricati.
In questo modulo sono presenti anche le funzioni che controllano che i bollettini sono abbiano lo stesso nome e la gestione degli errori riguardante la lettura dei bollettini.

### get_data

Richieste al database che venivano utilizzate in più views come la conversione delle date.

### password

Funzioni riguardanti l'hash i controlli delle password.

### risks

Richieste al database e conversioni riguardanti i rischi, utilizzati sia nella view report che in cfd_analyzer.

## Models

Contiene il Database Model, utilizzato per connettersi ed eseguire query con il Database

**Ogni singola funzione di utils è spiegata in maniera approfondita nella sua docstring**

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

## Creazione applicativo per scaricare le email e estrapolare gli allegati PDF

Con la libreria ***Imaplib*** è stato creato un applicativo *Python* che, attraverso un autenticazione specifica, tramite la creazione di un’*APP password* (funzionalità di Google), accede alla casella di posta "*swallowspottesting@gmail.com*" adibita alla ricezione delle e-mail contenenti gli allegati dei bollettini e ne scarica il contenuto affinché possa essere elaborato per le letture dei dati nei PDF. Inoltre è stata aggiunta una lista di indirizzi e-mail consentiti, i quali vengono confrontati con i sender delle mail per validarne la provenienza, scartando ed eliminando qualsiasi mail sia già stata letta o che non sia non valida.

## Sistema di backup

### Ideazione

Il sistema di **Backup** è stato creato per garantire l'affidabilità del DataBase le cui informazioni sono soggette a molteplici minacce come la cancellazione involontaria o la rottura dei supporti di memorizzazione. Per ovviare a questo problema abbiamo voluto ideare un programma che sfrutta la tecnologia client-server per inviare e ricevere il file con la copia del DataBase, un file SQL dove sono contenuti strutture delle tabelle e dati contenuti in esse.
Per garantire la sicurezza e l’integrità del trasferimento dei dati è stata utilizzata la libreria ***OpenSSL*** per la generazione dei **certificati crittografati** e un controllo aggiuntivo sulla dimensione del file alla sua ricezione.

### Implementazione

I due programmi, *client_backup.py* e *server_backup.py*, effettuano un collegamento tramite **Socket TCP SSL** all'interno del quale avviene l'invio del file *.SQL* contenente il backup dell’intero database.
Il backup viene ottenuto mediante un comando dalla shell di Linux eseguita direttamente dal programma client nel server di Swallow Spot e genera un file con le ultime modifiche del DB.
Nel programma *server_backup.py*, eseguito sulla macchina remota dove eseguire il backup, sarà necessario importare il file con i certificati necessari per la connessione.
Una volta eseguito il programma sarà possibile effettuare il backup dal pannello di amministrazione del sito inserendo il corretto indirizzo IP e Porta logica del socket a cui connettersi.

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
# Possibili migliorie

- Aggiunta della verifica a due fattori per il recupero della password tramite e-mail.
- Migliore interfaccia di cambio credenziali all'interno del profilo e aggiunta di azioni e/o personalizzazioni.
- Aggiungere i bollettini sulle valanghe o di altri tipi.
- Implementare una classifica globale dei giocatori di Snake ed eventuale gestione di essa quando l'utente è offline.

---
# Link utili

[GitLab](https://git.e-fermi.it/s02599/swallowspot)   
[Grafico di Gantt](https://docs.google.com/spreadsheets/d/168YbsE5HJkgGRd5wHwkwUqBXXFXx9UqvABOlmpB-spY/edit?usp=sharing)   
[Meeting formalizzati](https://docs.google.com/document/u/0/d/1sRinEKfY7cUU00rmCMdOnxzq7RYrK_BtL3HxiMQvskY/edit)   
[Monte ore](https://docs.google.com/spreadsheets/u/0/d/1Xwgcuj6wsa1bmwlAo48x7urjbYj1wkDkMTtX7W9GGvQ/edit)   
[WBS](https://drive.google.com/file/d/1tl7dMJODTsOtKm8gPWkH-u98CW3RowVA/view?usp=sharing)   
[Project charter](https://docs.google.com/document/d/1s2t6DxKhILbeoxKxMlY8qBP8z9xPnwOq/edit?usp=sharing&ouid=108176821754793768186&rtpof=true&sd=true)   
[Informativa sulla privacy e sul trattamento dei dati personali](https://docs.google.com/document/d/1zuJWILUF4c712sJ3IW12un4LcLxyTNlbb49vMByV4iM/edit?usp=sharing)   
[Skill management](https://docs.google.com/document/d/1PyCQIAEj1DmMwY9xT3W8IKJT0NQssDxHBKveqqW169w/edit?usp=sharing)

# Crediti

*A questo Progetto hanno preso parte: Degetto Tommaso, La Rosa Leonardo, Maggiotto Giacomo, Martini Davide, Stefani Marco, Tosin Filippo.*