from .neo4j_api import Neo4jApi


class Neo4jInitWrapper(Neo4jApi):
    def __init__(self, driver, connection, auth):
        super.__init__(driver, connection, auth)
        self.commands = ['CREATE CONSTRAINT ON (node:Node) ASSERT node.name IS UNIQUE']

    def initialize_db(self):
        self._connect()
        [self.run(command) for command in self.commands]
        self._close()
