# Common server instructions

## Basic info
The server will be up until 22:30 every day.
For any problem add an issue to the project with (common-server) label.

## Accounts

Each team member has a personal account.
The credentials will be sent to you privately.

## Public IP

The public IP may change, if necessary I will write to you about the change.

## Access via ssh

To log in via ssh use the command

`ssh [yourusername]@[public-ip] -p 2234`

## Ports for testing

The port range for testing is 5000 - 5005.

So we can divide it in this way

- Degetto: 5000
- La Rosa: 5001
- Maggiotto: 5002
- Martini: 5003
- Stefani: 5004
- Tosin: 5005

## Database access
To access to adminer search in the url bar
`http://[public-ip]:5006/adminer.php`

You have to login with **only** your surname and the same password used for ssh.

For now only database and backend administrators can alter table but in the future it can be changed

**this file will be updated in the future!**