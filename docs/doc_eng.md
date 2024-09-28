![SwallowSpot logo](../static/images/swallowspot_title_mini.png)

# SwallowSpot - Documentation
---
---
# Introduction

Welcome to **SwallowSpot**!

The ideal place to get updated information on the weather conditions in the Veneto Region.

This site will be your reference point for accessing the official weather bulletins published by the region, ensuring a clear and comprehensive view of the forecasts and any alerts present.

The site monitors various types of weather situations that can affect the Veneto territory, including **snowfalls**, **hydraulic** and **hydrogeological** situations, as well as specific alerts related to **thunderstorms**.

Thanks to the classification into four distinct colors - **Green**, **Yellow**, **Orange**, and **Red** - you can immediately assess the risk level associated with each situation.

---
# Frontend

## Site Style

![color palette](../static/images/swallowspot_palette.png)
![swallow](../static/images/swallowspot_swallow.png)

The choice of the blue and azure color palette has been carefully studied because these colors convey reliability and safety, and they also remind one of the color of the sky.

Additionally, the choice of the swallow as the main symbol is due to the fact that it is an animal that easily adapts and, above all, has the ability to perceive imminent dangers, which also characterizes our site.

To ensure that the entire project is usable on mobile devices, the Bootstrap style library was used, facilitating operations for achieving responsiveness.

## Pages

### Home Page

Contains all the main links useful for navigation within the site. It also shows the latest bulletin concerning the specific area of the currently registered user, as well as presenting a general description of the service.

### Latest Bulletins

This page is divided into two sections:

1. Hydraulic Bulletins
2. Snowfall Forecasts

The first section contains **hydraulic**, **hydrogeological**, and **hydrogeological for thunderstorms** bulletins related to all areas of Veneto (*VENE*) with specific coloring for each type of risk:

- **Green** - No criticality level (Normality): no criticality expected
- **Yellow** - Ordinary criticality level (Surveillance Phase): assigned to minor events, difficult to locate and predict temporally
- **Orange** - Moderate criticality level (Attention Phase): associated with phenomena with possible effects on the stability of mountain slopes and watercourses
- **Red** - High criticality level (Pre-Alarm Phase): associated with particularly intense phenomena with significant effects on the ground
- **Purple** - Very high criticality level (Alarm): usually not visible, used only in case of extreme emergency

The second section reports the snowfall forecasts for the day the bulletin is issued, including the following two days. It shows the probability percentage of the phenomenon occurring at the top, while below are the predicted centimeters around different altitude levels, such as:

- 1000m
- 1500m
- 2000m and higher

Additionally, on the side of the page, there is a button to open a calendar (created with the help of the Flatpickr library) that allows viewing and consulting bulletins released on all previous dates, with the option to download the corresponding PDF file.

### Info and Legends on Risks

An informational page containing all the information related to the risks reported on the site and how to correctly read the data, as well as the legends on various colors and measures.

### Profile and Settings

On this page, you can modify your credentials, including:

- Username
- Password
- City of residence

It is also possible to delete your account.

Further down, there is a switch to change the site's theme display mode from light to dark.

### Admin Section

If you have administrative permissions, an additional button is visible that gives access to a page reserved for administrators. Here, the possible actions are:

- Manual uploading of PDF bulletins
- Linking to your Telegram account and a related group by entering their respective *chat_id*, to connect them with the **Telegram Bot** that will send notifications in case of an alert
- The ability to create a new administrator user from scratch if there is a need to assign an account to a new operator. Alternatively, you can add an already registered account to the administrators if an operator has created a new profile autonomously

There is also, for users with **Super Administrator** permissions, an additional section where you can perform a database backup by entering the IP address of the machine where you want to perform it. Below this, there is a button to activate and deactivate **maintenance** mode, which makes the site inaccessible to all except those with the Super Administrator role (to be used when database or specific interface modifications are necessary).

### Snake Game

In the side menu (or on the maintenance page), there is a button leading to a dedicated page where you can play **Snake**.

### Error 404

