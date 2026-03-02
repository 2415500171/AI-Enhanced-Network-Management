import pandas as pd
import numpy as np

df = pd.DataFrame({
    "traffic": np.random.randint(50, 500, 1000),
    "latency": np.random.randint(1, 200, 1000),
    "packet_loss": np.random.rand(1000)
})

df.to_csv("data/network_data.csv", index=False)
print("Network data generated")
