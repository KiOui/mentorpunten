# Mentorpunten
Welcome to the Mentorpunten repository. This repository includes the application that can be used to set up an
online scavenger hunt. The application can be used to create Tournaments and Teams of Users for these Tournaments. 
Challenges can be created for each Tournament. The Challenges can be solved by the Teams by uploading a photo after
which an administrator needs to approve (or decline) a Submission for a Challenge. If a Submission is approved, the
Challenge is closed for that Team and points are awarded.

## Setup
This project is built using both [Django](https://www.djangoproject.com) (for the backend) and 
[VueJS](https://vuejs.org) (for the frontend). Both need to be set up (and connected) for development to work.

### Setup backend
1. First install at least [Python](https://www.python.org) 3.11 on your system.
2. If `pip3` is not installed on your system, execute `apt install python3-pip` to install it.
3. Also make sure `python3-dev` is installed on your system, execute `apt install python3-dev`.
4. Install Poetry by following the steps on
[their website](https://python-poetry.org/docs/#installing-with-the-official-installer). Make sure `poetry` is added 
to `PATH` before continuing.
5. Clone this repository.
6. Go to the `backend` directory.
7. Run `poetry install` to install the backend dependencies.
8. Run `poetry shell` to start a shell with the dependencies loaded. This command needs to be run every time you open
a new shell and want to run the development server.
9. Go to the `website` directory.
10. Run `./manage.py migrate` to initialize the database and load all migrations.
11. Run `./manage.py createsuperuser` to create an administrator user.
12. Run `./manage.py runserver` to start the development server locally.

Now your backend server is setup and running on `localhost:8000`. The administrator interface can be accessed by going
to `localhost:8000/admin`.

### Setup frontend
1. Install at least version 17 of [NodeJS](https://nodejs.org/en).
2. Clonse this repository (or if you have done that in the previous steps, skip this step).
3. Go to the `frontend` directory.
4. Use `npm install` to install the required packages.
5. Use `npm run dev` to run the development server.

### Connecting the frontend to the backend
Now that both the frontend and the backend server are up and running, we need to supply the frontend with credentials
such that it can connect to the backend service.

1. Log in on the administrator dashboard of the backend by going to `localhost:8000/admin` and logging in with your
administrator account.
2. Under `Django OAuth Toolkit`, add an `Application`.
3. Provide the following settings: 
- Redirect uris: http://localhost:5173/auth/callback
- Client type: Public
- Authorization grant type: Implicit
- Name: VueJS Frontend
- Skip Authorization: True
4. Before saving the application, make sure to copy over the Client ID and Client Secret to some other location.
5. Now save the application.
6. Create a `.env` file in the `frontend` folder of the repository. The `.env` file should have the following content:
```
VITE_API_BASE_URI=http://localhost:8000
VITE_API_AUTHORIZATION_ENDPOINT=/oauth/authorize/
VITE_API_ACCESS_TOKEN_ENDPOINT=/oauth/token/
VITE_API_OAUTH_CLIENT_ID=[Client ID you copied over]
VITE_API_OAUTH_CLIENT_SECRET=[Client Secret you copied over]
VITE_API_OAUTH_REDIRECT_URI=http://localhost:5173/auth/callback
VITE_API_LOGOUT_URL=/users/logout
```
7. Reload the development server (`npm run dev`) and you are good to go!

## Deployment
This project can be deployed by using [Docker](https://www.docker.com). For deployment you can follow the following
steps. These steps assume that you have a working server that runs Ubuntu which faces the Internet and a domain name 
pointing to the IP address of the server.

1. First install Docker by following the steps on [their website](https://docs.docker.com/engine/install/ubuntu/).
2. Make sure to also install the [Rootless version of Docker](https://docs.docker.com/engine/security/rootless/). 
3. Run `loginctl enable-linger ubuntu` to enable the background services for the `ubuntu` user (such that the
container do not stop when you log out of the server).
4. Run `sudo nano /etc/sysctl.conf ` and add the following line: `net.ipv4.ip_unprivileged_port_start=80`. This enables
privileged ports for the `ubuntu` user.
5. Now copy all the contents inside the `deployment` directory of this repository to a different location.
6. In the newly copied over `deployment` directory, create the following directory structure:
```
data
 | - backend
 |      | - log
 |
 | - database
 |      | - data
 |
 | - shared
 |      | - static
 |      | - media
 |
 | - reverse-proxy
 |      | - conf.d
```
7. Also create a `repository` folder in the `deployment` directory. Clone this repository inside the
`repository` folder (so the repository should be in `repository/mentorpunten`).
8. Create an OAuth application on the [Thalia](https://thalia.nu) website. The OAuth application should have the
following settings:
- Redirect uris: https://[Your server hostname]/thalia/callback
- Client type: Confidential
- Authorization grant type: Authorization code
- Name: Mentorpunten
- Skip Authorization: False
9. Make sure to copy over the Client ID and Client Secret before saving the application. When you are done,
save the application.
10. Now copy over `docker-compose.yml.example` to `docker-compose.yml`. Fill the following environment
variables:
- Postgres Password: Create a random password.
- Django Secret key: Create a random secret key.
- Mentorpunten hostname: The domain pointing to the server running the deployment.
- Thalia OAuth Client ID: The Client ID for the Thalia OAuth application from the previous steps.
- Thalia OAuth Client Secret: The Client Secret for the Thalia OAuth application from the previous steps.
- Client ID from mentorpunten Django host: Leave empty for now.
- Client Secret from mentorpunten Django host: Leave empty for now.
11. Run `docker compose build` to build both the containers.
12. Run `docker compose pull` to pull the `nginx` and `postgres` container.
13. Run `docker compose up -d` to start the Docker containers.
14. Run `docker exec -it mentorpunten-backend /bin/bash` to start a shell in the backend container.
15. Go to the `website` directory inside the container by running `cd website`.
16. Run `./manage.py collectstatic` and `./manage.py createsuperuser` to collect static files and
create the first administrator user. Exit the shell by running `exit`.
17. Now head on over to the Django admin on your domain. You should be able to log in to the
admin by using `http://[Your domain]/admin-login` and the login credentials of the previous step.
18. Once again create an OAuth application with the following settings:
- Redirect uris: http://[Your server hostname]/auth/callback
- Client type: Public
- Authorization grant type: Implicit
- Name: VueJS Frontend
- Skip Authorization: True
19. Before saving, copy over the Client ID and Client Secret. Now save the OAuth application.
20. Run `docker compose down` to stop the containers from running.
21. Edit the `docker-compose.yml` file and enter the following variables:
- Client ID from mentorpunten Django host: The Client ID we got previously.
- Client Secret from mentorpunten Django host: The Client Secret we got previously.
22. Run `docker compose up -d` to start the containers again, the website should now be in working condition.
23. It might be nice to also enable SSL and HTTPS. You can do this by adding a `certbot` container to the 
`docker-compose.yml` file and enabling port 443 on the `reverse-proxy` container. Also make sure to edit the
nginx config in `data/reverse-proxy/conf.d`.

## Development
This section will explain some of the development steps that you have to take or were taken during development of the
application.

### Setting environment variables for the frontend
Normally, environment variables are included during build and can not be changed afterwards. This is a problem when
building a docker container which can be applied to different scenarios (e.g. with different API servers). Because of 
this fact, environment variables can be either included during build with a `.env` file in the root directory or with 
docker environment variables. Using docker environment variables will overwrite the environment variables included 
during build.

Environment variables that are available and should be overwritable by docker environment variables later should be 
included in the `docker.blueprint.env` file. Note that this file must use `'` for indicating strings and the format 
is as follows:
```
    '[NAME_OF_VARIABLE_IN_VUE]': '${NAME_OF_ENV_VARIABLE}'
```
Before starting the `nginx` process, the docker environment variables will be set under the `window.__env__` variable 
in the `index.html` file.

#### Using environment variables for the frontend
To use environment variables that can be set during runtime (with docker environment variables), add the variable to 
the `docker.blueprint.env` file as explained above. Then use the `getEnvVar` function in 
`src/common/general.service.ts` for getting the value of an environment variable. This function will first check 
whether it is set in the `window.__env__` variable and will then look if it is an environment variable.