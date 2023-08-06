"""
Defines a collection, storing data about the objects in the collection and the database to which it is relevant.
"""

from dataclasses import dataclass
from heaobject.root import HEAObjectDict
from ..db.database import DatabaseManager

from typing import TypeVar, Any, Type


@dataclass(frozen=True, eq=True, kw_only=True)
class CollectionKey:
    """
    A key to a collection that contains its name and relevant database manager class. CollectionKeys should only ever
    be used in testing environments.

    name: The name of the collection. If None, the key refers to any collection relevant to the given database manager.
     Required (keyword-only).
    db_manager_cls: A DatabaseManager type to which the collection is relevant. Defaults to DatabaseManager
    (keyword-only).
    """
    name: str | None
    db_manager_cls: Type[DatabaseManager] = DatabaseManager

    def coll_is_relevant_to(self, db_manager: DatabaseManager | Type[DatabaseManager]) -> bool:
        """
        Determines if the collection represented by this CollectionKey is relevant to the given database manager.
        :param db_manager: A DatabaseManager or DatabaseManager class.
        :return: True if the collection represented by this CollectionKey is relevant to the given database manager,
        otherwise False.
        """
        if isinstance(db_manager, type):
            return issubclass(db_manager, self.db_manager_cls)
        else:
            return isinstance(db_manager, self.db_manager_cls)

    def matches(self, other: 'str | CollectionKey', default_db_manager_cls: Type[DatabaseManager] = DatabaseManager) \
            -> bool:
        """
        Determines if the collection represented by this CollectionKey is represented by a part or entirety of the
        other string or CollectionKey. Since all DatabaseManagers inherit relevant collections from their superclasses,
        the database manager of the other collection key may be a subclass of the DatabaseManager class stored with
        this CollectionKey and vice versa.

        :param other: the other collection key, as either a string or CollectionKey (required).
        :param default_db_manager_cls: if other is a string, then this database manager class is used as the
        database manager class for the other collection key. Defaults to DatabaseManager (i.e. match
        any DatabaseManager).
        :return: True if the other collection key matches this one, otherwise False.
        """
        if isinstance(other, CollectionKey):
            other_ = other
        else:
            other_ = CollectionKey(name=str(other), db_manager_cls=default_db_manager_cls)
        return (self.name == other_.name if self.name is not None and other_.name is not None else True) \
            and (issubclass(self.db_manager_cls, other_.db_manager_cls) or issubclass(other_.db_manager_cls,
                                                                                      self.db_manager_cls))


def coll_is_relevant_to(key: str | CollectionKey, db_manager: DatabaseManager | Type[DatabaseManager]) -> bool:
    """
    Determines whether the collection represented by the given collection key is relevant to the given database
    manager. If the collection is a string, True will be returned.

    :param key: a collection key as a string or CollectionKey (required).
    :param db_manager: either a DatabaseManager or DatabaseManager class (required).
    :return: True if the collection represented by the given collection key is relevant to the given database
    manager, otherwise False.
    """
    if isinstance(key, CollectionKey):
        return key.coll_is_relevant_to(db_manager)
    else:
        return CollectionKey(name=str(key)).coll_is_relevant_to(db_manager)


def query_fixture_collection(fixtures: dict[str | CollectionKey, list[HEAObjectDict]], key: str | CollectionKey,
                             default_db_manager: DatabaseManager | Type[DatabaseManager] = DatabaseManager,
                             strict=True) -> list[HEAObjectDict] | None:
    """
    Get the collection with the given key.

    :param fixtures: The fixtures to query. Required.
    :param key: The name and database manager class must match those stored in the CollectionKey if
    key is a CollectionKey. If key is a string, then the database manager class is assumed to be default_db_manager.
    :param default_db_manager: The database manager to if the collection key is a string. Defaults to DatabaseManager.
    :param strict: If True, raises KeyError if nothing is found. If False, returns None if nothing is found. Defaults
    to True.
    :return: The objects in the collection that matches with the given key.
    """
    if fixtures is None:
        raise TypeError('fixtures may not be None')
    if isinstance(key, CollectionKey) and key.name is None:
        raise TypeError('the name of the CollectionKey may not be None when used as a parameter to '
                        'query_fixture_collection')
    result = query_fixtures(fixtures, default_db_manager=default_db_manager, strict=strict, key=key)
    if not result:
        return None
    else:
        return result[key.name if isinstance(key, CollectionKey) else key]


def query_content_collection(content: dict[str | CollectionKey, dict[str, bytes]], key: str | CollectionKey,
                             default_db_manager: DatabaseManager | Type[DatabaseManager] = DatabaseManager,
                             strict=True) -> dict[str, bytes] | None:
    """
    Get the collection with the given key.

    :param content: The content dictionary to query. If None, returns the empty dictionary. Required.
    :param key: The name and database manager class must match those stored in the CollectionKey if
    key is a CollectionKey. If key is a string, then the database manager class is assumed to be default_db_manager.
    :param default_db_manager: The database manager to use if the collection key is a string. Defaults to
    DatabaseManager.
    :param strict: If True, raises KeyError if nothing is found. If False, returns None if nothing is found. Defaults
    to True.
    :return: The content in the collection that matches with the given key.
    """
    if content is None:
        raise TypeError('content may not be None')
    if isinstance(key, CollectionKey) and key.name is None:
        raise TypeError('the name of the CollectionKey may not be None when used as a parameter to '
                        'query_fixture_collection')
    result = query_content(content, default_db_manager=default_db_manager, strict=strict, key=key)
    if not result:
        return None
    else:
        return result[key.name if isinstance(key, CollectionKey) else key]


