import sqlite3

CONN = sqlite3.connect('lib/dogs.db')
CURSOR = CONN.cursor()

class Dog:
    
    all = []
    
    def __init__(self, name, breed):
        self.name = name
        self.breed = breed
        self.id = None


    # Create a create_table() class method that will create the dogs table if it does not already exist. 
    # The table should have columns for an id, a name, and a breed.
    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS dogs (
                id INTEGER PRIMARY KEY,
                name TEXT,
                breed TEXT
            )
        """

        cls.all = CURSOR.execute(sql)


    # This class method should drop the dogs table 
    # if it does exist- pretty much the opposite of create_table().
    @classmethod
    def drop_table(cls):
        sql = """
            DROP TABLE IF EXISTS dogs
        """

        CURSOR.execute(sql)

    
    # Create an instance method save() that saves a Dog object to your database.
    def save(self):
        sql = """
            INSERT INTO dogs (name, breed)
            VALUES (?, ?)
        """

        CURSOR.execute(sql, (self.name, self.breed))
        CONN.commit()

        # Grabbing the id of that newly inserted row and assigning the given Dog instance's id attribute 
        # equal to the id of its associated database table row.
        self.id = CURSOR.execute("SELECT last_insert_rowid() FROM dogs").fetchone()[0]


    # Create a new row in the database.
    # Return a new instance of the Dog class.
    @classmethod
    def create(cls, name, breed):
        dog = Dog(name, breed)
        dog.save()

        return dog
    

    #  takes a database row and creates a Dog instance.
    @classmethod
    def new_from_db(cls, row):
        dog = cls(row[1], row[2])
        dog.id = row[0]

        return dog
    

    # This class method should return a list of Dog instances for every record in the dogs table.
    @classmethod
    def get_all(cls):
        sql = """
            SELECT * FROM dogs
        """    

        dogs = CURSOR.execute(sql).fetchall()

        cls.all = [cls.new_from_db(dog) for dog in dogs]

        return cls.all
    

    # returns a Dog instance corresponding to its database record retrieved by name.
    @classmethod
    def find_by_name(cls, name):
        sql = """
            SELECT * FROM dogs
            WHERE name = ?
            LIMIT 1
        """

        dog = CURSOR.execute(sql, (name,)).fetchone()

        if dog:
            return cls.new_from_db(dog)


    # returns a Dog instance corresponding to its database record retrieved by id.
    @classmethod
    def find_by_id(cls, id):
        sql = """
            SELECT * FROM dogs
            WHERE id = ?
            LIMIT 1
        """

        dog = CURSOR.execute(sql, (id,)).fetchone()

        if dog:
            return cls.new_from_db(dog)
    
    # This method takes a name and a breed as arguments. If there is already a dog in the database with the name and breed provided, 
    # it returns that dog. 
    # Otherwise, it inserts a new dog into the database, and returns the newly created dog.
    @classmethod
    def find_or_create_by(cls, name, breed):
        sql = """
            SELECT * FROM dogs 
            WHERE name = ? AND breed = ?
            LIMIT 1
        """

        dog = CURSOR.execute(sql, (name, breed)).fetchone()

        if not dog:
            new_dog = Dog(name, breed)
            new_dog.save()
            return new_dog
        else:  
            return cls.new_from_db(dog)
        

    #  a method "update()" that updates an instance's corresponding database record to match its new attribute values.
    def update(self):
        sql = """
            UPDATE dogs
            SET name = ?
            WHERE id = ?
        """

        CURSOR.execute(sql, (self.name, self.id))
        CONN.commit()

        



        
