<div align="center">
<img src="https://user-images.githubusercontent.com/47891196/139104117-aa9c2943-37da-4534-a584-e4e5ff5bf69a.png" width="350px" />
</div>



# k8s-argo-cd
k8s-argo-cd

🌐 Passo 0: Arquitetura (Tree Layout)

```
k8s-argo-cd/
├── cluster/
│   ├── minikube-3-nodes              # Via comando Configuração do cluster local
│   ├── namespaces.yaml               # Namespaces HML e PROD
│   └── ingress.yaml                  # Ingress Controller para URLs
│
├── argo-cd/
│   ├── values.yaml                   # Configuração via Helm
│   ├── ingress-argocd.yaml           # Acesso via URL ao Argo CD
│   └── hml-prod-apps.yaml            # Definição dos ambientes
│
├── python-app/
│   ├── app.py                        # Aplicação Flask/Django
│   ├── requirements.txt              # Dependências
│   ├── Dockerfile                    # Imagem da aplicação
│   ├── deployment.yaml               # Deployment no Kubernetes
│   ├── service.yaml                  # Service para expor a aplicação
│   └── ingress.yaml                  # URL para acessar a aplicação
│
├── future-db/
│   ├── postgres-deployment.yaml      # Banco de dados (futuro)
│   ├── service.yaml
│   └── pvc.yaml                      # Persistência de dados
│
└── README.md                         # Documentação detalhada
```

📌 Passo 1: Criar Cluster Kubernetes via Minikube
Instalar Minikube e kubectl.

Criar cluster com 3 nós (lembrando que sua máquina tem 16GB RAM, então vamos limitar recursos):

```
minikube start --nodes=3 --memory=4096 --cpus=2
```
Ótimo passo inicial, Thiago! 🚀
Depois de criar o cluster com minikube start --nodes=3 --memory=4096 --cpus=2, você pode validar se tudo está funcionando com alguns comandos básicos do kubectl e do minikube. Aqui vai um checklist prático:

📌 Validação do Cluster
Verificar status do Minikube

minikube status

→ Confirma se os nós estão rodando e se o cluster está ativo.

Listar nós do cluster

kubectl get nodes

→ Deve mostrar os 3 nós (minikube, minikube-m02, minikube-m03) com status Ready.

Checar informações detalhadas dos nós

kubectl describe nodes

👉 Dica extra: use kubectl cluster-info para verificar os endpoints do cluster (API Server e DNS).

Para criar namespaces no Kubernetes você tem duas opções principais: via kubectl direto na linha de comando ou aplicando um manifesto YAML como o que você mostrou.

📌 Criando Namespaces com kubectl
Criar namespace de homologação (hml):

bash
kubectl create namespace hml
Criar namespace de produção (prod):

bash
kubectl create namespace prod
📌 Criando Namespaces com YAML
Você já tem o manifesto pronto. Basta aplicar:

bash
kubectl apply -f namespaces.yaml
Onde namespaces.yaml contém os dois blocos que você mostrou (hml e prod).

✅ Boas práticas
Separar ambientes: usar namespaces distintos para dev, hml e prod ajuda a organizar recursos e aplicar políticas diferentes.

Naming claro e curto: nomes simples (hml, prod) são melhores que nomes longos ou ambíguos.

RBAC por namespace: defina permissões específicas para cada ambiente, evitando que usuários de homologação tenham acesso ao prod.

Resource Quotas e LimitRanges: configure limites de CPU/memória por namespace para evitar que um ambiente consuma todos os recursos do cluster.

Labels: adicione labels nos namespaces para facilitar automação e seleção:

yaml
metadata:
  name: hml
  labels:
    environment: hml

📂 Estrutura de arquivos
Dentro da pasta cluster/ você pode separar assim:

deployment-ingress.yaml → Deployment do Ingress Controller (NGINX)

service-ingress.yaml → Service para expor o Ingress Controller

📌 Passo a passo para aplicar
Criar namespaces (se ainda não fez):

