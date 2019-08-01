from pathlib import Path
import records


def get_database() -> records.Database:
    database_path = Path('./monopoly.db')
    return records.Database("sqlite:///" + str(database_path))


db = get_database()

