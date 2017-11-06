from neo4j.v1 import GraphDatabase, basic_auth
from .neo4j_wrapper import Neo4jWrapper
from .neo4j_init_wrapper import Neo4jInitWrapper


class WrapperFactory:
    @staticmethod
    def build_neo4j_wrapper(host, port, username, password):
        connect = f'bolt://{host}:{port}'
        auth = basic_auth(username, password)
        return Neo4jWrapper(GraphDatabase.driver, connect, auth)

    @staticmethod
    def build_neo4j_init_wrapper(self, host, port, username, password):
        connect = f'bolt://{host}:{port}'
        auth = basic_auth(username, password)
        return Neo4jInitWrapper(GraphDatabase.driver, connect, auth)
