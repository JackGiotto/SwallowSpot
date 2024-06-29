# GUIDE TO LOCAL CONFIGURATION OF A SWALLOWSPOT SERVER

## Code repository

### Cloning repository

Run `git clone https://github.com/JackGiotto/SwallowSpot`

### User configuration

`git config user.name <github username>`

`git config user.email <github @users.noreply email>`

You can find your @users.noreply email in [settings](https://github.com/settings/emails)

### Creation of virtual environment
- For Windows `python -m venv venv`

- For Linux and macOS `python3 -m venv venv`

If you are running it from vs-code it will appear a pop-up saying that a virtual enviornment has beeen noticed, click yes

If it does not appear run:

- For Windows `.\venv\Scripts\activate`

- For Linux and macOS `source venv/bin/activate`

You can exit from virtual environment using `deactivate`

**In case you clicked yes on vs-code pop-up it should automatically enter in the virtual enviornment from now on, in other case you should always enter with the previous commands**


### Libraries installation
Make sure to start the virtual enviornment and run:

`pip install -r requirements.txt`

### Updating requirements file
If you download any other python library you can update the requirements file by running:

`pip freeze > requirements.txt`

## Database

### Database creation

Run apache and mysql from xampp console and then enter from a browser  [myadmin console page](http://localhost/phpmyadmin/).

Here create a new DB called swallowspot.

Inside the database page go to import page and import the backup file of the database.

### .env configuration

Inside SwallowSpot folder create a new file called .env and copy-paste the contents of .env.example.

Now compile .env

    SERVERNAME="localhost"
    DBUSER=[name of your database user]
    DBNAME="swallow spot"
    PASSWORD=[password of yout database user]
    PORT=5000
    BULLETINS_FOLDER="./static/bulletins"
    MAIL=""
    MAILPASSWORD=""
    IMAPSERVER=""

##### (In next meeting will be decided what to do for mail testing)

You can create new users and change current users password in [users page](http://localhost/phpmyadmin/index.php?route=/server/privileges&viewing_mode=server)

## Running

now you can run the server with
`python app.py`

### !Attention!

make sure that in main file ssl is not activated or the page will not be accessible (this is only for localhost)