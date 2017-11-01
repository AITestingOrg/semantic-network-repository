class Neo4jWrapper:
    def __init__(self, driver, connection, auth):
        self.graphDb = driver
        self.auth = auth
        self.connection = connection

    def __connect__(self):
        self.driver = self.graphDb(self.connection, self.auth)
        self.session = self.driver.session()

    def __close__(self):
        self.session.close()

    def insertNode(self, node):
        self.__connect__()
        self.session.run("CREATE (a:Person {name: {name}, title: {title}})",
                    {"name": "Arthur", "title": "King"})
        self.__close__()

    def getNodes(self):
        pass

    def getNode(self, name):
        pass

    def updateNode(self, node):
        pass

    def execQuery(self, query):
        self.__connect__()
        results = self.session.run(query)
        self.__close__()
        return results