#!/usr/bin/env -S uvx autopep723
import pandas as pd
import requests

response = requests.get("https://jsonplaceholder.typicode.com/users")
df = pd.DataFrame(response.json())
print(df.head())
