<div align="center">
<img src="https://user-images.githubusercontent.com/47891196/139104117-aa9c2943-37da-4534-a584-e4e5ff5bf69a.png" width="350px" />
</div>

# PASSO 1

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
 ├── enviroments/
 │   ├── dev/
 │   │   └── app.yaml
 │   └── prod/
 │       └── app.yaml
```
👉 Aqui está o segredo:

apps/nginx → código da aplicação
enviroments/dev → como rodar no DEV
enviroments/prod → como rodar no PROD

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
kubectl apply -f enviroments/dev/app.yaml
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
replicas: 2
```

# PASSO 2

🧠 🎯 O que vamos construir

Uma aplicação com:

Frontend (web) → interface
Backend (Python) → API
Banco de dados → metadados das imagens
Storage → salvar imagens
Deploy via Argo CD

🏗️ 📐 Arquitetura

```
[ Browser ]
     ↓
[ Frontend (React ou HTML simples) ]
     ↓
[ Backend (FastAPI) ]
     ↓
[ PostgreSQL ]
     ↓
[ Volume (PVC) → imagens salvas ]
```

📁 Estrutura no seu repo

Adicione isso no seu repo:

```k8s-argo-cd/
├── apps
│   ├── image-app
│   │   ├── backend
│   │   │   ├── main.py
│   │   │   └── Dockerfile
│   │   ├── frontend
│   │   │   ├── index.html
│   │   │   └── Dockerfile
│   │   └── k8s
│   │       ├── backend-deployment.yaml
│   │       ├── frontend-deployment.yaml   ✅
│   │       ├── frontend-service.yaml      ✅
│   │       ├── ingress.yaml               ✅
│   │       ├── postgres.yaml
│   │       └── pvc.yaml
│   └── nginx
│       ├── deployment.yaml
│       └── service.yaml
├── environments   ✅
│   ├── dev
│   │   ├── nginx.yaml
│   │   └── image-app.yaml   ✅
│   └── prod
│       └── image-app.yaml

```
🐍 🧠 Backend (Python com FastAPI)

Use FastAPI

📄 backend/main.py


```
from fastapi import FastAPI, UploadFile, File
from fastapi.staticfiles import StaticFiles
import shutil
import os

app = FastAPI()

UPLOAD_DIR = "/data/images"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"filename": file.filename}

@app.get("/images")
def list_images():
    return os.listdir(UPLOAD_DIR)

app.mount("/images", StaticFiles(directory=UPLOAD_DIR), name="images")
```
🌐 Frontend simples (HTML + JS)
📄 frontend/index.html

```
<!DOCTYPE html>
<html>
<head>
  <title>Image App</title>
</head>
<body>
  <h1>Upload de Imagem</h1>

  <input type="file" id="fileInput">
  <button onclick="upload()">Upload</button>

  <h2>Galeria</h2>
  <div id="gallery"></div>

  <script>
    async function upload() {
      const file = document.getElementById("fileInput").files[0];
      const formData = new FormData();
      formData.append("file", file);

      await fetch("/api/upload", {
        method: "POST",
        body: formData
      });

      loadImages();
    }

    async function loadImages() {
      const res = await fetch("/api/images");
      const images = await res.json();

      const gallery = document.getElementById("gallery");
      gallery.innerHTML = "";

      images.forEach(img => {
        const el = document.createElement("img");
        el.src = "/api/images/" + img;
        el.style.width = "200px";
        el.onclick = () => {
          document.body.style.backgroundImage = `url(${el.src})`;
        };
        gallery.appendChild(el);
      });
    }

    loadImages();
  </script>
</body>
</html>
```
💾 Persistência (PVC)
📄 pvc.yaml

```
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: image-pvc
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi
```

🐘 Banco (PostgreSQL simples)
📄 postgres.yaml

```
apiVersion: v1
kind: Pod
metadata:
  name: postgres
spec:
  containers:
  - name: postgres
    image: postgres:15
    env:
    - name: POSTGRES_PASSWORD
      value: "postgres"
```

⚙️ Backend Deployment
📄 backend-deployment.yaml

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend
spec:
  replicas: 1
  selector:
    matchLabels:
      app: backend
  template:
    metadata:
      labels:
        app: backend
    spec:
      containers:
      - name: backend
        image: sua-imagem-backend
        volumeMounts:
        - mountPath: /data/images
          name: image-storage
      volumes:
      - name: image-storage
        persistentVolumeClaim:
          claimName: image-pvc
```

🌐 📦 1. frontend-deployment.yaml

📄 apps/image-app/k8s/frontend-deployment.yaml

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: image-app-frontend
  labels:
    app: frontend
spec:
  replicas: 2
  selector:
    matchLabels:
      app: frontend
  strategy:
    type: RollingUpdate
  template:
    metadata:
      labels:
        app: frontend
    spec:
      containers:
      - name: frontend
        image: nginx:alpine
        ports:
        - containerPort: 80

        resources:
          requests:
            cpu: "100m"
            memory: "128Mi"
          limits:
            cpu: "300m"
            memory: "256Mi"

        volumeMounts:
        - name: frontend-content
          mountPath: /usr/share/nginx/html

      volumes:
      - name: frontend-content
        configMap:
          name: frontend-config
```

🌍 📦 2. ingress.yaml (para acesso via navegador)

📄 apps/image-app/k8s/ingress.yaml

```
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: image-app-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  rules:
  - host: image.local
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: image-app-frontend
            port:
              number: 80
```

🌐 Service + acesso local

Para simplificar no seu lab:

```
apiVersion: v1
kind: Service
metadata:
  name: frontend
spec:
  type: NodePort
  selector:
    app: frontend
  ports:
    - port: 80
      targetPort: 80
```
🌍 Melhor opção (recomendado)

👉 Use Ingress (produção-like)

```
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: image-app
spec:
  rules:
  - host: image.local
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: frontend
            port:
              number: 80
```
🧠 Configurar domínio local

No seu /etc/hosts:
```
docker ps --format "table {{.Names}}"
NAMES
k8s-ia-control-plane
k8s-ia-worker2
k8s-ia-worker

docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' k8s-ia-control-plane
172.18.0.4
```
Depois:

```
sudo nano /etc/hosts
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