# Installing submariner on multiple k8s clusters


kind create cluster --config kind-cluster-c1.yaml
kind create cluster --config kind-cluster-c2.yaml


kubectl --context kind-c1
kubectl --context kind-c1 create -f https://raw.githubusercontent.com/projectcalico/calico/v3.26.3/manifests/tigera-operator.yaml

 nano tigera-c1.yaml
 nano tigera-c2.yaml
 
kubectl --context kind-c1 apply -f tigera-c1.yaml 


kubectl --context kind-c2 create -f https://raw.githubusercontent.com/projectcalico/calico/v3.26.3/manifests/tigera-operator.yaml
kubectl --context kind-c2 apply -f tigera-c2.yaml 

kubectl --context kind-c1 get pods -A
kubectl --context kind-c2 get pods -A

# References:
- https://piotrminkowski.com/2021/07/08/kubernetes-multicluster-with-kind-and-submariner/
- https://docs.tigera.io/calico/latest/getting-started/kubernetes/self-managed-onprem/onpremises
