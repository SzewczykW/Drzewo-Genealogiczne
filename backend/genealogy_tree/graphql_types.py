import graphene
from .neo4j_connection import get_driver

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
            id=node['id'],
            first_name=node['first_name'],
            last_name=node['last_name'],
            birth_date=node.get('birth_date'),
            death_date=node.get('death_date'),
            gender=node['gender']
        )

    def resolve_parents(parent, info):
        driver = get_driver()
        with driver.session() as session:
            result = session.run(
                "MATCH (p:Person)<-[:PARENT]-(parent:Person) WHERE p.id = $id RETURN parent",
                id=parent.id
            )
            return [PersonType.from_node(record['parent']) for record in result]

    def resolve_children(parent, info):
        driver = get_driver()
        with driver.session() as session:
            result = session.run(
                "MATCH (p:Person)-[:PARENT]->(child:Person) WHERE p.id = $id RETURN child",
                id=parent.id
            )
            return [PersonType.from_node(record['child']) for record in result]

    def resolve_spouses(parent, info):
        driver = get_driver()
        with driver.session() as session:
            result = session.run(
                "MATCH (p:Person)-[:MARRIED]->(spouse:Person) WHERE p.id = $id RETURN spouse",
                id=parent.id
            )
            return [PersonType.from_node(record['spouse']) for record in result]

    def resolve_siblings(parent, info):
        driver = get_driver()
        with driver.session() as session:
            result = session.run(
                "MATCH (p:Person)-[:SIBLING]->(sibling:Person) WHERE p.id = $id RETURN sibling",
                id=parent.id
            )
            return [PersonType.from_node(record['sibling']) for record in result]

