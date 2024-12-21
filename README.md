# Hello Qdrant

Setting up qdrant client for local use

## Timing benchmarks

I include a simple benchmark of embedding random N-dimensional points for 6 cities
(trivial modification of the demo example in their docs).

- The rate-limiting step is the upsert.
- Faster speeds are obtained over gRPC and using localhost rather than persisting to disk.
    - In fact, persisting to disk is so rate limited that 1280D and 128D are the same speed.
    - The speedup from using gRPC is roughly an order of magnitude.

### 128D

- 98 seconds for 10^6
- 7 seconds for 10^5
- 0.9 seconds for 10^4

```
Using 10,020 points in 128D space in batches of 2,000
Processing batch 1
Processing batch 2
Processing batch 3
Processing batch 4
Processing batch 5
Processing batch 6
Upsert took 0.97 seconds
Query took 0.00 seconds
```

### 1280D

- 496 seconds for 10^6
- 33 seconds for 10^5
- 3 seconds for 10^4
- 0.3 seconds for 10^3

```
Using 1,002,000 points in 1280D space in batches of 200000
Processing batch 1
Processing batch 2
Processing batch 3
Processing batch 4
Processing batch 5
Processing batch 6
Upsert took 496.34 seconds
Query took 0.50 seconds
```
