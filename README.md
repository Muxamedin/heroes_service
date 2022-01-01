# Marvel heroes in squads
Something similar to the REST API service

To run service - you can execute `main.py`

`python3 main.py`


- Allows store information about heroes and about groups.
- Allows compare power of squads of heroes.
- Allows create, delete , modify - hero.
- Allows create, delete , modify - squad.


See, which commands you may use to play with service:
- Note: Tested with curl on Linux and MacOs (on Windows commands POS may not
  work as described)
(make sure you know how to adopt commands to run curl from cmd )

## Get list of heroes:

`curl -X GET  http://localhost:8080/heroes`


## Create some group:
`curl -d '{"fake_group":["doctor_octopus", "captain_america"]}' -H
"Content-Type:
application/json" -X POST  http://localhost:8080/squads`


## Create hero:
###  positions in a list [true, 200, 1] means:
- index 0 - true/false -  good/bad
- index 1 - integer    -  power
- index 1 - 1/0.5/0    -  alive/injured/dead

`curl -d '{"cosmo_cat_dog":[true, 200, 1]}' -H "Content-Type:
application/json" -X POST http://localhost:8080/heroes`

## Update hero:
### all can be updated for hero,  except power
`curl -d '{"alive": "injured", "good": false}' -H "Content-Type: application/json" -X PATCH  http://localhost:8080/heroes/rocket`

## Get info about hero and about group:

## Hero
### Get hero info
`curl -X GET  http://localhost:8080/heroes/cosmo_cat_dog`
### description values from hero
- index 0 - true/false -  good/bad
- index 1 - integer    -  power
- index 1 - 1/0.5/0    -  alive/injured/dead
### Create hero
`curl -d '{"name":[false, 203, 1]}' -H "Content-Type: application/json" -X POST  http://localhost:8080/heroes`


### Delete hero
### will be deleted from groups as well
`curl  -X DELETE  http://localhost:8080/heroes/nova`

## Squads
### Get info about squad
`curl  -X GET  http://localhost:8080/squads/spider_man_team`

### Create squad
`curl -d '{"new_team":["venom", "carnage" ,"toxin" ]}' -H "Content-Type:
application/json" -X POST  http://localhost:8080/squads`

### Delete squad
`curl  -X DELETE  http://localhost:8080/squads/new_team`

### Create Squad


## Tournament
### I'm using post here to get tournament
#### use such format for json body
{"squad1": "<name_of_team>",
 "squad2": "<name_of_team>"
}

 `curl -d '{"squad1":"spider_man_team", "squad2":"tmnt"}' -H "Content-Type:
 application/json" -X POST  http://localhost:8080/tournament:q`