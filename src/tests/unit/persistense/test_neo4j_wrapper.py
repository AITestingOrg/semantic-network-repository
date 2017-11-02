from ....common.persitence.neo4j_wrapper import Neo4jWrapper

# given connect is called
# when a configuration is given
# then the driver should be called with the correct parameters
def test_connect_parameters(mocker):
    # arrange
    stub = mocker.stub(name='driver_stub')
    neo = Neo4jWrapper(stub, 'con', 'test')
    neo.__connect__()

    # assert
    stub.assert_called_once_with('con', 'test')
    assert stub.call_count == 1

# given close is called
# when a connection is open
# then the session should be closed.
def test_close_session(mocker):
    # arrange
    stub = mocker.stub(name='driver_stub')
    neo = Neo4jWrapper(stub, 'con', 'test')
    neo.__connect__()

    # assert
    stub.assert_called_once_with('con', 'test')
    assert stub.call_count == 1