bash
kubectl apply -f namespaces.yaml
Aplicar o Deployment do Ingress Controller:

bash
kubectl apply -f deployment-ingress.yaml
Aplicar o Service:

bash
kubectl apply -f service-ingress.yaml

Validar se o Ingress Controller está rodando:

bash
kubectl get pods -n kube-system
kubectl get svc -n kube-system

# OBS Em caso de ERRO

Ingress Controller está em CrashLoopBackOff. Isso significa que o pod inicia, falha e fica reiniciando em loop.

🔎 Passos para diagnosticar
Ver logs do pod

bash
kubectl logs ingress-nginx-controller-56db97c99b-r6zls -n kube-system
→ Vai mostrar o motivo do crash (imagem não encontrada, configuração inválida, porta em conflito etc.).

erro está bem claro nos logs:

Código
F0326 ... Unexpected error obtaining ingress-nginx pod: unable to get POD information (missing POD_NAME or POD_NAMESPACE environment variable)
🔎 O que significa
O Ingress Controller precisa dessas variáveis de ambiente (POD_NAME e POD_NAMESPACE) para funcionar corretamente. Elas são injetadas automaticamente quando você usa os manifests oficiais do projeto ingress-nginx ou quando habilita o addon do Minikube.
No seu YAML manual, essas variáveis não foram configuradas, por isso o pod entra em CrashLoopBackOff.

✅ Como corrigir
Adicionar env vars no Deployment  
No deployment-ingress.yaml, dentro do container, inclua:

yaml
env:
  - name: POD_NAME
    valueFrom:
      fieldRef:
        fieldPath: metadata.name
  - name: POD_NAMESPACE
    valueFrom:
      fieldRef:
        fieldPath: metadata.namespace

O que mudou
Adicionei as variáveis de ambiente POD_NAME e POD_NAMESPACE que o Ingress Controller precisa para inicializar corretamente.

Mantive a imagem v1.9.0, mas se continuar dando problema, você pode atualizar para uma versão mais recente (ex.: v1.11.1).

🚀 Passo a passo para aplicar
Salve o arquivo como deployment-ingress.yaml.

Delete o pod antigo que está em loop:

bash
kubectl delete pod -n kube-system ingress-nginx-controller-56db97c99b-r6zls
Reaplique o manifesto corrigido:

bash
kubectl apply -f deployment-ingress.yaml
Verifique se o pod sobe corretamente:

bash
kubectl get pods -n kube-system

-------------------------------------------------------------------------------------------------

📌 Passo 2: Instalar Argo CD via Helm

Adicionar repositório Helm

```
helm repo add argo https://argoproj.github.io/argo-helm
helm repo update
```
Instalar Argo CD com seu values.yaml

helm install argocd argo/argo-cd -n argocd --create-namespace -f argocd/values.yaml



Ingress para acessar via URL local:

Validar instalação
bash
kubectl get pods -n argocd
kubectl get ingress -n argocd

5. Configurar acesso local
Descobrir IP do Minikube:

bash
minikube ip

# Em casos de Erro e Ajustes

╭─orbite at pop-os in ⌁/k8s-argo-cd (main ✚1…3)
╰─λ cat /etc/hosts                                                                             0 (37.437s) < 12:12:00
# See `man hosts` for details.
#
# By default, systemd-resolved or libnss-myhostname will resolve
# localhost and the system hostname if they're not specified here.
127.0.0.1	localhost
::1		localhost
172.18.0.4      image.local
192.168.58.2    argocd.local
╭─orbite at pop-os in ⌁/k8s-argo-cd (main ✚1…3)
╰─λ kubectl get ingress -n argocd                                                               0 (0.002s) < 12:12:10

NAME            CLASS   HOSTS                ADDRESS        PORTS   AGE
argocd-server   nginx   argocd.example.com   192.168.58.2   80      11m


✅ Como corrigir
Você tem duas opções:

