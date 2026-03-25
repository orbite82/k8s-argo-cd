<div align="center">
<img src="https://user-images.githubusercontent.com/47891196/139104117-aa9c2943-37da-4534-a584-e4e5ff5bf69a.png" width="350px" />
</div>

# k8s-argo-cd
k8s-argo-cd

🚀 Criar o cluster com único comando
Execute:

```
bash
kind create cluster --name k8s-ia --config kind-config.yaml
```
--name k8s-ia → dá o nome ao cluster.

--config kind-cluster.yaml → usa o arquivo que define os nós.

🔍 Validar
Depois que terminar:

bash
kubectl get nodes
Você deve ver:

Código
NAME                  STATUS   ROLES           AGE   VERSION
k8s-ia-control-plane  Ready    control-plane   1m    v1.29.0
k8s-ia-worker         Ready    <none>          1m    v1.29.0
k8s-ia-worker2        Ready    <none>          1m    v1.29.0

🚀 1. Instalar Argo CD no seu cluster

```
kubectl create namespace argocd

kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```
Em caso de erro:

🧹 Solução 2: limpar e reinstalar

Se você já aplicou antes, faça:

```
kubectl delete namespace argocd
```
Espere deletar completamente:

```
kubectl get ns
```

Depois rode:

```
kubectl create namespace argocd
kubectl create -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

# OPCIONAL

🧹 1. Remover tudo do Argo CD
🔥 Opção mais simples (recomendada)

Se você instalou no namespace argocd:

```
kubectl delete namespace argocd
```
⏳ Aguarde remover completamente

```
kubectl get ns
```
Se ainda aparecer argocd como Terminating, aguarde alguns segundos.

⚠️ 2. (IMPORTANTE) Remover CRDs manualmente (se necessário)

Às vezes os CRDs ficam presos. Verifique:

```
kubectl get crds | grep argoproj
```
Se aparecer algo como:

applications.argoproj.io
applicationsets.argoproj.io

Remova:

```
kubectl delete crd applications.argoproj.io
kubectl delete crd applicationsets.argoproj.io
kubectl delete crd appprojects.argoproj.io
```
🚀 3. Instalar via Helm

Agora sim, instalação limpa:

```
helm repo add argo https://argoproj.github.io/argo-helm
helm repo update

helm install argocd argo/argo-cd -n argocd --create-namespace
```
# Em caso de Erro

💥 O problema
ClusterRole "argocd-application-controller" exists and cannot be imported...
invalid ownership metadata

👉 Tradução:

Recursos antigos ainda existem no cluster
Mas não foram criados pelo Helm
O Helm se recusa a “adotar” esses recursos por segurança

🔍 1. Encontrar recursos restantes

```
kubectl get clusterrole | grep argocd
kubectl get clusterrolebinding | grep argocd
```
🧹 2. Remover tudo do Argo CD (cluster-wide)

```
kubectl delete clusterrole argocd-application-controller
kubectl delete clusterrole argocd-server
kubectl delete clusterrole argocd-repo-server

