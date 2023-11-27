# Microsoft SQL Server on Docker containers

## Create namespace
```sh
kubectl create namespace mssql
```
## Create secret
```sh
kubectl create secret generic mssql --from-literal=MSSQL_SA_PASSWORD="p@ssword1!" -n mssql
```

### Deploy on k8s
```sh
# Deploy one MSSQL container and attach the iSCSI LUN for R/W (one container at a time).
kubectl -n mssql create -f deployment-iscsi-rwo.yaml

# Deploy two (or more) MSSQL container(s) and mount the NFS share for R/W (multiple containers at same time).
kubectl -n mssql create -f deployment-nfs-rwx.yaml
```


## Connect to container CLI
```sh
kubectl exec -it mssql-pod-id -n mssql -- /bin/bash
/opt/mssql-tools/bin/sqlcmd -S localhost -U SA -P "p@ssword1!"
```

### Basic SQL commands:
```sql
SELECT name FROM sys.databases;
GO
CREATE DATABASE foo;
GO
USE foo;
CREATE TABLE Inventory (id INT, name NVARCHAR(50), quantity INT);
INSERT INTO Inventory VALUES (1, 'banana', 150);
INSERT INTO Inventory VALUES (2, 'orange', 154);
GO
SELECT * FROM Inventory WHERE quantity > 152;
GO
QUIT
```


# References
- [Deploying Sql Server Always On Availability Group on Kubernetes](https://pradeepl.com/blog/kubernetes/deploying-sql-server-on-kubernetes/)
- [Microsoft: Quickstart: Run SQL Server Linux container images with Docker](https://learn.microsoft.com/en-us/sql/linux/quickstart-install-connect-docker?view=sql-server-ver16&pivots=cs1-bash)
- [Microsoft: Deploy SQL Server Linux containers on Kubernetes with StatefulSets](https://learn.microsoft.com/en-us/sql/linux/sql-server-linux-kubernetes-best-practices-statefulsets?view=sql-server-ver16)
- [Microsoft: Quickstart: Install SQL Server and create a database on Ubuntu](https://learn.microsoft.com/en-us/sql/linux/quickstart-install-connect-ubuntu?view=sql-server-ver16&tabs=ubuntu2004)
- [Microsoft: Configure SQL Server settings with environment variables on Linux](https://learn.microsoft.com/en-us/sql/linux/sql-server-linux-configure-environment-variables?view=sql-server-ver16)
- [Docker Mssql Tools](https://hub.docker.com/_/microsoft-mssql-tools)
- [Microsoft: Tutorial: Configure Active Directory authentication with SQL Server on Linux containers](https://learn.microsoft.com/en-us/sql/linux/sql-server-linux-containers-ad-auth-adutil-tutorial?view=sql-server-ver16)