We also wanted to customize the error page in case of pages not found.

## Cookies

The creation of **Cookies** is done through JavaScript functions called via buttons in the *button.js* file.

### User Choices

User choices are managed in a label that is displayed if the user has never accessed the site. This check is done through a JavaScript function located in *layout.html*, making it accessible on all pages of the site, by comparing a variable in local storage.

### Privacy Policy

As stipulated by the GDPR (General Data Protection Regulation), every site that handles sensitive data must provide a visible privacy policy on the site. Therefore, a custom text was written for the site, explaining the purposes and techniques for storing user data. Although the site does not explicitly require any sensitive data for storage.

## Snake

### Description

The **Snake** game was developed using HTML, CSS, and JavaScript. The game is designed to be played on both desktop and mobile devices, with automatic detection that adapts the controls accordingly. It includes a feature to save the highest score achieved by the user using the browser's local storage.

### Features and Functionality

#### Multi-device Compatibility and Responsiveness

Through three JavaScript checks, it is detected whether the device is a mobile or desktop device.
The first check detects if the device supports *multi-touch*.
The second check verifies if the device supports touch using a combination of "*ontouchstart*" in the window and the *DocumentTouch* interface.
The third check is based on the device's width. If at least two of the three checks indicate that the device supports touchscreen technology, then listening for movements through finger swipes is enabled.
If the checks detect that the device is a desktop type, the snake's movements will be controlled through keyboard input detection.

#### Snake & Food

The snake is always generated in the center of the playing field, while the food is generated randomly, except in positions where the snake is present.

#### Saving the Personal Score

The score that the user achieves is compared with the highest score saved in the browser's local storage. If the new score exceeds the saved score, it is replaced; otherwise, it remains unchanged.

#### End of the Game

The game can end in two scenarios:

- The first if the snake collides with itself;
- The second if the snake collides with the edges of the playing field;

In these cases, the game ends, and a game over message is displayed along with the score the user achieved.

#### HTML

Used for the user interface, which includes a section to display the current score and the highest score, the main playing area, and a Game Over screen.

#### JavaScript

Used for all controls on the snake, its collisions, the randomly generated food (but not where the snake is), adding the snake's body as the game progresses, managing the snake's movements with both keyboard inputs and touch inputs.

#### CSS

CSS styles were used to create an attractive layout, CSS grids were employed to organize the playing area, and media queries ensure that the game is well-displayed on devices of different sizes.

---
# Backend

## Flask Views

### App.py

To better organize the code, Flask routing is divided using Blueprints.
Thus, in app.py, only the Blueprint calls and the pages for maintenance and error 404 are present.

### Home

Home contains the routing for:
- The home page
- The snake page
- The main ajax requests (e.g., city requests for registration)

### Auth

Contains the pages for login and signup.

### Profile

Contains the pages for the profile, including the admin profile.

### Reports

Contains the pages for reports plus the functions used only on those pages.

### Info

Contains the information page.

## Utils

In utils, the modules used in multiple files are contained, so they can be imported into other parts of the project.

### cfd_analyzer

Cfd analyzer is used to read the bulletins. To do this, you just need to instantiate a Pdf_reader object, in which checks will be performed to see if the bulletin concerns a snowfall or a hydraulic risk.

Depending on the type of risk, another object, Snow or Hydro, will be instantiated. Both classes have functions that allow:

- Reading the PDF using the Camelot library
- Inserting the obtained data into a dictionary that follows the form risk_templates_hydro.json or risk_template_snow.json
- Adding the data to the database

### DB Backup

Functions for database backup, explained in the Database section.

### bulletins_utils

Functions for reading bulletins, both via email and manually uploaded.

It uses the **Pdf_reader** class and saves the bulletins in static/bulletins so they can be downloaded.
This module also includes functions that check for duplicate bulletin names and handle errors related to bulletin reading.

### get_data

Database queries used in multiple views, such as date conversion.

### password

Functions related to password hashing and validation.

### risks

Database queries and conversions related to risks, used both in the report view and in cfd_analyzer.

## Models

