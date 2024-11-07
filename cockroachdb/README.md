# Installing cockroachdb example


## Install using helm
```sh
helm repo add cockroachdb https://charts.cockroachdb.com/
helm repo update
```

values.yaml
```
statefulset:
  resources:
    limits:
      memory: "2Gi"
    requests:
      memory: "2Gi"
conf:
  cache: "1Gi"
  max-sql-memory: "1Gi"
tls:
  enabled: false
```

# Install
```sh
helm install cockroachdb --values values.yaml cockroachdb/cockroachdb
```

# Verify the pods/pvs
```sh
kubectl get pods
kubectl get pv
```

# Proxy the dashboard
```sh
kubectl port-forward -n default cockroachdb-0 8080
```

http://localhost:8080

# Use the built-in SQL client
```sh
kubectl run -it --rm cockroach-client \
  --image=cockroachdb/cockroach \
  --restart=Never \
  --command -- \
  ./cockroach sql --insecure --host=cockroachdb-public.default
```

## SQL command promt
```sql
root@cockroachdb-public.default:26257/defaultdb>

> CREATE DATABASE bank;

> \c bank

> CREATE TABLE bank.accounts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    balance DECIMAL
  );

> INSERT INTO bank.accounts (balance)
  VALUES
      (1000.50), (20000), (380), (500), (55000);

> SELECT * FROM bank.accounts;

> \q
```


## Scale from 3 to 4 nodes
```sh
helm upgrade \
  cockroachdb \
  cockroachdb/cockroachdb \
  --set statefulset.replicas=4 \
  --reuse-values
```

## Simulate node failure
```sh
kubectl delete pod cockroachdb-2
kubectl get pods
```

## Stop the cluster
```sh
helm uninstall cockroachdb
```


# Rerefences
- https://www.cockroachlabs.com/docs/stable/deploy-cockroachdb-with-kubernetes
- https://www.cockroachlabs.com/docs/v24.2/deploy-cockroachdb-with-kubernetes-insecure?filters=helm
- https://www.cockroachlabs.com/docs/v24.2/scale-cockroachdb-kubernetes?filters=helm