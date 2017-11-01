from neo4j.v1 import GraphDatabase, basic_auth
from .neo4j_wrapper import Neo4jWrapper

class WrapperFactory:
    @staticmethod
    def buildNeo4jWrapper(host, port, username, password):
        connect = f'bolt://{host}:{port}'
        auth = basic_auth(username, password)
        return Neo4jWrapper(GraphDatabase.driver, connect, auth)