Contains the Database Model, used to connect to and execute queries with the Database.

**Each function in utils is thoroughly explained in its docstring.**

## Database

### Project Requirements

Create a database containing the following information:
- Paths of the bulletin files on the server
- History of risks in the Bassano area
- Data related to registered users
- Different roles for admins and regular users

The website should allow:
- Registration, through username, password, and the area of residence
- Registered users to download the latest bulletin
- Users to receive notifications if their area is at risk
- Filtering by area to see the risk history for that area (Example: Vene-B 12/06 hydraulic risk yellow, 14/06 geological risk yellow, etc.)
- Filtering by days (what risks were present on 14/06?) and a table regarding the latest bulletin for that day
- Filtering by type of risk
- Managing bulletins for snow and frost

Admin side:
- Can interface with the site to receive a message via a Telegram bot, which will then be sent to the municipality's Telegram channel. The admin will enter a Telegram contact who will receive the message from the server, which can be modified by the admin (or accepted/rejected)
- Delete or create new admin accounts (taking into account our super admin account)
- Upload any new bulletins that do not arrive automatically from the server

### Requests from Colleagues

- List of cities along with their respective areas to provide users with a reference scheme for their risk area
- List of IDs assigned by Telegram bots related only to admins
- Knowing what data we collect from users to include in the cookie policy
- Separating bulletins regarding hydraulic and geological risks from those for snow and avalanches

### Considerations

From the following requests, the following entities (relationships) can be derived:
1. **Area** (zone)
2. **Risk** (risk)
3. **Role** (role)
4. **Color** (color)
5. **Altitude** (altitude)
6. **Report** (bulletin)
7. **Criticalness** (predicted criticality)
8. **Snow_report** (snow risk bulletin)
9. **Snow_criticalness** (predicted snow criticality)
10. **Topology** (topology)
11. **User** (user)
12. **Admin** (admin user)

Table names will be in singular form for easier readability.

In the **Area** relationship, data related to the zones will be inserted:
- ***ID_area***: zone identification code
- *area_name*: name of the zone divided by bulletins

In the **Risk** relationship, data related to possible risks will be inserted:
- ***ID_risk***: unique identifier associated with each risk
- *risk_name*: name of the risk

In the **Role** relationship, data related to roles will be collected:
- ***ID_role***: unique code assigned to each role
- *role_name*: name of the role (admin, super-admin)

In the **Color** relationship, various possible colors to present in the criticalities will be collected:
- ***ID_color***: color code
- *color_name*: name of the color

In the **Altitude** relationship, various possible altitudes present in snow criticalities will be collected:
- ***ID_altitude***: altitude code
- *height*: height value

In the **Report** relationship, data related to each bulletin will be collected:
- ***ID_report***: unique code for each bulletin
- *starting_date*: start date of the risk presence
- *ending_date*: end date of the risk presence
- *path*: bulletin path on the server

In the **Criticalness** table, data related to predicted criticalities in a specific bulletin will be collected:
- ***ID_issue***: unique code for the criticality
- *ID_area*: code of the bulletin area (taken from **Area**)
- *ID_risk*: code of the type of risk (taken from **Risk**)
- *ID_color*: color code (taken from **Color**)
- *ID_report*: bulletin code (taken from **Report**)

In the **Snow_report** table, data related to each bulletin for mountain areas at risk will be collected:
- ***ID_snow_report***: unique code for each bulletin
- *date*: start date of the risk presence
- *path*: bulletin path on the server

In the **Snow_criticalness** table, data related to the predicted criticalities in a specific bulletin will be collected:
- ***ID_snow_issue***: unique code for snow-related criticality
- *date*: start date of the snow risk presence
- *percentage*: value of the snow level percentage
- *ID_area*: code of the bulletin area (taken from **Area**)
- *ID_snow_report*: code of the type of risk (taken from **Snow_report**)

In the **Topology** table, data related to cities and their corresponding areas will be inserted:
- ***ID_city***: unique city code
- *city_name*: unique city name
- *ID_area*: code identifying the area (taken from **Area**)

