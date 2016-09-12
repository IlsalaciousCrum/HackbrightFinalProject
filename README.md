#Kind Table

<img src="static/recipe_search.png">

### Technology Stack

**Application:** Python, Flask, Jinja, SQLAlchemy, PostgreSQL    
**APIs:** Spoonacular  
**Front-End**: HTML/CSS, Bootstrap, JQuery, JavaScript
*See Further_Development.md file for my public to-do list of further improvements to this project*

Kind Table
--------

**Description**

Kind Table takes the work out of choosing recipes for a dinner party or holiday event by managing your friends dietary preferences and presenting recipes that would work for all.

Please see the further_development branch for continuing work on this project and the .md file Further_Development.md for where I am in the process now. This is a learning project, created for the final project while attending Hackbright Academy. Let the learning/experimenting continue!

**How it works**

Users enter dietary restriction information about themselves and their contacts into webforms served by a Flask app, which populate a Postgres database using SQLAlchemy:

<img src="static/user_profile.png">

The user creates a party and invites their contacts:

<img src="static/party_profile_unexploded.png">

An API call is made to Spoonacular with all the guests dietary restrictions collated and then recipes are presented to the user. Recipe limiters such as diet type, intolerances/allergies and ingredients to avoid can be deselected and the search rerun. 

<img src="static/recipe_search.png">

Recipes can be previewed and then saved to the SQL Alchemy database. The dietary restrictions that were used to run the search are also saved.
These recipes can be viewed from the party profile page. 

<img src="static/recipe_preview.png">


### About the Developer    
Ilsa Gordon 
[Linkedin](https://www.linkedin.com/in/ilsa-gordon)    