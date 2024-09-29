class Config:
    DB_USER = "user"
    DB_HOST = "localhost"
    DB_PORT = "3306"
    DB_NAME = "your_database_name"

    @staticmethod
    def get_database_url(password):
        return f"mysql://{Config.DB_USER}:{password}@{Config.DB_HOST}:{Config.DB_PORT}/{Config.DB_NAME}"