In the **User** table, all data related to users will be collected, including:
- ***ID_user***: unique identifier assigned to each user
- *username*: user-chosen name, which must be unique
- *password*: 64-bit hash of the user's password
- *ID_area*: area where the user lives (taken from **Area**)
- *ID_role*: user role code within the site (taken from **Role**)

In the **Admin** table, data related to admins will be collected, including:
- ***ID_telegram***: unique identifier collected to send messages on Telegram
- *groupID*: unique group identifier on Telegram
- *ID_user*: unique user identifier assigned by the DB (taken from **User**)

Some entities are in the form ID_entity - entity_name to facilitate management, subsequent normalization, and referential integrity.

### Restructuring

Before proceeding with the logical design, the E-R diagram was restructured to be representable within the logical model. In particular, the many-to-many association between ***Snow_criticalness*** and ***Altitude*** was simplified with two one-to-many associations and a new bridge entity ***Snow_criticalness_altitude***.

The conceptual schema does not require other modifications as it was designed with a view that already considers the limits of the logical schema.
In fact, the schema did not contain multiple attributes, composite attributes, redundancies, hierarchies, or specializations.

### Logical Design

In this phase, we will define the logical schema that highlights all the associations present within our database.

1. ***Area*** (**ID_area(PK)**, area_name)
2. ***Risk*** (**ID_risk(PK)**, risk_name)
3. ***Role*** (**ID_role(PK)**, role_name)
4. ***Color*** (**ID_color(PK)**, color_name)
5. ***Altitude*** (**ID_altitude(PK)**, height)
6. ***Report*** (**ID_report(PK)**, starting_date, ending_date, path)
7. ***Criticalness*** (**ID_issue(PK)**, ID_area(FK1), ID_risk(FK2), ID_color(FK3), ID_report(FK4))
    1. ID_area FK1 references ***Area***.ID_area
    2. ID_risk FK2 references ***Risk***.ID_risk
    3. ID_color FK3 references ***Color***.ID_color
    4. ID_report FK4 references ***Report***.ID_report
8. ***Snow_report*** (**ID_snow_report(PK)**, date, path)
9. ***Snow_criticalness*** (**ID_snow_issue(PK)**, date, percentage, ID_area(FK1), ID_snow_report(FK2))
    1. ID_area FK1 references ***Area***.ID_area
    2. ID_report FK2 references ***Snow_report***.ID_snow_report
10. ***Topology*** (**ID_city(PK)**, city_name, ID_area(FK1))
    1. ID_area FK1 references ***Area***.ID_area
11. ***User*** (**ID_user(PK)**, username, password, ID_area(FK1), ID_role(FK2))
    1. ID_area FK1 references ***Area***.ID_area
    2. ID_role FK2 references ***Role***.ID_role
12. ***Admin*** (**ID_telegram(PK)**, groupID, ID_user(FK1))
    1. ID_user FK1 references ***User***.ID_user
13. ***Snow_criticalness_altitude*** (**ID_snow_issue (PK, FK1)**, **ID_altitude (PK, FK2)**)
    1. ID_snow_issue FK1 references ***Snow_issue***.ID_report
    2. ID_altitude FK2 references ***Altitude***.ID_altitude

### Normalization

During the conceptual construction process of the Database, the possibility of avoiding the creation of functional dependencies or transitive functional dependencies was taken into account.
The relationships already comply with the first normal form because there is a primary key for each table, and there are no composite attributes.
The relationships also comply with the second normal form because there are no functional dependencies as possible dependencies were separated a priori during conceptual modeling into separate tables.
The relationships also comply with the third normal form because there are no transitive functional dependencies; all attributes fully depend on the primary key.

## Application Creation to Download Emails and Extract PDF Attachments

Using the ***Imaplib*** library, a *Python* application was created that, through specific authentication via the creation of a *Google APP password*, accesses the "*swallowspottesting@gmail.com*" mailbox designated for receiving emails containing bulletin attachments and downloads the content so it can be processed for data reading in the PDFs. Additionally, a list of allowed email addresses was added, which are compared with the senders of the emails to validate their origin, discarding and deleting any email that has already been read or is invalid.

