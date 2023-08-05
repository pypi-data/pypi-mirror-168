Clustering using different non-parameteric models with the power of bert embeddings

## Usage

```python
# import the crp algorithm
from embed_clustering.latent_component import crp_algorithm

# read the data you want to cluster
import pandas as pd
df = pd.read_csv('sample.csv')

corpus = df[column] # mention the column you want to cluster

# apply the algorithm by passing the parameters
df['cluster'] = crp_algorithm(corpus, compute='cuda', cleaning=True) #if you have gpu, else computer='cpu', if you doesn't wish to clean the text before clustering you can flag cleaning=False

```

## License
[MIT](https://choosealicense.com/licenses/mit/)