Opção 1: Ajustar o Ingress para usar argocd.local
Edite o ingress-argocd.yaml ou o values.yaml e troque o host para argocd.local:

yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: argocd-server-ingress
  namespace: argocd
  annotations:
    kubernetes.io/ingress.class: "nginx"
spec:
  rules:
  - host: argocd.local
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: argocd-server
            port:
              number: 443
Depois aplique:

bash
kubectl apply -f argocd/ingress-argocd.yaml
Opção 2: Ajustar o /etc/hosts para usar argocd.example.com
Mantenha o Ingress como está e altere o /etc/hosts:

Código
192.168.58.2 argocd.example.com
E acesse no navegador:

Código
https://argocd.example.com

Valide:

bash
kubectl get ingress -n 


🔎 O que isso significa
O primeiro (argocd-server) foi criado automaticamente pelo Helm Chart, com host padrão argocd.example.com.

O segundo (argocd-server-ingress) foi criado manualmente por você, com host argocd.local.

Ambos apontam para o mesmo endereço (192.168.58.2) e usam o mesmo Ingress Controller (nginx).

✅ Como acessar corretamente
Se você mantiver o /etc/hosts com:

Código
192.168.58.2 argocd.example.com
→ Acesse no navegador: https://argocd.example.com


Obs Remnover o antigo ingress após a correção:

✅ Como deletar o Ingress argocd.local
Execute o comando abaixo:

bash
kubectl delete ingress argocd-server-ingress -n argocd
Isso vai remover apenas o recurso argocd-server-ingress (que estava configurado com host argocd.local).

📌 Depois da exclusão
Verifique novamente:

bash
kubectl get ingress -n argocd


6. Acessar no navegador

https://argocd.example.com/

7. Login inicial
Usuário: admin  
Senha:

kubectl get secret argocd-initial-admin-secret -n argocd -o jsonpath="{.data.password}" | base64 -d

-------------------------------------------------------------------------------------------------

📌 Passo 3: Aplicação Python

📂 Estrutura final do python-app
Código
python-app/
├── app.py
├── requirements.txt
├── Dockerfile
├── deployment.yaml
├── service.yaml
├── ingress.yaml
└── templates/
    └── index.html
app.py
python
from flask import Flask, request, render_template
import os

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["image"]
        if file:
            filepath = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filepath)
            return render_template("index.html", background=filepath)
    return render_template("index.html", background=None)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
requirements.txt
Código
Flask==3.0.2
Werkzeug==3.0.1
Dockerfile
dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
deployment.yaml
yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: python-app
  namespace: hml
spec:
  replicas: 1
  selector:
    matchLabels:
      app: python-app
  template:
    metadata:
      labels:
        app: python-app
    spec:
      containers:
      - name: python-app
        image: python-app:latest
        imagePullPolicy: IfNotPresent
        ports:
        - containerPort: 5000
service.yaml
yaml
apiVersion: v1
kind: Service
metadata:
  name: python-app-service
  namespace: hml
spec:
  selector:
    app: python-app
  ports:
    - protocol: TCP
      port: 5000
      targetPort: 5000
  type: ClusterIP
ingress.yaml
yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: python-app-ingress
  namespace: hml
spec:
  rules:
  - host: app.local
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: python-app-service
            port:
              number: 5000
Não esqueça de adicionar app.local ao seu /etc/hosts apontando para o IP do Minikube.

templates/index.html
html
<!DOCTYPE html>
<html>
<head>
    <title>Minha App Python</title>
    <style>
        body {
            background-image: url("{{ background }}");
            background-size: cover;
            background-repeat: no-repeat;
            background-position: center;
        }
    </style>
</head>
<body>
    <h1>Upload de Imagem</h1>
    <form method="POST" enctype="multipart/form-data">
        <input type="file" name="image">
        <button type="submit">Enviar</button>
    </form>
</body>
</html>

📌 Passo a Passo – Aplicação Python

1. Build da imagem Docker

