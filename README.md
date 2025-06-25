# enenso

This is a very technical POC on how to connect to [ensenso cameras](https://www.optonic.com/marken/ensenso/), when running in kubernetes.
The poc uses the `hostnetw`

## prerequisites

- install [kubectl](https://kubernetes.io/de/docs/tasks/tools/install-kubectl/)
- install [skaffold](https://skaffold.dev)
- for development recommended [k9s](https://k9scli.io)
- the [ensenso sdk](https://community.ensenso.com/t/ensenso-sdk-downloads/58)
- get the kubeconfig from the IPC
    - `ssh USERNAME@host "kubectl config view --raw" > kubeconfig`
    - adjust the host within `kubeconfig`
    - `export KUBECONFIG=./kubeconfig`
- adjust the image paths in `skaffold.yaml` and `k8s/kustomization.yaml`
- adjust secret name in `k8s/deployment.yaml`
- run `skaffold.run` (first might fail, when images cant be pulled)
- [add secrets](https://kubernetes.io/docs/tasks/configure-pod-container/pull-image-private-registry/) when using a private registry
```bash
kubectl create -n ensenso secret docker-registry regcred --docker-server=<your-registry-server> --docker-username=<your-name> --docker-password=<your-pword> --docker-email=<your-email>
```
- (optional) install "kubernetes" extension for vscode (e.g. to remote develop within the container)

## build the image

- [python interface](https://manual.ensenso.com/latest/python/)
- `./build.sh` for building only
- `./push.sh` for building and pushing to registry (image tag might need to be adjusted)
- for development and deployment you can use `skaffold run` or `skaffold dev`

## (internal) network config 

- wabo IPC
    - changed `enp1s0f0` `172.28.60.2/24` to `192.168.1.250/24`
