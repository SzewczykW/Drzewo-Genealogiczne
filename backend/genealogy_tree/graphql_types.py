import graphene
from .neo4j_connection import get_session


class PersonType(graphene.ObjectType):
    id = graphene.ID()
    first_name = graphene.String()
    last_name = graphene.String()
    birth_date = graphene.String()
    death_date = graphene.String()
    gender = graphene.String()
    mother = graphene.Field(lambda: PersonType)
    father = graphene.Field(lambda: PersonType)
    siblings = graphene.List(lambda: PersonType)
    current_spouse = graphene.Field(lambda: PersonType)
    all_marriages = graphene.List(lambda: graphene.JSONString)
    children = graphene.List(lambda: PersonType)

    def resolve_mother(parent, info):
        session = get_session()
        with session:
            result = session.run(
                """
                MATCH (parent:Person {gender: 'Female'})-[:PARENT]->(child:Person {id: $id})
                RETURN parent
                """,
                id=parent.id,
            )
            record = result.single()
            if record:
                return PersonType(**record["parent"])
            return None

    def resolve_father(parent, info):
        session = get_session()
        with session:
            result = session.run(
                """
                MATCH (parent:Person {gender: 'Male'})-[:PARENT]->(child:Person {id: $id})
                RETURN parent
                """,
                id=parent.id,
            )
            record = result.single()
            if record:
                return PersonType(**record["parent"])
            return None

    def resolve_children(parent, info):
        session = get_session()
        with session:
            result = session.run(
                """
                MATCH (parent:Person {id: $id})-[:PARENT]->(child:Person)
                RETURN child
                """,
                id=parent.id,
            )
            return [PersonType(**record["child"]) for record in result]

    def resolve_current_spouse(parent, info):
        session = get_session()
        with session:
            result = session.run(
                """
                MATCH (p:Person {id: $id})-[r:MARRIED]-(spouse:Person)
                WHERE r.status = "Married"
                RETURN spouse
                """,
                id=parent.id,
            )
            record = result.single()
            if record:
                return PersonType(**record["spouse"])
            return None

    def resolve_all_marriages(parent, info):
        session = get_session()
        with session:
            result = session.run(
                """
                MATCH (p:Person {id: $id})-[r:MARRIED]-(spouse:Person)
                Return r as marriage_properties, spouse
                """,
                id=parent.id,
            )
            marriages = [
                {
                    "marriage_properties": dict(record["marriage_properties"]),
                    "spouse": dict(record["spouse"]),
                }
                for record in result
            ]
            return marriages

    def resolve_siblings(parent, info):
        session = get_session()
        with session:
            result = session.run(
                """
                MATCH (p:Person {id: $id})<-[:PARENT]-(commonParent:Person)-[:PARENT]->(sibling:Person)
                WHERE sibling.id <> $id
                RETURN DISTINCT sibling
                """,
                id=parent.id,
            )
            return [PersonType(**record["sibling"]) for record in result]
