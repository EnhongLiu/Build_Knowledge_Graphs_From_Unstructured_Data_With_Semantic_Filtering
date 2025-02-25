import pandas as pd
import numpy as np

dfg1.to_csv("./graph_test_200.csv", sep="|", index=False)

dfg1 = pd.read_csv("./graph_test_200.csv", sep="|")
dfg1.replace("", np.nan, inplace=True)
dfg1.dropna(subset=["node_1", "node_2",'edge'], inplace=True)
# dfg1.drop(columns=["node_3"], inplace=True)
dfg1['count'] = 1 ## It's just an assigned weights to count the number of times a pair of nodes are connected.  
print(dfg1.shape)
dfg1.head()
