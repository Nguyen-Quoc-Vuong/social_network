<h1 align="center">
  フェイスブック　
</h1>
<div align="center">
  
![](https://img.shields.io/github/last-commit/TaiZuon/social_network/main)

</div>
<td align="center">
      Feisubukku is a social networking web app project directly inspired by the globally famous social network Facebook.
</td>

## Demo
- Link to the demo video is [here]([https://youtu.be/xHnNuKbU6_s](https://youtu.be/hDZeMxDTlC4)).

## Technology used
-	Backend: Django
-	Frontend: HTML, CSS, Javascript
-	Database Management System: PostgreSQL, MongoDB, Redis
-	Deployment: Docker

## Main functions
-	Login – Logout
-	Register
-	Profile
-	Friends
-	Posts
-	Comments
-	Reacts
-	Chat
-	Notification

## New Feature
### Chat
- Only friends are able to see eachother for chatting
- Contact users sorted by last message

## Special point
### Replication (PostgreSQL)
- 2 postgresql databases, 'default' and 'replica'
- 'replica' is a backup and be updated by WAL file from 'default'
- prepare for database-shutdown scenarios

### Friendly UI/UX
- close to Facebook
- easy to use

## Implement
- Currently the project can only work on local due to the complicate system of databases
- Python is installed
### Get source code
- use `git clone https://github.com/TaiZuon/social_network.git`
### Set up database
- install PostgreSQL, MongoDB, Redis
- Config these database following the [social_network\settings.py](https://github.com/Nguyen-Quoc-Vuong/social_network/blob/main/social_network/settings.py) file
### Run
- Open folder contains the project (loccation of manage.py file), use the command `python manage.py runserver`
- [Local](http://127.0.0.1:8000/) ready to go! 
## Hope to get contribution from you ❤️




