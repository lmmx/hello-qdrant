from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from qdrant_client.models import PointStruct as PS

client = QdrantClient(":memory:")  # in-memory Qdrant instance, for testing

client.create_collection(
    collection_name="test_collection",
    vectors_config=VectorParams(size=4, distance=Distance.DOT),
)
coll = client.get_collections().collections[0]
points = [
    PS(id=1, vector=[0.05, 0.61, 0.76, 0.74], payload={"city": "Berlin"}),
    PS(id=2, vector=[0.19, 0.81, 0.75, 0.11], payload={"city": "London"}),
    PS(id=3, vector=[0.36, 0.55, 0.47, 0.94], payload={"city": "Moscow"}),
    PS(id=4, vector=[0.18, 0.01, 0.85, 0.80], payload={"city": "New York"}),
    PS(id=5, vector=[0.24, 0.18, 0.22, 0.44], payload={"city": "Beijing"}),
    PS(id=6, vector=[0.35, 0.08, 0.11, 0.44], payload={"city": "Mumbai"}),
]
operation_info = client.upsert(
    collection_name="test_collection", wait=True, points=points
)

search_result = client.query_points(
    collection_name="test_collection",
    query=[0.2, 0.1, 0.9, 0.7],
    with_payload=True,
    with_vectors=True,
    limit=3,
).points

for res in search_result:
    print(res.model_dump_json(indent=2, exclude_unset=True))