## Backup System

### Design

The **Backup** system was created to ensure the reliability of the Database, whose information is subject to various threats such as accidental deletion or storage device failure. To address this problem, we designed a program that uses client-server technology to send and receive the file with the Database copy, an SQL file containing table structures and the data within them.
To ensure the security and integrity of data transfer, the ***OpenSSL*** library was used to generate **encrypted certificates** and an additional check on the file size upon receipt.

### Implementation

The two programs, *client_backup.py* and *server_backup.py*, establish a connection via **Socket TCP SSL** within which the *.SQL* file containing the database backup is sent.
The backup is obtained through a shell command in Linux executed directly by the client program on the Swallow Spot server, generating a file with the latest DB changes.
In the *server_backup.py* program, run on the remote machine where the backup will be performed, it is necessary to import the file with the required certificates for the connection.
Once the program is executed, the backup can be performed from the site's admin panel by entering the correct IP address and logical port of the socket to connect to.

---
# Telegram Bot

## Introduction

The **Telegram Bot** serves to automatically send the latest snowfall and hydrogeological bulletin via Telegram messages to admins, with the option to forward or delete the received alert message. Additionally, the **Telegram Bot** offers the possibility to manually check the latest bulletin uploaded to the database via private chat.

## Main Features

### Automatic Message Sending

The Bot is configured to automatically send messages to a specific Telegram group. Using the group's *chat ID* and a scheduling system, the bot can deliver messages precisely and promptly.

### Message Management

The Bot is programmed to handle various commands, including buttons from the Telegram user:
1. A button that appears with the `/start` command serves to provide the user with their *chat_id*, granting them the privileges to use the Bot.
2. In the private chat, after linking the Bot with their Telegram account from the website, the user can manually check the types of bulletins in the database.
3. Another command must be sent in the Telegram group that the user creates, adding the Bot as well, to discover the group's *chat_id* to receive automatic alert messages from the Telegram Bot.
4. If the user has not linked their Telegram account with their website account, they will not be able to use any of the Bot's services.

### Message Forwarding

When there is an alert color in the bulletin for the relevant area of the Telegram bot, the bot will send a message to all linked admins in the Telegram group, describing the alert color and type. Below this message, there will be two buttons allowing the admin to either forward the message to the set group or delete the message.

### Technical Implementation

The Telegram Bot was developed using Telegram's APIs with the Python programming language. It was configured to interact with the Telegram server, using the *chat ID* to identify users and groups. The automatic sending and message management functionalities were implemented through automation scripts that process user commands and send appropriate responses.

### Conclusion

In conclusion, the created Telegram Bot is an effective resource for promptly keeping users informed about snowfall and hydrogeological risks. Thanks to its ability to automatically send messages to designated Telegram groups and manage user commands, it offers an efficient system for disseminating critical information. The technical implementation using Telegram's APIs and Python ensures reliable and stable operation. Additionally, the ability for administrators to forward or delete received alerts adds a level of customization and control to message management. Overall, the Bot presents itself as an indispensable tool for improving communication and content sharing within online communities.

---

# Potential Improvements

- Adding two-factor authentication for password recovery via email.
- Better interface for changing credentials within the profile and adding actions and/or customizations.
- Adding avalanche or other types of bulletins.
- Implementing a global leaderboard for Snake players and managing it when the user is offline.

---

# Licensing

## Code

The code in this project is licensed under the GNU General Public License v3.0. See the [LICENSE](./LICENSE) file for details.

## Assets

The assets in this project (including images, graphics, audio, etc.) are licensed under the Attribution-NonCommercial-NoDerivatives 4.0 license. See the [LICENSE-ASSETS](./LICENSE-ASSETS) file for details.

# Credits

*This project involved: Degetto Tommaso, La Rosa Leonardo, Maggiotto Giacomo, Martini Davide, Stefani Marco, Tosin Filippo.*