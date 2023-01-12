#   Player Service

==============


## Descripción

Microservicio que gestiona la entidad Jugador:
   - Operaciones CRUD.

##  Endpoints


Verbo HTTP | Endpoint | Descripcion
---       | ---       | ---
GET	player|{​​​​​​​idPlayer}​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​|​	Devulve los datos de un jugador

GET	player|{​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​idPlayer}​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​calification	|Devulve una calificación del 0 al 10 basado en rendimiento del jugador (confirmar con el equipo)

POST	player|{​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​idPlayer}| ​Añade un jugador​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​

PUT	player|{​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​idPlayer}| ​Modifica un jugador​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​

DELETE|	player/{​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​idPlayer}|​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​Elimina un jugador

##  Consumo

- Team Service.
- Match Service.
- MatchState Service.

