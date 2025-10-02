from neo4j import GraphDatabase
from config import settings

driver = GraphDatabase.driver(settings.NEO4J_URI, auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD))

def create_fact(subject: str, predicate: str, obj: str, meta: dict = None):
    with driver.session() as s:
        s.run(
            "MERGE (a:Entity {name:$s}) MERGE (b:Entity {name:$o}) MERGE (a)-[r:REL {pred:$p}]->(b) RETURN r",
            s=subject, o=obj, p=predicate,
        )

def query_related(entity_name: str, limit: int = 10):
    with driver.session() as s:
        r = s.run(
            "MATCH (e:Entity {name:$name})-[r]-(x) RETURN x.name as name, type(r) as rel LIMIT $l",
            name=entity_name, l=limit,
        )
        return [row.data() for row in r]