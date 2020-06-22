# Seeurmoney Api

You can acess the graphql endpoint of the api at : *127.0.0.1:5000/graphql*

## The List available schemas/mutations

1. category
2. create_category
3. infrastructure
4. create_infrastructure
5. location
6. fetch_category
7. fetch infrastructure
8. infrastructure_query_input
9. save.query

The Api is currently in debug mode to switch to production mode, change the value of **FLASK_DEBUG** in ".flaskenv" file to **0**

The environment variables are present in the ".env" file

### Setting-up the Api

Install the dependencies in the requirements.txt file using the command

`pip install -r requirements.txt`

Start the server using the command

`flask run`
