

# Servicio de jugador

## Descripción

Este microservicio forma parte de la aplicación, proyecto para la asignatura "Fundamentos de Ingeniería Software para Cloud" del "Máster en Ingeniería del Software: Cloud, Datos y Gestión TI" en la  Universidad de Sevilla.

la funcionalidad de este microservicio es ofrecerle las informaciones a Team-Service las informaciones necesarias para la creación de los equipo, puedo ellos consumir de nuestra API, así como también ofreciéndole el servicio del envío de correos, notificando a los jugadores cuando se aproxime la fecha del partido al que están inscrito.


## Tecnologías

Para el desarrollo de este microservicio se utilizaron las siguientes tecnologías:
-	**Django**  (backend)
-   **Flask**  (FrameWork-backend)
-   **MongoDB**  (Base de Datos)
-   **Swagger**  (Documentación de la API)
-   **Docker**  (Gestor de contenedores)
-   **Okteto**  (Despliegue en la nube)

## API Endpoints

(Swagger API docs)[https://player-service-danaremar.cloud.okteto.net/apidocs/]

## API externas

Hemos utilizado la API Rest  **Send Grid**  para el envió de correos electrónicos notificando cuando los diferentes jugadores tienen partido agendado, adicional de  la informaciones metrológicas para ese día/hora.

## Microservicio básico:

- El backenddebe ser un API REST tal como se ha visto en clase implementando al menos los métodos GET, POST, PUT y DELETE y devolviendo un conjunto de códigos de estado adecuado ([**player_service/app.py**](./player_service/app.py)).
- La API debe tener un mecanismo de autenticación (función _**verify_token**_ en el fichero [**player_service/utils.py**](./player_service/utils.py)).
- Debe tener un frontend que permita hacer todas las operaciones de la API (este frontend puede ser individual o estar integrado con el resto de frontends) ([**Frontend PlayerComponent**](https://github.com/Football-FIS/footmatch-frontend/tree/develop/src/app/players)).
- Debe estar desplegado y accesible en la nube (https://player-service-danaremar.cloud.okteto.net/apidocs/).
- La API que gestione el recurso también debe ser accesible en una dirección bienversionada (https://player-service-danaremar.cloud.okteto.net/apidocs/).
- Se debe tener una documentación de todas las operaciones de la APIincluyendo las posibles peticiones y las respuestas recibidas (https://player-service-danaremar.cloud.okteto.net/apidocs/).
- Debe tener persistencia utilizando MongoDBu otra base de datos no SQL ([**player_service/app.py**](./player_service/app.py)).
- Deben validarse los datos antes de almacenarlos en la base de datos (por ejemplo, haciendo uso de mongoose) ([**player_service/model.py**](./player_service/model.py)).
- Debe haber definida una imagen Docker del proyecto ([**docker-compose.yaml**](./docker-compose.yaml)).

## Microservicio avanzado:

- Consumir alguna API externa (SendGrid) a través del backend  [función **sengrid_send_mail** de **player_service/utils.py**](./player_service/utils.py)).

## Extra

- Frontend común que integra todos los microservicios.
- Empleo de JWT para autentificarse (cabecera authentification: Bearer ...)
- Swagger (https://player-service-danaremar.cloud.okteto.net/apidocs/).

## Run

### Gunicorn

Ejecución local con [_**gunicorn**_](https://gunicorn.org/):

```
unicorn --bind 0.0.0.0:8080 wsgi:app --reload
```

### Docker

```
docker compose --env-file .env -f compose.yaml up --build
```

### Variables de entorno

Esta aplicación recibe parametro mediante variables de entorno. Se puede encontrar una plantilla en [.env.template](.env.template).

### Autores

-   José María Cruz Lorite
-   Johnsiel Antonio Castaños Hernández










