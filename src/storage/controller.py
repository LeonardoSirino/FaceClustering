import sqlite3 as sql
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Image:
    hash: str
    path: str


@dataclass
class Location:
    image_hash: str
    box: str
    encoding: bytes
    label_id: Optional[str] = None
    _id: int = -1

    def __repr__(self) -> str:
        return f'Location(image_hash={self.image_hash[:5]}, box={self.box}, encoding={len(self.encoding)} bytes, label_id={self.label_id})'


@dataclass
class Labels:
    name: str
    _id: int = -1


class Controller:
    def __init__(self):
        self.__conn = sql.connect('storage.db')
        self.__cursor = self.__conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.__cursor.execute("""CREATE TABLE IF NOT EXISTS images
                            (
                                hash TEXT PRIMARY KEY NOT NULL,
                                path TEXT
                            )""")

        self.__cursor.execute("""CREATE TABLE IF NOT EXISTS labels
                            (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name TEXT
                            )""")

        self.__cursor.execute("""CREATE TABLE IF NOT EXISTS locations
                            (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                image_hash TEXT NOT NULL,
                                label_id INTEGER,
                                box TEXT,
                                encoding BLOB,
                                FOREIGN KEY(label_id) REFERENCES labels(id),
                                FOREIGN KEY(image_hash) REFERENCES images(hash)
                            )""")

    def get_images_hashes(self):
        self.__cursor.execute('SELECT hash FROM images')
        return [i[0] for i in self.__cursor.fetchall()]

    def get_locations(self, unlabeled: bool) -> List[Location]:
        """
        Reads all locations from the database.

        Args:
        - unlabeled: if True, return only unlabeled locations
        """
        stmt = """SELECT image_hash, box, encoding, label_id, id 
                            FROM locations"""
        if unlabeled:
            stmt += " WHERE label_id IS NULL or label_id = '-1'"

        self.__cursor.execute(stmt)
        locations = [Location(*i) for i in self.__cursor.fetchall()]

        return locations

    def add_images(self, images: List[Image]):
        params = [(img.hash, str(img.path)) for img in images]
        self.__cursor.executemany("""INSERT INTO images(hash, path)
                                    VALUES(?, ?)""", params)
        self.__conn.commit()

    def add_locations(self, locations: List[Location]):
        params = [(loc.image_hash, loc.label_id, loc.box, loc.encoding)
                  for loc in locations]
        self.__cursor.executemany("""INSERT INTO locations(image_hash, label_id, box, encoding)
                                    VALUES(?, ?, ?, ?)""", params)
        self.__conn.commit()