Dentro da pasta python-app/:

-------------------------------------------------------------------------------------------------

📌 Passo 4: Documentação no README.md
O README.md deve conter:

Arquitetura (tree layout + desenho opcional).

Instalação do Minikube e criação do cluster.

Deploy do Argo CD e acesso via URL.

Deploy da aplicação Python com upload de imagens.

Configuração de Ingress para acessar URLs locais.

Futuro: integração com banco de dados (Postgres).

Comandos úteis (kubectl get pods, kubectl logs, etc.).

```
👉 Sugestão: no seu repositório GitHub (https://github.com/orbite82/k8s-argo-cd), crie branches separados para hml e prod, e vincule-os ao Argo CD. Assim você terá um fluxo GitOps real.

📌 Passo a Passo – Aplicação Python
1. Build da imagem Docker
Dentro da pasta python-app/:

bash
# Entre na pasta
cd python-app

# Build da imagem
docker build -t python-app:latest .
Isso cria a imagem python-app:latest usando o Dockerfile.

2. Carregar a imagem no Minikube
Como o Minikube roda em um ambiente isolado, você precisa carregar a imagem nele:

bash
minikube image load python-app:latest
3. Aplicar os manifests no Kubernetes
Agora vamos aplicar os YAMLs da aplicação:

bash
kubectl apply -f deployment.yaml -n hml
kubectl apply -f service.yaml -n hml
kubectl apply -f ingress.yaml -n hml
Aqui estamos usando o namespace hml. Se quiser rodar em prod, basta trocar -n prod.

4. Verificar se os pods estão rodando
bash
kubectl get pods -n hml
Você deve ver algo como:

Código
python-app-xxxx   Running
5. Verificar o service
bash
kubectl get svc -n hml
6. Ingress e acesso via URL
Confirme que o ingress controller (NGINX) está rodando:

bash
kubectl get pods -n ingress-nginx
Adicione no seu /etc/hosts:

Código
127.0.0.1 app.local
Acesse no navegador:

Código
http://app.local

-------------------------------------------------------------------------------------------------

# Em caso de Erro para acessar app.local

🔧 Passo a Passo para acessar a aplicação via URL
1. Verifique se o Ingress Controller está instalado
Se você não instalou o NGINX ingress controller, rode:

bash
minikube addons enable ingress
Isso cria os pods do NGINX ingress controller no namespace ingress-nginx.

2. Confirme que os pods do ingress estão rodando
bash
kubectl get pods -n ingress-nginx
Você deve ver algo como:

Código
nginx-ingress-controller-xxxx   Running

3. Descubra o IP do Minikube
bash
minikube ip
Exemplo de saída:

Código
192.168.49.2
Esse é o IP que o ingress vai usar.

4. Configure o /etc/hosts
Edite o arquivo /etc/hosts e adicione:

Código
192.168.49.2 app.local
192.168.49.2 argocd.local
Substitua 192.168.49.2 pelo IP que você obteve no comando minikube ip.

5. Teste o acesso
Agora abra no navegador:

Código
http://app.local
Se o ingress e o service estiverem corretos, você verá sua aplicação Flask.

🔧 Como corrigir
1. Alterar o Service da aplicação para LoadBalancer
Edite o arquivo python-app/service.yaml e troque o tipo:

yaml
apiVersion: v1
kind: Service
metadata:
  name: python-app-service
  namespace: hml
spec:
  selector:
    app: python-app
  ports:
    - protocol: TCP
      port: 5000
      targetPort: 5000
  type: LoadBalancer   # <<<<< altere aqui
Depois aplique novamente:

bash
kubectl apply -f python-app/service.yaml -n hml
2. Verifique se o túnel reconhece o serviço
Com o minikube tunnel rodando em um terminal, abra outro e rode:

bash
kubectl get svc -n hml
Agora você deve ver algo como:

Código
python-app-service   LoadBalancer   10.96.x.x   192.168.58.2   5000:xxxxx/TCP   2m
Note que aparece um EXTERNAL-IP (192.168.58.2).

3. Ajuste o /etc/hosts
Adicione:

Código
192.168.58.2 app.local
4. Teste no navegador
Abra:

Código
http://app.local
✅ Alternativa sem LoadBalancer
Se preferir manter o Service como ClusterIP, você pode acessar via ingress normalmente, mas precisa garantir que o ingress controller está resolvendo o host app.local para o IP do Minikube. Nesse caso, o passo crítico é mapear o IP do Minikube no /etc/hosts.

👉 Resumindo:

Se usar ClusterIP, precisa do ingress + /etc/hosts.

Se usar LoadBalancer, precisa do minikube tunnel + /etc/hosts.


-------------------------------------------------------------------------------------------------

📌 Passo 3.1 – Configuração do Argo CD com Cluster e GitHub

4. Criar o manifesto de aplicação do Argo CD
No arquivo argocd/hml-prod-apps.yaml:

yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: python-app-hml
  namespace: argocd
spec:
  project: default
  source:
    repoURL: 'https://github.com/orbite82/k8s-argo-cd.git'
    targetRevision: main
    path: python-app
  destination:
    server: 'https://kubernetes.default.svc'
    namespace: hml
  syncPolicy:
    automated:
      prune: true
      selfHeal: true

---
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: python-app-prod
  namespace: argocd
spec:
  project: default
  source:
    repoURL: 'https://github.com/orbite82/k8s-argo-cd.git'
    targetRevision: main
    path: python-app
  destination:
    server: 'https://kubernetes.default.svc'
    namespace: prod
  syncPolicy:
    automated:
      prune: true
      selfHeal: true

=================================================================================================

📌 Estrutura recomendada no GitHub
No seu repositório https://github.com/orbite82/k8s-argo-cd, crie duas branches:

hml → ambiente de homologação

prod → ambiente de produção

Cada branch terá os mesmos diretórios (cluster/, python-app/, argocd/), mas com configurações específicas se necessário.

📌 Passo a passo para criar branches
Crie a branch hml a partir da main:

bash
git checkout main
git checkout -b hml
git push origin hml
Crie a branch prod:

bash
git checkout main
git checkout -b prod
git push origin prod
Agora você terá três branches no GitHub: main, hml, prod.


📌 Ajuste do manifesto Argo CD
No arquivo argocd/hml-prod-apps.yaml, configure cada aplicação para apontar para o branch correto:

apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: python-app-hml
  namespace: argocd
spec:
  project: default
  source:
    repoURL: 'https://github.com/orbite82/k8s-argo-cd.git'
    targetRevision: main
    path: python-app
  destination:
    server: 'https://kubernetes.default.svc'
    namespace: hml
  syncPolicy:
    automated:
      prune: true
      selfHeal: true

---
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: python-app-prod
  namespace: argocd
spec:
  project: default
  source:
    repoURL: 'https://github.com/orbite82/k8s-argo-cd.git'
    targetRevision: prod
    path: python-app
  destination:
    server: 'https://kubernetes.default.svc'
    namespace: prod
  syncPolicy:
    automated:
      prune: true
      selfHeal: true

---
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: python-app-prod
  namespace: argocd
spec:
  project: default
  source:
    repoURL: 'https://github.com/orbite82/k8s-argo-cd.git'
    targetRevision: prod   # <<<<< branch PROD
    path: python-app
  destination:
    server: 'https://kubernetes.default.svc'
    namespace: prod
  syncPolicy:
    automated:
      prune: true
      selfHeal: true

Aplique:

bash
kubectl apply -f argocd/prod-apps.yaml


📌 Fluxo de trabalho com branches
Homologação (HML)  
Você faz commits e push na branch hml. O Argo CD sincroniza automaticamente no namespace hml.

Produção (PROD)  
Quando a versão estiver validada, você faz merge da hml para prod. O Argo CD sincroniza no namespace prod.
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