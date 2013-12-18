import unittest, schemaGenerator

class schemaGeneratorTest(unittest.TestCase):
    def testGetConnectionReturnsAConnection(self):
        generator = schemaGenerator.SchemaGenerator()
        connection = generator.getDatabaseConnection()
        assert(connection is not None)
