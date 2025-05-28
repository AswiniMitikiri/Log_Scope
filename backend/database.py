from sqlalchemy import create_engine, Column, String, Integer, MetaData, Table

engine = create_engine("sqlite:///logs.db", echo=True)
metadata = MetaData()

logs_table = Table("logs", metadata,
                   Column("id", Integer, primary_key=True),
                   Column("timestamp", String),
                   Column("level", String),
                   Column("message", String))

metadata.create_all(engine)
