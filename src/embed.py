import time

import numpy as np
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from qdrant_client.models import PointStruct as PS


class Timer:
    def __init__(self, action: str):
        self.action = action

    def __enter__(self):
        self.start_time = time.time()
        return self

    def __exit__(self, *args):
        self.end_time = time.time()
        self.elapsed_time = self.end_time - self.start_time
        print(f"{self.action} took {self.elapsed_time:.2f} seconds")


d_model = 128
n_points = 1_000
print(f"Using {n_points:,} points in {d_model}D space")

# client = QdrantClient(":memory:")  # in-memory Qdrant instance, for testing
client = QdrantClient(path="./db")  # in-memory Qdrant instance, for testing
if not client.collection_exists("test_collection"):
    client.create_collection(
        collection_name="test_collection",
        vectors_config=VectorParams(size=d_model, distance=Distance.COSINE),
    )


def random_vector(seed: int):
    rng = np.random.default_rng(seed)
    return rng.random(d_model).tolist()


with Timer("Build"):
    points = [
        PS(
            id=idx * n_points + frame_id,
            vector=random_vector(seed=idx * n_points + frame_id),
            payload={"city": city, "frame": frame_id},
        )
        for idx, city in enumerate("Berlin London Moscow NYC Beijing Mumbai".split())
        for frame_id in range(n_points)
    ]
with Timer("Upsert"):
    operation_info = client.upsert(
        collection_name="test_collection", wait=True, points=points
    )

with Timer("Query"):
    search_result = client.query_points(
        collection_name="test_collection",
        query=random_vector(seed=123),
        with_payload=True,
        with_vectors=True,
        limit=3,
    ).points

for res in search_result:
    print(res.model_dump_json(indent=2, exclude=["vector"], exclude_unset=True))
