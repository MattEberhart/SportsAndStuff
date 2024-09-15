from sqlalchemy.types import TypeDecorator, String

class CommaSeparatedInteger(TypeDecorator):
    """
    This class is a custom SQLAlchemy TypeDecorator which is designed to get
    comma separated integers from database and convert them into list of integers,
    and convert list of integers back into comma separated integers before storing into database.
    """
    impl = String

    def process_literal_param(self, value, dialect):
        if value is not None:
            return [int(v) for v in value.split(",")]
        else:
            return []

    def process_bind_param(self, value, dialect):
        if value is not None:
            return ",".join([str(v) for v in value])
        else:
            return None

    def process_result_value(self, value, dialect):
        if value is not None:
            return [int(v) for v in value.split(",")]
        else:
            return []