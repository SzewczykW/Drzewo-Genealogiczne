import graphene
from .graphql_types import PersonType
from .neo4j_connection import get_driver

class Query(graphene.ObjectType):
    person = graphene.Field(PersonType, id=graphene.ID(required=True))
    all_persons = graphene.List(PersonType)

    def resolve_person(root, info, id):
        driver = get_driver()
        with driver.session() as session:
            result = session.run("MATCH (p:Person {id: $id}) RETURN p", id=id)
            record = result.single()
            if record:
                return PersonType.from_node(record['p'])
        return None

    def resolve_all_persons(root, info):
        driver = get_driver()
        persons = []
        with driver.session() as session:
            result = session.run("MATCH (p:Person) RETURN p")
            for record in result:
                persons.append(PersonType.from_node(record['p']))
        return persons

