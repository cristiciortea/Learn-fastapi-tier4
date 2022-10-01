import uvicorn

from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

from src.mutations.library_mutations import author_schema

graphql_app = GraphQLRouter(author_schema)

app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")

if (
    __name__ == "__main__"
):  # this is to be able to run the api on local machine, no docker containers
    uvicorn.run(app, host="0.0.0.0", port=8000)
