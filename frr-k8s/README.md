## Clone the vagrant-infrastructure project
```sh
git clone https://github.com/adolfomaltez/vagrant-infrastructure
```

## Deploy kubernetes on vagrant (3x worker nodes)
```sh
cd vagrant-infrastructure/kubernetes-cluster
vagrant up
vagrant ssh master
```

## Deploy ubuntu router on vagrant
```sh
cd vagrant-infrastructure/vagrant-ubuntu-router
vagrant up
vagrant ssh router
```

## Change default gateway on vtysh router

```sh
ip route del default 
ip route add default via 192.168.31.1
```

## Change default gateway on k8s nodes

```sh
ip route del default 
ip route add default via 10.63.16.2
```

## Add static routes to k8s cluster on local laptop
```sh
ip route add 10.63.16.0/24 via 192.168.31.22
ip route add 10.10.235.0/27 via 192.168.31.22
```

## Config antrea on cluster
- Enable Egress
- Enable ServiceExternalIP
- Enable EgressSeparateSubnet

```sh
export EDITOR=nano
kubectl edit cm antrea-config -n kube-system

kubectl rollout restart deployment/antrea-controller -n kube-system
kubectl rollout restart daemonset/antrea-agent -n kube-system
```

## Install helm on master
- https://helm.sh/docs/intro/install/

```sh
curl https://baltocdn.com/helm/signing.asc | gpg --dearmor | sudo tee /usr/share/keyrings/helm.gpg > /dev/null
sudo apt-get install apt-transport-https --yes
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/helm.gpg] https://baltocdn.com/helm/stable/debian/ all main" | sudo tee /etc/apt/sources.list.d/helm-stable-debian.list
sudo apt-get update
sudo apt-get install helm
```

## Install frr-k8s:

- https://github.com/metallb/frr-k8s
```sh
kubectl create namespace frr
helm repo add frr-k8s https://metallb.github.io/frr-k8s
helm install frr-k8s frr-k8s/frr-k8s -n frr
```

## Configure FRRconfiguration for BGP peer on cluster
```sh
kubectl  apply -f frr.yaml
```

## Configure BGP on router
```sh
configure terminal
ip forwarding
router-id 10.63.16.2
router bgp 64500
neighbor 10.63.16.101 remote-as 64500
neighbor 10.63.16.102 remote-as 64500
neighbor 10.63.16.103 remote-as 64500
exit
write memory
```


## Verify BGP peers
```sh
show ip bgp neighbors
```

## Deploy hello
```sh
kubectl  apply -f hello.yaml
```