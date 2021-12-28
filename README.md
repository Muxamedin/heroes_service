
# Get list of heroes:

curl -X GET  http://localhost:8080/heroes


# Create some group:
curl -d '{"fake_group":["doctor_octopus", "captain_america"]}' -H
"Content-Type:
application/json" -X POST  http://localhost:8080/squads


# Create hero:
### where positions in a list [true, 200, 1] mean:
index 0 - true|false -  good|bad
index 1 - integer    -  power
index 1 - 1|0.5|0    -  alive|injured|dead

curl -d '{"cosmo_cat_dog":[true, 200, 1]}' -H "Content-Type:
application/json" -X
POST
http://localhost:8080/heroes

# Update hero:
## all can be updated for hero,  except power
curl -d '{"alive": "injured", "good": false}' -H "Content-Type: application/json" -X PATCH  http://localhost:8080/heroes/rocket

# Get info about hero and about group:

## hero
curl -X GET  http://localhost:8080/heroes/cosmo_cat_dog
### description values from hero
index 0 - true|false -  good|bad
index 1 - integer    -  power
index 1 - 1|0.5|0    -  alive|injured|dead


## group
curl  -X GET  http://localhost:8080/squads/spider_man_team


# Delete hero
## will be deleted from groups as well
curl  -X DELETE  http://localhost:8080/heroes/nova

# Delete squad
curl  -X DELETE  http://localhost:8080/squads/fantastic_four


curl -d '{"name":[false, 203, 1]}' -H "Content-Type: application/json" -X POST  http://localhost:8080/heroes