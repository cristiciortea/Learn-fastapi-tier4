import graphene

from src.db.db_conf import db_session
from src.models import blog_models
from src.schemas.blog_schemas import PostSchema

db = db_session.session_factory()


class CreateNewPost(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        content = graphene.String(required=True)

    ok = graphene.Boolean()

    @staticmethod
    def mutate(root, info, title, content):
        post = PostSchema(title=title, content=content)
        db_post = blog_models.Post(title=post.title, content=post.content)
        db.add(db_post)
        db.commit()
        db.refresh(db_post)

        ok = True

        return CreateNewPost(ok=ok)


class PostMutations(graphene.ObjectType):
    create_new_post = CreateNewPost.Field()
