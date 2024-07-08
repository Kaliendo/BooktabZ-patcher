
# Patcher
Questo patcher è un'utility per alterare il normale funzionamento di BooktabZ.
Le funzioni offerte sono:

- Rimozione delle scadenze per ogni libro
- Rimozione delle analytics
- Riabilitazione di ogni libro scaduto
- Abilitazione della modalità sviluppatore

## Note
- Testato su BooktabZ dalla versione 4.12.1 alla 4.24.4485346 (attuale)
- Inizialmente era inclusa anche una funzione per estrarre la chiave blowfish in modo da rimuovere il DRM dai file, rimossa in questa release per evitare problemi :)
- Essendo questa una cosa fatta durante i miei anni alle superiori per puro divertimento (e perché mi risultava fastidiosissimo usare questo software invece di un pdf) non ci saranno update futuri

## Modalità Sviluppatore
La modalità sviluppatore offre diverse funzionalità selezionabili dal menù "Strumenti" e lascia aperto il server TCP utilizzato per la "rimozione" del DRM.

Durante l'avvio, viene aperto un server TCP abbinato a una porta casuale tramite le librerie di networking di Qt5. È possibile conoscere la porta utilizzata leggendo il file di debug presente alla path `C:\Users\{USER}\AppData\Local\Zanichelli\BooktabZ\debuglog.txt`.
Sarà presente una linea di questo tipo:
`Server is listening at port "http://localhost:{PORT}" "{PORT}"`

Quando dal software si richiede la pagina di un libro, viene effettuata una richiesta a `http://localhost:{PORT}/{PATH DEL FILE DA DECRIPTARE}` e come risposta verrà fornito il file in cleartext.

Normalmente (senza modalità sviluppatore attiva), il server accetta richieste solamente nell'arco di tempo in cui dal software viene richiesta una pagina e quest'ultima viene fornita in risposta, droppando eventuali altre richieste fatte dall'utente.
In modalità sviluppatore ciò non accade ed è quindi possibile effettuare richieste personalizzate.

## Come Utilizzare lo Script
1.  **Installazione delle Dipendenze**:
Installare le dipendenze richieste eseguendo il comando:
```bash
pip install -r requirements.txt
```
2.  **Esecuzione dello script**:

È importante aprire il prompt dei comandi con privilegi di amministratore, altrimenti non sarà possibile accedere ai file necessari, navigare nella directory dov'è presente lo script `patcher.py`.
Eseguire il seguente comando:
```bash
py patcher.py
```