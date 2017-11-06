from ....common.persitence.neo4j_api import Neo4jApi


# given connect is called
# when a configuration is given
# then the driver should be called with the correct parameters
def test_connect_parameters(mocker):
    # arrange
    stub = mocker.stub(name='driver_stub')
    neo = Neo4jApi(stub, 'con', 'test')

    # act
    neo._connect()

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

        def run(self, query, obj=None):
            pass

    driverMock = DriverMock()

    def mockFactory(param1, param2):
        return driverMock

    mocker.spy(driverMock, 'close')

    neo = Neo4jApi(mockFactory, 'con', 'test')
    neo._connect()

    # act
    neo._close()

    # assert
    assert driverMock.close.call_count == 1


# given close is called
# when a connection is not open
# then nothing should happen.
def test_close_unopen_session(mocker):
    # arrange
    class DriverMock(object):
        def session(self):
            return self

        def close(self):
            pass

        def run(self, query, obj=None):
            pass

    driverMock = DriverMock()

    def mockFactory(param1, param2):
        return driverMock

    mocker.spy(driverMock, 'close')

    neo = Neo4jApi(mockFactory, 'con', 'test')

    # act
    neo._close()

    # assert
    assert driverMock.close.call_count == 0


# given run is called
# when pass an object
# the session should be run with the object.
def test_run_called_with_object(mocker):
    # arrange
    class DriverMock(object):
        def session(self):
            return self

        def close(self):
            pass

        def run(self, query, obj=None):
            pass

    driverMock = DriverMock()

    def mockFactory(param1, param2):
        return driverMock

    mocker.spy(driverMock, 'run')

    neo = Neo4jApi(mockFactory, 'con', 'test')

    # act
    neo._run('test', {'test':'1'})

    # assert
    driverMock.run.assert_called_once_with('test', {'test':'1'})

# given run is called
# when pass an object
# the session should be run with the object.
def test_run_called_without_object(mocker):
    # arrange
    class DriverMock(object):
        def session(self):
            return self

        def close(self):
            pass

        def run(self, query, obj=None):
            print('t')
            pass

    driverMock = DriverMock()

    def mockFactory(param1, param2):
        return driverMock

    mocker.spy(driverMock, 'run')

    neo = Neo4jApi(mockFactory, 'con', 'test')

    # act
    neo._run('test')

    # assert
    driverMock.run.assert_called_once_with('test')
