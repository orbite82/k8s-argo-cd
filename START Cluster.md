📌 Passo a passo para recuperar seus recursos
1. Inicie o Minikube novamente
bash
minikube start
Isso vai recriar o cluster e atribuir um novo IP (pode ser diferente do 192.168.58.2).

2. Verifique o status
bash
minikube status
Você deve ver algo como:

Código
host: Running
kubelet: Running
apiserver: Running
3. Descubra o novo IP
bash
minikube ip
4. Ajuste o /etc/hosts
Atualize o IP para os domínios que você configurou:

Código
<NOVO_IP> app.local
<NOVO_IP> argocd.local
5. Reaplique os manifests
Como o cluster foi reiniciado, os recursos podem ter sido apagados. Reaplique os YAMLs:

bash
kubectl apply -f cluster/namespaces.yaml
kubectl apply -f python-app/deployment.yaml -n hml
kubectl apply -f python-app/service.yaml -n hml
kubectl apply -f python-app/ingress.yaml -n hml
kubectl apply -f argocd/hml-prod-apps.yaml -n argocd
6. Verifique os pods
bash
kubectl get pods -n hml
kubectl get pods -n argocd
7. Se usar LoadBalancer
Não esqueça de rodar novamente:

bash
minikube tunnel
✅ Conclusão
Sempre que reiniciar a máquina, é preciso iniciar o Minikube novamente.

O IP muda, então você precisa atualizar o /etc/hosts.

Os recursos podem precisar ser reaplicados (a não ser que você configure um storage persistente).

O Argo CD vai sincronizar novamente assim que o cluster estiver ativo.