kubectl delete clusterrolebinding argocd-application-controller
kubectl delete clusterrolebinding argocd-server
kubectl delete clusterrolebinding argocd-repo-server
```
⚠️ 3. Limpar CRDs (se ainda existirem)

```
kubectl get crds | grep argoproj
```
Se aparecer, remove:

```
kubectl delete crd applications.argoproj.io
kubectl delete crd applicationsets.argoproj.io
kubectl delete crd appprojects.argoproj.io
```
🧼 4. (Opcional, mas recomendado) limpeza geral

Se quiser garantir 100%:

```
kubectl get all -A | grep argocd
```

🚀 5. Instalar novamente via Helm

Agora sim, vai funcionar:

```
helm install argocd argo/argo-cd -n argocd --create-namespace --replace
```
🔍 6. Verificar se está distribuído nos nodes

```
kubectl get pods -n argocd -o wide
```
👉 Você deve ver pods rodando em nodes diferentes (worker1, worker2)

💡 Se quiser forçar comportamento mais real:

usar anti-affinity (nível avançado depois)

🔐 7. Acessar UI

```
kubectl port-forward svc/argocd-server -n argocd 8080:443
```
🌐 Como acessar o Argo CD via URL

Depois de rodar:

kubectl port-forward svc/argocd-server -n argocd 8080:443

👉 O acesso é:

https://localhost:8080

⚠️ Importante (HTTPS)

Vai aparecer aviso de segurança no navegador
👉 Isso é normal (certificado self-signed)
✔️ No navegador:
Clique em Avançado
Depois Continuar para localhost

🔐 Login : admin

Senha:
```
kubectl get secret argocd-initial-admin-secret -n argocd -o jsonpath="{.data.password}" | base64 -d
```

Usuário:

🧱 8. Ajuste IMPORTANTE para ambiente “produção-like”
👉 Use namespaces separados

Exemplo:
```
kubectl create namespace dev
kubectl create namespace prod
```
📦 5. Criar aplicações separadas (simulando ambientes)

No Argo CD:

app-dev

```
destination:
  namespace: dev
```
app-prod

```
destination:
  namespace: prod
```
🗂️ 1. Estrutura recomendada do Git

```
k8s-gitops-lab/
 ├── apps/
 │   └── nginx/
 │       ├── deployment.yaml
 │       ├── service.yaml
 ├── environments/
 │   ├── dev/
 │   │   └── app.yaml
 │   └── prod/
 │       └── app.yaml
```
👉 Aqui está o segredo:

apps/nginx → código da aplicação
environments/dev → como rodar no DEV
environments/prod → como rodar no PROD

🚀 ✅ 1. Forma rápida (kubectl — teste/local)

Se você só quer aplicar o apps/nginx direto no cluster:
```
🚀 ✅ 1. Forma rápida (kubectl — teste/local)

Se você só quer aplicar o apps/nginx direto no cluster:
```
👉 Isso aplica:

deployment.yaml
service.yaml

🔍 Verificar

```
kubectl get pods
kubectl get svc
```

🚀 Passo 3 — aplicar o Application (uma vez só)

```
kubectl apply -f environments/dev/app.yaml
```

🔍 Verificar no Argo CD

```
kubectl get applications -n argocd
```
Se tudo estiver certo, você vai ver algo como:

```
nginx-dev   Synced   Healthy
```
================================================================

🧠 🎯 Objetivo

Conectar o Argo CD ao seu repo:

👉 https://github.com/orbite82/k8s-argo-cd

🚀 ✅ 1. Forma mais simples (funciona direto)

Se o repo for público, você não precisa autenticação.

👉 Basta ajustar seu app.yaml:

```
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: nginx-dev
  namespace: argocd
spec:
  project: default

  source:
    repoURL: https://github.com/orbite82/k8s-argo-cd.git
    targetRevision: main
    path: apps/nginx

  destination:
    server: https://kubernetes.default.svc
    namespace: dev

  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```
⚠️ Atenção importante
✔️ targetRevision

Confere sua branch:

```
git branch
```
Se for main, ok.
Se for master, muda no YAML.

🚀 2. Aplicar no cluster

```
kubectl apply -f enviroments/dev/app.yaml
```
🔍 3. Verificar

```
kubectl get applications -n argocd
```
🌐 4. Ver no browser

👉 acessar:

https://localhost:8080

🔥 5. Teste REAL de GitOps

Agora faz isso:

✏️ altera no GitHub:

```
replicas: 3
```

```
```

```
```

```
```

```
```

```
```

```
```

```
```

```
```

```
```

```
```

```
```

```
```

```
```

```
```

```
```

```
```

```
```

```
```

```
```

```
```

```
```

```
```

```
```

```
```

```
```