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