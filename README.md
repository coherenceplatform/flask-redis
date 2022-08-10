# Flask-api Template

This is a template to get started building on Coherence (withcoherence.com)

## To use

- Sign up for an account at app.withcoherence.com
- Import this template into a new repo
- Follow the onboarding steps on the Coherence site to set up your Cloud IDE, automatic preview environments, CI/CD pipelines, and managed cloud infrastructure

## Test running code

Default home:

https://<url_server>

Login to the app (and store user session info)

https://<url_server>/login

Logout from the app

https://<url_server>/logout

## To connect to redis

- Run the toolbox from the Coherence UI
- Run a terminal in the toolbox
- Use cocli to run commands in the running instance. Example:

To run redis-cli:

```console
cocli exec backend 'REDIS_PORT=$(compgen -A variable | grep _REDIS_PORT) && redis-cli -h localhost -p ${!REDIS_PORT}'

Going to run command (backend): [REDIS_PORT=$(compgen -A variable | grep _REDIS_PORT) && redis-cli -h localhost -p ${!REDIS_PORT}]
localhost:6379> 

localhost:6379> set key1 value1
OK
localhost:6379> type key1
string
localhost:6379> get key1
"value1"
localhost:6379> 

```