def query_fixtures(fixtures: dict[str | CollectionKey, list[HEAObjectDict]] | None,
                   default_db_manager: DatabaseManager | Type[DatabaseManager] = DatabaseManager,
                   strict=False, *,
                   name: str = None,
                   db_manager: DatabaseManager | Type[DatabaseManager] = None,
                   key: str | CollectionKey = None) -> dict[str, list[HEAObjectDict]]:
    """
    Query a dictionary of fixtures by collection.

    :param fixtures: The fixtures to query. If the key to a collection is a string, then the database manager class
    will be assumed to be default_db_manager. If None, returns the empty dictionary. Required.
    :param default_db_manager: The database manager to if the collection key is a string. Defaults to DatabaseManager.
    :param strict: If True, raises KeyError if nothing is found. If False, an empty dictionary is returned. Defaults
    to False.
    :param name: If specified, the name of the collection must match the given name.
    :param db_manager: If specified, the database manager of the collection must be the given database manager, its
    class if it is an instance of a database manager, or a subclass.
    :param key: If specified, the name and database manager class must match those stored in the CollectionKey if
    key is a CollectionKey. If key is a string, it is the same as specifying name. Both name and db_manager are
    ignored if this argument is specified.
    :return: All the collections and their data that matches the given query parameters. Any CollectionKeys in the
    keys of the given fixtures are replaced with their names if key is either not specified or not a CollectionKey.
    """
    if not fixtures:
        return {}
    key_ = key if isinstance(key, CollectionKey) else CollectionKey(name=str(key) if key is not None else None)
    if db_manager is None or isinstance(db_manager, type(None)):
        db_manager_ = default_db_manager
    else:
        db_manager_ = db_manager if isinstance(db_manager, type) else type(db_manager)
    coll_key = key_ if key else CollectionKey(name=str(name) if name is not None else None, db_manager_cls=db_manager_)
    result = {(coll.name if isinstance(coll, CollectionKey) else coll): data
              for coll, data in fixtures.items() if coll_key.matches(coll,
                                                                     default_db_manager_cls=
                                                                     default_db_manager
                                                                     if isinstance(default_db_manager, type)
                                                                     else type(default_db_manager))}
    if result:
        return result
    elif strict:
        raise KeyError(f'query result is empty: {key_}')


def query_content(content: dict[str | CollectionKey, dict[str, bytes]] | None,
                  default_db_manager: DatabaseManager | Type[DatabaseManager] = DatabaseManager,
                  strict=False, *,
                  name: str = None,
                  db_manager: DatabaseManager | Type[DatabaseManager] = None,
                  key: str | CollectionKey = None) -> dict[str, dict[str, bytes]]:
    """
    Query a dictionary of content by collection.

    :param content: The content dictionary to query. If the key to a collection is a string, then the database manager
    class will be assumed to be default_db_manager. If None, returns the empty dictionary. Required.
    :param default_db_manager: The database manager to use if the collection key is a string. Defaults to
    DatabaseManager.
    :param strict: If True, raises KeyError if nothing is found. If False, an empty dictionary is returned. Defaults
    to False.
    :param name: If specified, the name of the collection must match the given name.
    :param db_manager: If specified, the database manager of the collection must be the given database manager, its
    class if it is an instance of a database manager, or a subclass.
    :param key: If specified, the name and database manager class must match those stored in the CollectionKey if
    key is a CollectionKey. If key is a string, it is the same as specifying name. Both name and db_manager are
    ignored if this argument is specified.
    :return: All the collections and their content that matches the given query parameters. Any CollectionKeys in the
    keys of the given content dictionary are replaced with their names.
    """
    if not content:
        return {}
    key_ = key if isinstance(key, CollectionKey) else CollectionKey(name=str(key) if key is not None else None)
    if db_manager is None or isinstance(db_manager, type(None)):
        db_manager_ = default_db_manager
    else:
        db_manager_ = db_manager if isinstance(db_manager, type) else type(db_manager)
    coll_key = key_ if key else CollectionKey(name=str(name) if name is not None else None, db_manager_cls=db_manager_)
    result = {(coll.name if isinstance(coll, CollectionKey) else coll): data
              for coll, data in content.items() if coll_key.matches(coll)}
    if result:
        return result
    elif strict:
        raise KeyError('query result is empty')


_T = TypeVar('_T')


def simplify_collection_keys(collections: dict[str | CollectionKey, _T]) -> dict[str, _T]:
    """
    Convert all CollectionKeys in the given collection dictionary to strings that are equal to their names.
    """
    return {(coll_key.name if isinstance(coll_key, CollectionKey) else coll_key): objs
            for coll_key, objs in collections.items()}


def convert_to_collection_keys(collections: dict[str | CollectionKey, _T],
                               default_db_manager: DatabaseManager | type[DatabaseManager] = DatabaseManager) \
                               -> dict[CollectionKey, _T]:
    """
    Convert all strings in the given collection dictionary to CollectionKeys using the given default database manager.
    """
    db_manager = default_db_manager if isinstance(default_db_manager, type) else type(default_db_manager)
    return {(key if isinstance(key, CollectionKey) else CollectionKey(name=key, db_manager_cls=db_manager)): objs
            for key, objs in collections.items()}


def get_key_from_name(collections: dict[str | CollectionKey, Any], name: str) -> str | CollectionKey | None:
    """
    Get the key to access the collection with the given name. If there are multiple collections with the same name,
    behavior is undefined because this should never happen. If there is no collection with the name, return None.
    """
    return next(iter([x for x in collections.keys() if (x.name if isinstance(x, CollectionKey) else str(x)) == name]),
                None)
