from .neo4j_api import Neo4jApi
from ..models.edge import Edge


class Neo4jWrapper(Neo4jApi):
    def __init__(self, driver, connection, auth):
        super(Neo4jWrapper, self).__init__(driver, connection, auth)

    def insert_node(self, node):
        self._run('CREATE (a:Idea {name: {name}, created_at: timestamp()})', {'name': node })

    def get_nodes(self):
        return self._run('MATCH(n) RETURN(n);')

    def get_node(self, name):
        return self._run(f'MATCH (n) WHERE n.name = "{name}" RETURN n')

    def insert_edge(self, source, target, edge):
        # check if the relationship already exits
        matches = self._run('MATCH (x:Idea {name:{source}})-[r:BE]-(z:Idea {name:{target}}) RETURN x, r, z', {'source': source, 'target': target })
        if matches.single() != None:
            return

        # check if the ideas exist
        sourceNode = self.get_node(source).single()
        targetNode = self.get_node(target).single()
        if sourceNode == None:
            self.insert_node(source)
        if targetNode == None:
            self.insert_node(target)

        # create the relationship
        self._run('MATCH (u:Idea {name: {source}}), (r:Idea {name: {target}}) \
            CREATE (u)-[:' + edge.upper() + ']->(r)', {'source': source, 'target': target })

    def update_node(self, old_name, node):
        node.old_name = old_name
        self._run('MATCH (p:Person{old_name: name}) WITH p, p {.*} as snapshot SET p.name = name RETURN snapshot', node)

    def exec_query(self, query):
        return self._run(query)
