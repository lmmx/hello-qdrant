import time

import numpy as np
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams


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


cities = "Berlin London Moscow NYC Beijing Mumbai".split()
n_cities = len(cities)
d_model = 128
n_points_per = 16_700
total_points = n_points_per * n_cities
batch_size = 2_000
print(f"Using {total_points:,} points in {d_model}D space in batches of {batch_size:,}")

# client = QdrantClient(":memory:")  # in-memory Qdrant instance, for testing
client = QdrantClient(url="http://localhost:6333", prefer_grpc=True)
if not client.collection_exists("test_collection"):
    client.create_collection(
        collection_name="test_collection",
        vectors_config=VectorParams(size=d_model, distance=Distance.COSINE),
    )


def random_vector(seed: int):
    rng = np.random.default_rng(seed)
    return rng.random(d_model).tolist()


def yield_rows():
    for frame_id in range(n_points_per):
        for idx, city in enumerate(cities):
            yield PointStruct(
                id=idx * n_points_per + frame_id,
                vector=random_vector(seed=idx * n_points_per + frame_id),
                payload={"city": city, "frame": frame_id},
            )


batch_n = 0
tbc = True
generator = yield_rows()
with Timer("Upsert"):
    while tbc:
        batch_n += 1
        print(f"Processing batch {batch_n}")
        points = []
        for n in range(batch_size):
            try:
                points.append(next(generator))
            except StopIteration:
                tbc = False
        if points:
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

# for res in search_result:
#     print(res.model_dump_json(indent=2, exclude=["vector"], exclude_unset=True))
