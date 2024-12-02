import graphene
from .graphql_types import PersonType
from .neo4j_connection import get_session


class Query(graphene.ObjectType):
    person = graphene.Field(PersonType, id=graphene.ID(required=True))
    all_persons = graphene.List(PersonType)
    all_trees = graphene.List(PersonType)

    def resolve_person(root, info, id):
        session = get_session()
        with session:
            result = session.run("MATCH (p:Person {id: $id}) RETURN p", id=id)
            record = result.single()
            if record:
                return PersonType.from_node(record["p"])
        return None

    def resolve_all_persons(root, info):
        session = get_session()
        persons = []
        with session:
            result = session.run("MATCH (p:Person) RETURN p")
            for record in result:
                persons.append(PersonType.from_node(record["p"]))
        return persons

    def resolve_all_trees(root, info):
        session = get_session()
        with session:
            result = session.run(
                """
                MATCH (n:Person)
                WHERE NOT (n)<-[:PARENT]-()
                OPTIONAL MATCH path = (n)-[:PARENT*]->(m)
                WITH COLLECT(path) AS paths
                CALL apoc.paths.toJsonTree(paths) YIELD value
                RETURN value
            """
            )
            print(result)
            return [PersonType.from_tree_node(record["value"]) for record in result]
