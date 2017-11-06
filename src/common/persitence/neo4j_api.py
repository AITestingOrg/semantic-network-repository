class Neo4jApi:
    def __init__(self, driver, connection, auth):
        self.graphDb = driver
        self.auth = auth
        self.connection = connection

    def _connect(self):
        self.driver = self.graphDb(self.connection, self.auth)
        self.session = self.driver.session()

    def _close(self):
        if hasattr(self, 'session') and self.session != None:
            self.session.close()

    def _run(self, query, obj = None):
        self._connect()
        if obj == None:
            results = self.session.run(query)
        else:
            results = self.session.run(query, obj)
        self._close()
        return results