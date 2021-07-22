import pymongo
client = None
db = None


class Databaseconfig:
    """Used for managing interactions between worker process and mongo database"""

    @staticmethod
    def connect():
        """Connects to database"""

        global client, db
        try:
            uri = "mongodb+srv://siqsessjacob:admin123@cluster0.63xdz.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
            client = pymongo.MongoClient(uri)
            # print("Connecting to MongoDB ...")
            client.admin.command('isMaster')

        except Exception as inst:
            print('Exception occurred while connecting to database', inst)
            if client is None:
                raise Exception('Mongo db not connected')
            db = client['admin']
