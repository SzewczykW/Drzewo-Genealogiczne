import graphene
from .graphql_types import PersonType
from .neo4j_connection import get_session
import uuid


class CreatePerson(graphene.Mutation):
    class Arguments:
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)
        birth_date = graphene.String()
        death_date = graphene.String()
        gender = graphene.String(required=True)

    person = graphene.Field(PersonType)

    def mutate(
        root, info, first_name, last_name, gender, birth_date=None, death_date=None
    ):
        person_id = str(uuid.uuid4())
        session = get_session()
        with session:
            result = session.run(
                """
                CREATE (p:Person {
                    id: $id,
                    first_name: $first_name,
                    last_name: $last_name,
                    gender: $gender,
                    birth_date: $birth_date,
                    death_date: $death_date
                }) RETURN p
                """,
                id=person_id,
                first_name=first_name,
                last_name=last_name,
                gender=gender,
                birth_date=birth_date,
                death_date=death_date,
            )
            record = result.single()
            person = PersonType.from_node(record["p"])
        return CreatePerson(person=person)


class CreateParentRelationship(graphene.Mutation):
    class Arguments:
        parent_id = graphene.ID(required=True)
        child_id = graphene.ID(required=True)

    ok = graphene.Boolean()

    def mutate(root, info, parent_id, child_id):
        session = get_session()
        with session:
            session.run(
                """
                MATCH (parent:Person {id: $parent_id}), (child:Person {id: $child_id})
                CREATE (parent)-[:PARENT]->(child)
                """,
                parent_id=parent_id,
                child_id=child_id,
            )
        return CreateParentRelationship(ok=True)


class CreateMarriedRelationship(graphene.Mutation):
    class Arguments:
        person1_id = graphene.ID(required=True)
        person2_id = graphene.ID(required=True)
        since = graphene.String(required=True)
        status = graphene.String(required=True)

    ok = graphene.Boolean()

    def mutate(root, info, person1_id, person2_id, since, status):
        session = get_session()
        with session:
            session.run(
                """
                MATCH (p1:Person {id: $person1_id}), (p2:Person {id: $person2_id})
                CREATE (p1)-[:MARRIED {since: $since, status: $status}]->(p2)
                CREATE (p2)-[:MARRIED {since: $since, status: $status}]->(p1)
                """,
                person1_id=person1_id,
                person2_id=person2_id,
                since=since,
                status=status,
            )
        return CreateMarriedRelationship(ok=True)


class Mutation(graphene.ObjectType):
    create_person = CreatePerson.Field()
    create_parent_relationship = CreateParentRelationship.Field()
    create_married_relationship = CreateMarriedRelationship.Field()
