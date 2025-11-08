class DBConnector:
   
    def __init__(self, db_type, user, password, host, database, port=None):
       
        self.db_type = db_type.lower()
        self.user = user
        self.password = password
        self.host = host
        self.database = database
        
        if port:
            self.port = port
        else:
            self.port = 3306 if self.db_type == "mysql" else 5432

        self.engine = self.create_engine()

    def create_engine(self):
        if self.db_type == "mysql":
            conn_str = f"mysql+mysqlconnector://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"
        elif self.db_type == "postgres":
            conn_str = f"postgresql+psycopg2://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"
        else:
            raise ValueError("Unsupported db_type. Use 'mysql' or 'postgres'.")
        
        return create_engine(conn_str)

    def execute_query(self, query, params=None, fetch=True):
        try:
            with self.engine.connect() as connection:
                result = connection.execute(text(query), params or {})

                if fetch and query.strip().lower().startswith("select"):
                    return result.fetchall()
                else:
                    connection.commit()
                    return None
        except SQLAlchemyError as e:
            print(f"Database Error as {e}")
            return None

    def close(self):
        self.engine.dispose()