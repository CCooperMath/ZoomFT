# Zoomfront

## Project Description 
ZoomFront is a fake 'steam'-style storefront that allows
users to create accounts, add friends, add funds, and view/purchase games.
It supports a basic library and tagging system. 

It is made with Flask and uses a MariaDB database to store information.

The visuals of the site are not a high priority, as the project serves as 
a method of learning more about database management with SQL rather than 
web-dev practice. ZoomFront implements simple queries (such as SELECT * FROM) 
but also adds some more complicated joins (e.g. finding all games which share a tag with a current game). 

## Instructions 

You need to manually modify the config in "website/__init__.py" to match your local database info to properly log in.
/SQL/create.sql contains the necessary code to generate the database. If you would like to prepopulate
the database with fake games, users, friendships, and tag assignments, please run "website/generateFakeInfo.py"

If you would like to log in with an 'administrative' account that is precreated, with 

username: "Fragorl" 
password: "1234". 

Start the web server by running main.py, connect on wherever it hosts, and have fun clicking around.


## Flaws
ZoomFront is flawed in many ways! In particular, it stores passwords in plain text because I did not want to get bogged down in that side of things. There are occasions where I believe queries are made multiple times where not needed, and those show room for optimization later on when I've fully fleshed the project out. ZoomFront also has an odd file layout, and includes code in some places it honestly shouldnt. It is, of course, a work in progress :) 

At a certain point in coding up the manager classes, I realized that it was much more appropriate to work with IDs than things like a fixed username at time of clicking a link. Philosophically, every part of the manager classes
should really work with IDs more often, and if I go back and make refactors of that class I would 100% change that aspect of the code.

The code for the webpages includes a lot of useless logic. If I had managed my project a little more from the outset and decided where inputs are santizied, how errors are thrown in a standard way, and how to do the logical flow from the beginning I would've saved myself a lot of headache later. 

## Known Bugs

When fetching the list of games with a shared tag, duplicates appear because two games may share different tags! 


