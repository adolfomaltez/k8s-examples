# Microsoft SQL Server AG on Kubernetes

## Create namespace
```sh
kubectl create namespace mssql
```
## Create secret
```sh
export MSSQL_SA_PASSWORD=p@ssword1!
kubectl create secret generic mssql-secret --from-literal=MSSQL_SA_PASSWORD="$MSSQL_SA_PASSWORD" -n mssql
```

## Deploy on k8s

### Create PVCs
```sh
kubectl -n mssql apply -f 01-PVCs.yaml
```

### Deploy MSSQL instances
```sh
kubectl -n mssql apply -f 02-mssql-primary.yaml 
kubectl -n mssql apply -f 03-mssql-secondary1.yaml 
kubectl -n mssql apply -f 04-mssql-secondary2.yaml 
```
### Verify pods and get pod's name
```sh
kubectl -n mssql get pods
podagp=$(kubectl -n mssql get pods -l app=mssql-primary -o json | jq -r '.items[0].metadata.name')
podags1=$(kubectl -n mssql get pods -l app=mssql-secondary1 -o json | jq -r '.items[0].metadata.name')
podags2=$(kubectl -n mssql get pods -l app=mssql-secondary2 -o json | jq -r '.items[0].metadata.name')
```

## Create AG
```sh
cat AG1-Primary-CreateandAdd.sql | kubectl -n mssql exec -it $podagp -- /bin/bash -c '/opt/mssql-tools18/bin/sqlcmd -C -S localhost -U SA -P "$MSSQL_SA_PASSWORD"'
```

### Create certificate and copy to secondary nodes
```sh
PathToCopyCert=${podagp}":var/opt/mssql/ag_certificate.cert"
PathToCopyCertKey=${podagp}":var/opt/mssql/ag_certificate.key"
kubectl -n mssql cp $PathToCopyCert ag_certificate.cert
kubectl -n mssql cp $PathToCopyCertKey ag_certificate.key
kubectl -n mssql cp ag_certificate.cert  $podags1:var/opt/mssql
kubectl -n mssql cp ag_certificate.key  $podags1:var/opt/mssql
kubectl -n mssql cp ag_certificate.cert $podags2:var/opt/mssql
kubectl -n mssql cp ag_certificate.key $podags2:var/opt/mssql
```

### Create and Add secondary nodes to AG
```sh
cat AG2-Secondary-CreateandAdd.sql | kubectl -n mssql exec -it $podags1 -- /bin/bash -c '/opt/mssql-tools18/bin/sqlcmd -C -S localhost -U SA -P "$MSSQL_SA_PASSWORD"'
cat AG3-Secondary-CreateandAdd.sql | kubectl -n mssql exec -it $podags2 -- /bin/bash -c '/opt/mssql-tools18/bin/sqlcmd -C -S localhost -U SA -P "$MSSQL_SA_PASSWORD"'
```


###
```sh
cat AG4-Primary--Collect.sql       | kubectl -n mssql exec -it $podagp -- /bin/bash -c '/opt/mssql-tools18/bin/sqlcmd -C -S localhost -U SA -P "$MSSQL_SA_PASSWORD"'
cat AG5-Primary--Queryreplicas.sql | kubectl -n mssql exec -it $podagp -- /bin/bash -c '/opt/mssql-tools18/bin/sqlcmd -C -S localhost -U SA -P "$MSSQL_SA_PASSWORD"'
cat AG6-Primary--CreateData.sql    | kubectl -n mssql exec -it $podagp -- /bin/bash -c '/opt/mssql-tools18/bin/sqlcmd -C -S localhost -U SA -P "$MSSQL_SA_PASSWORD"'
```

## Test on sqlcmd cli on pods
```sh
# Primary
kubectl exec -it $podagp -- /bin/bash -c '/opt/mssql-tools18/bin/sqlcmd -C -S localhost -U SA -P "$MSSQL_SA_PASSWORD"'

# Secondary 1
kubectl exec -it $podags1 -- /bin/bash -c '/opt/mssql-tools18/bin/sqlcmd -C -S localhost -U SA -P "$MSSQL_SA_PASSWORD"'

# Secondary 2
kubectl exec -it $podags2 -- /bin/bash -c '/opt/mssql-tools18/bin/sqlcmd -C -S localhost -U SA -P "$MSSQL_SA_PASSWORD"'

```

# References
- [Deploying Sql Server Always On Availability Group on Kubernetes](https://pradeepl.com/blog/kubernetes/deploying-sql-server-on-kubernetes/)
- [Microsoft: Quickstart: Run SQL Server Linux container images with Docker](https://learn.microsoft.com/en-us/sql/linux/quickstart-install-connect-docker?view=sql-server-ver16&pivots=cs1-bash)
- [Microsoft: Deploy SQL Server Linux containers on Kubernetes with StatefulSets](https://learn.microsoft.com/en-us/sql/linux/sql-server-linux-kubernetes-best-practices-statefulsets?view=sql-server-ver16)
- [Microsoft: Quickstart: Install SQL Server and create a database on Ubuntu](https://learn.microsoft.com/en-us/sql/linux/quickstart-install-connect-ubuntu?view=sql-server-ver16&tabs=ubuntu2004)
- [Microsoft: Configure SQL Server settings with environment variables on Linux](https://learn.microsoft.com/en-us/sql/linux/sql-server-linux-configure-environment-variables?view=sql-server-ver16)
- [Docker Mssql Tools](https://hub.docker.com/_/microsoft-mssql-tools)
- [Microsoft: Tutorial: Configure Active Directory authentication with SQL Server on Linux containers](https://learn.microsoft.com/en-us/sql/linux/sql-server-linux-containers-ad-auth-adutil-tutorial?view=sql-server-ver16)
