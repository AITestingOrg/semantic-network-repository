from ....common.persitence.neo4j_wrapper import Neo4jWrapper

# given connect is called
# when a configuration is given
# then the driver should be called with the correct parameters
def test_connect_parameters(mocker):
    # arrange
    stub = mocker.stub(name='driver_stub')
    neo = Neo4jWrapper(stub, 'con', 'test')

    # act
    neo.__connect__()

    # assert
    stub.assert_called_once_with('con', 'test')
    assert stub.call_count == 1

# given close is called
# when a connection is open
# then the session should be closed.
def test_close_session(mocker):
    # arrange
    class DriverMock(object):
        def session(self):
            return self
        def close(self):
            pass

    driverMock = DriverMock()

    def mockFactory(param1, param2):
        return driverMock

    mocker.spy(mockFactory, 'close')

    neo = Neo4jWrapper(driverMock, 'con', 'test')
    neo.__connect__()

    # act
    neo.__close__()

    # assert
    assert driverMock.close.call_count == 1