#!/usr/bin/env python3
"""8-all
"""


def list_all(mongo_collection):
    """lists all documents in a collection
    Args:
        mongo_collection: The pymongo collection object.

    Returns:
        A list of documents in the collection.
        An empty list if no documents are found.
    """
    documents = list(mongo_collection.find())
    return documents
