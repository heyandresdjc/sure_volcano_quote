# Volcanoa Insurance


## Initialize the project
- Run the `./setup.sh` with a desire mode with the options of `MODE=docker` or `MODE=pipenv` (Docker highly suggested)
    - Follow terminal prompts and the project will be available in (Port 8000)[http://localhost:8000]


## How to user the API
To find all the available endpoints pplease navigate to the [Swagger](http://localhost:8000/swagger/), it will list out all the avaible enpoints

### Summary of the endpoints:
#### `http://0.0.0.0:8000/api/users/`
- This is your user registration authentication using token authentication Example CURL call:
```shell
curl -X POST -H "Content-Type: application/json" \
-d '{"username": "linuxize", "email": "linuxize@example.com", "password": "SureApp123!"}' \
http://0.0.0.0:8000/api/users/

# Response
{"token":"8054d51b8e38bc953c1ebdf415484d4e878b060f"}
```
#### `http://0.0.0.0:8000/api/quotes/`
- Create a quote for the desire holder
```shell
curl -X POST -H "Content-Type: application/json" \
-H "Authorization: Token {{api-token}}" \
-d '{"policy_holder": "Frank Underwood", "had_previously_cancel_volcano_policy": true, "never_cancel_volcano_policy": true, "new_property": true, "address": "1600 Pennsylvania Avenue NW, Washington, DC 20500"}' \
http://0.0.0.0:8000/api/quotes/

Example Response
{"quote_number":"SH9H16N6A0"}
```

- `http://0.0.0.0:8000/api/checkout/`
Finalize the Quote
```shell
curl -X POST -H "Content-Type: application/json" -H "Authorization: Token {{api-token}}" -d '{"quote_number":"SH9H16N6A0"}' http://0.0.0.0:8000/api/checkout/

Example Response
{"quote_number":"SH9H16N6A0"}
```

