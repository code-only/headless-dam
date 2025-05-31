# utils/es_indexing.py
from utils.es import es, ES_INDEX


def index_asset(asset: dict):
    """
    Index a new asset in the Elasticsearch index.
    :param asset: The asset data to index, should be a dict with at least an 'id' field.
    """
    # asset should be a dict with at least an 'id' field
    es.index(index=ES_INDEX, id=asset["id"], document=asset)


def update_asset_index(asset_id: str, asset: dict):
    """
    Update an existing asset in the Elasticsearch index.
    :param asset_id: The ID of the asset to update.
    :param asset: The asset data to update, should be a dict.
    """
    es.update(index=ES_INDEX, id=asset_id, doc={"doc": asset})


def delete_asset_index(asset_id: str):
    """
    Delete an asset from the Elasticsearch index.
    :param asset_id: The ID of the asset to delete.
    """
    es.delete(index=ES_INDEX, id=asset_id, ignore=[404])

