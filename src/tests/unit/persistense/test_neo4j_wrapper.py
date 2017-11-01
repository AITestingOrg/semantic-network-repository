from ....common.persitence.neo4j_wrapper import Neo4jWrapper

def setup():
    connection = 'bolt://localhost:7474'
    auth = {}
    return Neo4jWrapper({}, connection, auth)

def test_answer():
    assert inc(4) == 5