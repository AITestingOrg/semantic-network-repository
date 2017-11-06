from .neo4j_api import Neo4jApi


class Neo4jWrapper(Neo4jApi):
    def __init__(self, driver, connection, auth):
        super.__init__(driver, connection, auth)

    def insert_node(self, node):
        self._run('CREATE (a:Node {name: {name}}, {created_at: {timestamp()}})', node)

    def get_nodes(self):
        return self._run('MATCH(n) RETURN(n);')

    def get_node(self, name):
        return self._run(f'MATCH (n) WHERE n.name = "{name}" RETURN n')

    def update_node(self, old_name, node):
        node.old_name = old_name
        self._run('MATCH (p:Person{old_name: name}) WITH p, p {.*} as snapshot SET p.name = name RETURN snapshot', node)

    def exec_query(self, query):
        return self._run(query)
