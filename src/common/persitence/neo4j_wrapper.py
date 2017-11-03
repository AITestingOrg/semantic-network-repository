class Neo4jWrapper:
    def __init__(self, driver, connection, auth):
        self.graphDb = driver
        self.auth = auth
        self.connection = connection

    def __connect__(self):
        self.driver = self.graphDb(self.connection, self.auth)
        self.session = self.driver.session()

    def __close__(self):
        if self.session:
            self.session.close()

    def __run__(self, query):
        self.__connect__()
        results = self.session.run(query)
        self.__close__()
        return results

    def insertNode(self, node):
        self.__connect__()
        self.session.run("CREATE (a:Person {name: {name}, title: {title}})",
                    {"name": "Arthur", "title": "King"})
        self.__close__()

    def getNodes(self):
        return self.__run__('MATCH(n) RETURN(n);')

    def getNode(self, name):
        pass

    def updateNode(self, node):
        pass

    def execQuery(self, query):
        return self.__run__(query)