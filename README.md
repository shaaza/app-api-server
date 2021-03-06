## Description
This API server was built as a prototype/MVP of an analytics/application server for an energy analytics app, in a very short period of time. This was tuned and tested for a couple of months with around ~3000 users, in Denmark.

The front-end was in Angular 1 + PHP/Laravel (not in this repo). We used a PostgreSQL database along with this API server.

Some of the code for the analytics was later to ported to C, and keeping this in mind, we've used an extremely imperative style in various place to make the transition easier.

### Directory Structure
------------

* the v1 folder contains the API, with wsgi.py wrapping main.py via Gunicorn. main.py is the core starter file.
* the config folder contains the server setup configurations.
* the docs folder contains the documentation, with details of each route/group separated into separate files/folders.
* API-REFERENCE.md contains the full compiled version of all the docs (less readable than the docs folder)
* update_server.sh is an updating tool (deprecated, use git now)

### Logs
--------------

The error logs on the server are located at:
A. Nginx: /var/log/nginx/error.log
B. Gunicorn + Flask: /var/log/upstart/onboardingapi.log

Access logs (requests to server) are at /var/log/nginx/access.log

## Deploying Code
--------------------

After making changes to any of the files, the files can be updated by running:

		 ./update_server.sh "/path/to/private/key.pem"

This will replace all the files with new edited versions.
To reload the Gunicorn server after updating the files, run:

		 ./update_server.sh "/path/to/private/key.pem" reload

Note that this will upload AND reload the server. Reload the server only during maintenance, as any connected clients will be affected.


## Installation
------------------------

The process is almost identical to the guide at: https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-14-04, except for the use of virtualenv and filename conventions.

There wasn't a need for virtualenv as all installations were made to the specific version of python using the commands pip2.7 and python2.7. Note that this specific-version python has to be called using 'python2.7' and not the global 'python'.

A. Installing Nginx, Gunicorn, Flask

1. sudo apt-get install nginx
2. pip2.7 install flask
3. pip2.7 install gunicorn
4. pip2.7 install flask_cors


B. Setup Application

1. Create project folder at ~/scripts/onboarding
2. Copy api.py, onboarding.py and activities.json to the folder.
3. Create wsgi.py, which imports the Flask app (variable name) from api.py.





C. Configuration

1. Gunicorn
- Create an Upstart script to start at boot time and copy contents of gunicorn_config to it, at /etc/init/onboardingapi.conf.
- After adding this file, it can be started without reboot (first time only) using sudo start onboarding.

2. Nginx
- Disable the default server with nginx by deleting /etc/nginx/sites-enabled/default
- Copy contents of file nginx_config to /etc/nginx/sites-available/engazeapi.
- Enable the site by creating symlink: sudo ln -s /etc/nginx/sites-available/engazeapi /etc/nginx/sites-enabled
- sudo service nginx restart

Note: Default server can be re-enabled by creating a symlink of the config file of same name in /etc/nginx/sites-available/, as done above for sites-available/onboarding. Make sure the two don't clash.




## Configuration
-----------------------------------------
Make changes to wsgi.py for any Flask deployment configuration.
Make changes to nginx_config or gunicorn_config as required and copy to their locations mentioned at the top of the file, and restart to see changes.

Possible changes are documented:

A. gunicorn_config

Explanation
- start/stop commands starts gunicorn on boot, and stops it on shutdown.
- respawn ensures that the gunicorn process restarts incase it is killed for some reason.
- setuid and setgid sets user and group (change depending on system's usernames/groups)
- cd to the project directory
- Call gunicorn.

Configurations for calling gunicorn:

--> exec gunicorn --workers 3 --bind unix:api.sock -m 007 wsgi:app

> --workers 3: No. of workers should ideally be (2 * (no. of CPU Cores) + 1). Gunicorn is based on a worker model - there is a central master process that manages a set of worker processes. All requests and responses are handled completely by worker processes, and master knows nothing about individual clients.

> unix:api.sock -m 007: Binds to a sock file in the same directory with permissions 007, which is later referenced by the nginx configuration.

> wsgi:app: wsgi is the file that gunicorn binds to, and the app is the Flask app that is imported inside wsgi.py.


B. nginx_config

Explanation and Configurable settings
--> listen 80 default_server:
sets the port number and makes this the default server, i.e. it handles all incoming requests to the IP. Otherwise, it is possible to specify server_name below and route that to a specific process etc.

--> server_name _ :
as mentioned above, can be used to specify IP/domain of the server and process requests accordingly. _ is merely a mis-match character, nothing special about it.

--> proxy_pass http://unix:/home/ubuntu/api/v1/api.sock:
This forwards all requests to 80 to the gunicorn .sock file setup at the above location by /etc/init/onboardingapi.conf


## Reading
-----------------------------------------
Here a few articles on how this setup works.

How gunicorn and nginx works:
https://www.quora.com/What-are-the-differences-between-nginx-and-gunicorn

RESTful APIs with Flask:
http://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask

RESTful APIs:
http://www.andrewhavens.com/posts/20/beginners-guide-to-creating-a-rest-api/

Extra Setups:
Postgres: http://blog.bigbinary.com/2016/01/23/configure-postgresql-to-allow-remote-connection.html

## Contributors
-----------------------------------------

* Abhit Patil ([@Abhit03](https://github.com/Abhit03)
* Shaaz Ahmed ([@shaaza](https://github.com/shaaza))
