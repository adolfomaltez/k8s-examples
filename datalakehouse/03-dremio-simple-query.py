from dremio_simple_query.connect import get_token, DremioConnection
import polars as pl
import seaborn as sns
import matplotlib.pyplot as plt

# Dremio login details
login_endpoint = "http://dremio:9047/apiv2/login"
payload = {
    "userName": "admin",  # Dremio username
    "password": "password1!"  # Dremio password
}

# Get the token
token = get_token(uri=login_endpoint, payload=payload)

# Dremio Arrow Flight endpoint (no SSL for local setup)
arrow_endpoint = "grpc://dremio:32010"

# Create the connection
dremio = DremioConnection(token, arrow_endpoint)

# Query the Gold dataset
query = "SELECT * FROM nessie.sales.sales_data_gold;"
df = dremio.toPolars(query)

# Display the Polars DataFrame
print(df)

# Convert the Polars DataFrame to a Pandas DataFrame for Seaborn visualization
df_pandas = df.to_pandas()

# Create a bar plot of total sales by product
sns.barplot(data=df_pandas, x="product", y="total_sales", palette="viridis", hue="product")
plt.title("Total Sales by Product")
plt.xlabel("Product")
plt.ylabel("Total Sales")
plt.xticks(rotation=45)
plt.show()

