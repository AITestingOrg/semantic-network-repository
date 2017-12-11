class Neo4jApi:
    def __init__(self, driver, connection, auth):
        self.driver = driver(connection, auth=auth)

    def _run(self, query, obj = None):
        print(query)
        with self.driver.session() as session:
            with session.begin_transaction() as tx:
                if obj == None:
                    results = tx.run(query)
                else:
                    results = tx.run(query, parameters = obj)
                tx.sync()
        return results