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
- Enable BGPPolicy

```sh
export EDITOR=nano
kubectl edit cm antrea-config -n kube-system

kubectl rollout restart deployment/antrea-controller -n kube-system
kubectl rollout restart daemonset/antrea-agent -n kube-system
```

## Configure BGP on router
```sh
configure terminal
ip forwarding
router-id 10.63.16.2
router bgp 64520
neighbor 10.63.16.101 remote-as 64520
neighbor 10.63.16.102 remote-as 64520
neighbor 10.63.16.103 remote-as 64520
exit
write memory
```

## Deploy BGP
```sh
kubectl  apply -f antrea-bgp.yaml
```


## Verify BGP peers
```sh
show ip bgp neighbors
```

## Deploy hello
```sh
kubectl  apply -f hello.yaml
```


# Reference
- https://antrea.io/docs/v2.1.0/docs/bgp-policy/