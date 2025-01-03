import graphene
import uuid

from .graphql_types import PersonType
from .neo4j_connection import get_session
from datetime import datetime


class CreatePerson(graphene.Mutation):
    class Arguments:
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)
        birth_date = graphene.Date()
        death_date = graphene.Date()
        gender = graphene.String()

    person = graphene.Field(PersonType)

    def mutate(
        root, info, first_name, last_name, gender=None, birth_date=None, death_date=None
    ):
        person_id = str(uuid.uuid4())
        session = get_session()

        if not gender:
            gender = "Unknown"

        if not birth_date:
            birth_date = "Unknown"

        if not death_date:
            death_date = "NULL"

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
            person = PersonType(**record["p"])
        return CreatePerson(person=person)


class EditPerson(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        first_name = graphene.String()
        last_name = graphene.String()
        birth_date = graphene.Date()
        death_date = graphene.Date()
        gender = graphene.String()

    person = graphene.Field(PersonType)

    def mutate(
        root,
        info,
        id,
        first_name=None,
        last_name=None,
        gender=None,
        birth_date=None,
        death_date=None,
    ):
        session = get_session()
        with session:
            set_clauses = []
            parameters = {"id": id}
            if first_name is not None:
                set_clauses.append("p.first_name = $first_name")
                parameters["first_name"] = first_name
            if last_name is not None:
                set_clauses.append("p.last_name = $last_name")
                parameters["last_name"] = last_name
            if gender is not None:
                set_clauses.append("p.gender = $gender")
                parameters["gender"] = gender
            if birth_date is not None:
                set_clauses.append("p.birth_date = $birth_date")
                parameters["birth_date"] = birth_date
            if death_date is not None:
                set_clauses.append("p.death_date = $death_date")
                parameters["death_date"] = death_date

            if not set_clauses:
                raise Exception("No fields to update")

            set_clause = ", ".join(set_clauses)
            query = f"""
                MATCH (p:Person {{id: $id}})
                SET {set_clause}
                RETURN p
            """

            result = session.run(query, parameters)
            record = result.single()
            person = PersonType(**record["p"])
        return EditPerson(person=person)


class DeletePerson(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    ok = graphene.Boolean()

    def mutate(root, info, id):
        session = get_session()
        with session:
            session.run(
                """
                MATCH (p:Person {id: $id})
                DETACH DELETE p
                """,
                id=id,
            )
        return DeletePerson(ok=True)


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


class DeleteParentRelationship(graphene.Mutation):
    class Arguments:
        parent_id = graphene.ID(required=True)
        child_id = graphene.ID(required=True)

    ok = graphene.Boolean()

    def mutate(root, info, parent_id, child_id):
        session = get_session()
        with session:
            session.run(
                """
                MATCH (parent:Person {id: $parent_id})-[r:PARENT]->(child:Person {id: $child_id})
                DELETE r
                """,
                parent_id=parent_id,
                child_id=child_id,
            )
        return DeleteParentRelationship(ok=True)


class CreateMarriedRelationship(graphene.Mutation):
    class Arguments:
        person1_id = graphene.ID(required=True)
        person2_id = graphene.ID(required=True)
        since = graphene.Date()
        status = graphene.String()

    ok = graphene.Boolean()

    def mutate(root, info, person1_id, person2_id, since=None, status=None):
        session = get_session()

        if not since:
            since = "Unknown"

        if not status:
            status = "Unknown"

        with session:
            session.run(
                """
                MATCH (p1:Person {id: $person1_id}), (p2:Person {id: $person2_id})
                CREATE (p1)-[:MARRIED {since: $since, status: $status}]->(p2)
                """,
                person1_id=person1_id,
                person2_id=person2_id,
                since=since,
                status=status,
            )
        return CreateMarriedRelationship(ok=True)


class UpdateMarriedStatus(graphene.Mutation):
    class Arguments:
        person1_id = graphene.ID(required=True)
        person2_id = graphene.ID(required=True)
        status = graphene.String(required=True)

    ok = graphene.Boolean()

    def mutate(root, info, person1_id, person2_id, status):
        statuses = ["Widowed", "Divorced", "Married", "Unknown"]
        if status not in statuses:
            raise Exception(f"Invalid status. Allowed ones are {statuses}.")

        session = get_session()
        with session:
            result = session.run(
                """
                MATCH (p1:Person {id: $person1_id})-[r:MARRIED]->(p2:Person {id: $person2_id})
                SET r.status = $status
                RETURN r
                """,
                person1_id=person1_id,
                person2_id=person2_id,
                status=status,
            )
        return UpdateMarriedStatus(ok=True)


class DeleteMarriedRelationship(graphene.Mutation):
    class Arguments:
        person1_id = graphene.ID(required=True)
        person2_id = graphene.ID(required=True)

    ok = graphene.Boolean()

    def mutate(root, info, person1_id, person2_id):
        session = get_session()
        with session:
            session.run(
                """
                MATCH (p1:Person {id: $person1_id})-[r:MARRIED]->(p2:Person {id: $person2_id})
                DELETE r
                """,
                person1_id=person1_id,
                person2_id=person2_id,
            )
        return DeleteMarriedRelationship(ok=True)


class InitializeDatabase(graphene.Mutation):
    notifications = graphene.List(graphene.String)
    gql_status = graphene.String()
    status_description = graphene.String()
    message = graphene.String()

    def mutate(root, info):
        session = get_session()
        try:
            with session:
                result = session.run("CALL apoc.cypher.runFile('init.cypher')")

                summary = result.consume()
                metadata = summary.metadata
                notifications = summary.notifications

                statuses = metadata.get("statuses")
                gql_status = statuses[0]["gql_status"]
                status_description = statuses[0]["status_description"]

                notification_messages = []
                if notifications:
                    notification_messages = [
                        note["description"] for note in notifications
                    ]

                message = f"Database initialized completed."

                return InitializeDatabase(
                    notifications=notification_messages,
                    gql_status=gql_status,
                    status_description=status_description,
                    message=message,
                )
        except Exception as e:
            return InitializeDatabase(
                notifications=None,
                gql_status=None,
                status_description=None,
                message="Unknown error occured!",
            )


class Mutation(graphene.ObjectType):
    create_person = CreatePerson.Field()
    edit_person = EditPerson.Field()
    delete_person = DeletePerson.Field()
    create_parent_relationship = CreateParentRelationship.Field()
    delete_parent_relationship = DeleteParentRelationship.Field()
    create_married_relationship = CreateMarriedRelationship.Field()
    update_married_status = UpdateMarriedStatus.Field()
    delete_married_relationship = DeleteMarriedRelationship.Field()
    initialize_database = InitializeDatabase.Field()
