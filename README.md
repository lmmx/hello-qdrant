# Hello Qdrant

Setting up qdrant client for local use

## Timing benchmarks

I include a simple benchmark of embedding 1,000 random `d_model` dimensional points for 6 cities,
i.e. storing six thousand vectors in total.

Surprisingly, dimensionality of the vectors doesn't really matter: it performs poorly above 3 orders
of magnitude regardless.

The rate-limiting step is the upsert, poor performance beyond 1,000 points per city.

### 128D

- 35 seconds for 10^3
- 3 seconds for 10^2
- 0.3 seconds for 10^1

```
Using 1,000 points in 128D space
Build took 0.16 seconds
Upsert took 35.61 seconds
Query took 0.00 seconds
```

### 1280D

- 40 seconds for 10^3
- 3 seconds for 10^2
- 0.3 seconds for 10^1

```
Using 1,000 points in 1280D space                                                         
Build took 0.38 seconds                                                                   
Upsert took 38.89 seconds                                                                 
Query took 0.02 seconds                                                                   
```
