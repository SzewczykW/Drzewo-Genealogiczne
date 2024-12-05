import graphene
from .graphql_types import PersonType
from .neo4j_connection import get_session
from datetime import datetime


class Query(graphene.ObjectType):
    all_people = graphene.List(PersonType)
    all_trees = graphene.Field(graphene.JSONString)
    people_male = graphene.List(PersonType)
    people_female = graphene.List(PersonType)
    people_alive = graphene.List(PersonType)
    people_dead = graphene.List(PersonType)
    people_alone = graphene.List(PersonType)

    person = graphene.Field(
        PersonType,
        id=graphene.ID(),
        first_name=graphene.String(),
        last_name=graphene.String(),
        birth_date=graphene.String(),
    )

    def resolve_person(
        root, info, id=None, first_name=None, last_name=None, birth_date=None
    ):
        session = get_session()
        with session:
            if id:
                result = session.run("MATCH (p:Person {id: $id}) RETURN p", id=id)
            elif first_name and last_name and birth_date:
                result = session.run(
                    """
                    MATCH (p:Person {first_name: $first_name, last_name: $last_name, birth_date: $birth_date})
                    RETURN p
                    """,
                    first_name=first_name,
                    last_name=last_name,
                    birth_date=birth_date,
                )
            else:
                raise Exception(
                    "You have provide either `id` or `first_name`, `last_name` and `birth_date`."
                )

            record = result.single()
            if record:
                return PersonType(**record["p"])
            return None

    def resolve_all_people(root, info):
        session = get_session()
        persons = []
        with session:
            result = session.run("MATCH (p:Person) RETURN p")
            for record in result:
                persons.append(PersonType(**record["p"]))
        return persons

    def resolve_people_male(root, info):
        session = get_session()
        with session:
            result = session.run("MATCH (p:Person {gender: 'Male'}) RETURN p")
            return [PersonType(**record["p"]) for record in result]

    def resolve_people_female(root, info):
        session = get_session()
        with session:
            result = session.run("MATCH (p:Person {gender: 'Female'}) RETURN p")
            return [PersonType(**record["p"]) for record in result]

    def resolve_people_alive(root, info):
        session = get_session()
        today = datetime.now().strftime("%Y-%m-%d")
        with session:
            result = session.run(
                """
                MATCH (p:Person)
                WHERE p.birth_date < $today AND (p.death_date IS NULL OR p.death_date > $today)
                RETURN p
                """,
                today=today,
            )
            return [PersonType(**record["p"]) for record in result]

    def resolve_people_dead(root, info):
        session = get_session()
        today = datetime.now().strftime("%Y-%m-%d")
        with session:
            result = session.run(
                """
                MATCH (p:Person)
                WHERE p.death_date < $today
                RETURN p
                """,
                today=today,
            )
            return [PersonType(**record["p"]) for record in result]

    def resolve_people_alone(root, info):
        session = get_session()
        with session:
            result = session.run(
                """
                MATCH (p:Person)
                OPTIONAL MATCH (p)-[m:MARRIED]->()
                WITH p, m
                WHERE m IS NULL OR m.status IN ['Divorced', 'Widowed']
                RETURN p
                """
            )
            return [PersonType(**record["p"]) for record in result]

    def resolve_all_trees(root, info):
        session = get_session()
        with session:
            result = session.run(
                """
                MATCH (n:Person)
                WHERE NOT (n)<-[:PARENT]-()  // Find root nodes
                OPTIONAL MATCH path = (n)-[:PARENT*]->(m)  // Match all descendant paths
                WITH COLLECT(path) AS paths
                CALL apoc.paths.toJsonTree(paths) YIELD value
                RETURN value
                """
            )
            tree_data = result.single()["value"] if result else None
            return tree_data
