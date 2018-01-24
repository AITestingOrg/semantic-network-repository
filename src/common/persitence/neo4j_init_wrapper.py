from .neo4j_api import Neo4jApi


class Neo4jInitWrapper(Neo4jApi):
    def __init__(self, driver, connection, auth):
        super(Neo4jInitWrapper, self).__init__(driver, connection, auth)
        self.commands = ['CREATE CONSTRAINT ON (idea:Idea) ASSERT idea.name IS UNIQUE']

    def initialize_db(self):
        [self._run(command) for command in self.commands]
