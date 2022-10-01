import uvicorn
import strawberry

from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter


@strawberry.type
class Query:
    @strawberry.field
    def hello(self) -> str:
        return "Hello World"


schema = strawberry.Schema(query=Query)
graphql_app = GraphQLRouter(schema)

app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")

if (
    __name__ == "__main__"
):  # this is to be able to run the api on local machine, no docker containers
    uvicorn.run(app, host="0.0.0.0", port=8000)
