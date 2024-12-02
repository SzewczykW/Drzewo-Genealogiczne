import graphene
from .neo4j_connection import get_session


class PersonType(graphene.ObjectType):
    id = graphene.ID()
    first_name = graphene.String()
    last_name = graphene.String()
    birth_date = graphene.String()
    death_date = graphene.String()
    gender = graphene.String()
    parents = graphene.List(lambda: PersonType)
    children = graphene.List(lambda: PersonType)
    spouses = graphene.List(lambda: PersonType)
    siblings = graphene.List(lambda: PersonType)

    @staticmethod
    def from_node(node):
        return PersonType(
            id=node["id"],
            first_name=node["first_name"],
            last_name=node["last_name"],
            birth_date=node.get("birth_date"),
            death_date=node.get("death_date"),
            gender=node["gender"],
        )

    @staticmethod
    def from_tree_node(data):
        return PersonType(
            id=data.get("_id"),
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            birth_date=data.get("birth_date"),
            death_date=data.get("death_date"),
            gender=data.get("gender"),
            children=[
                PersonType.from_tree_node(child) for child in data.get("_children", [])
            ],
        )

    def resolve_parents(parent, info):
        session = get_session()
        with session:
            result = session.run(
                "MATCH (p:Person)<-[:PARENT]-(parent:Person) WHERE p.id = $id RETURN parent",
                id=parent.id,
            )
            return [PersonType.from_node(record["parent"]) for record in result]

    def resolve_children(parent, info):
        session = get_session()
        with session:
            result = session.run(
                "MATCH (p:Person)-[:PARENT]->(child:Person) WHERE p.id = $id RETURN child",
                id=parent.id,
            )
            return [PersonType.from_node(record["child"]) for record in result]

    def resolve_spouses(parent, info):
        session = get_session()
        with session:
            result = session.run(
                "MATCH (p:Person)-[:MARRIED]->(spouse:Person) WHERE p.id = $id RETURN spouse",
                id=parent.id,
            )
            return [PersonType.from_node(record["spouse"]) for record in result]

    def resolve_siblings(parent, info):
        session = get_session()
        with session:
            result = session.run(
                "MATCH (p:Person)-[:SIBLING]->(sibling:Person) WHERE p.id = $id RETURN sibling",
                id=parent.id,
            )
            return [PersonType.from_node(record["sibling"]) for record in result]
