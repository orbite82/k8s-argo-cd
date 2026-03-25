🔥 0. LIMPEZA TOTAL
👉 Deleta cluster kind
kind delete cluster
👉 (Opcional) limpar imagens locais
docker system prune -af
🚀 1. Criar cluster kind

Se você já tem config, usa ela. Senão:

kind create cluster --name argocd-lab

Confirma:

kubectl get nodes
📦 2. Criar namespace do Argo CD
kubectl create namespace argocd
⚠️ 3. Instalar Argo CD (forma correta)

IMPORTANTE: usar server-side (evita erro de CRD)

kubectl apply -n argocd \
  -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml \
  --server-side
⏳ 4. Aguardar subir tudo
kubectl get pods -n argocd -w

Só segue quando tudo estiver:

Running
🌐 5. Acessar Argo CD
kubectl port-forward svc/argocd-server -n argocd 8080:443

Abre:

https://localhost:8080
🔐 6. Login

Usuário:

admin

Senha:

kubectl -n argocd get secret argocd-initial-admin-secret \
  -o jsonpath="{.data.password}" | base64 -d

🔗 7. Conectar seu GitHub

Repo:

https://github.com/orbite82/k8s-argo-cd

No Argo CD:

Settings → Repositories → Add
📦 8. Criar Application
Preenche assim:

General

Name: image-app
Project: default

Source

Repo URL: https://github.com/orbite82/k8s-argo-cd
Revision: HEAD
Path: apps/image-app   ← (ajustar se necessário)

Destination

Cluster: https://kubernetes.default.svc
Namespace: default

👉 Marca:

✅ Auto Sync
✅ Self Heal
🚀 9. Deploy
Clique em Create
Depois Sync (se não automático)
🔍 10. Validar aplicação
kubectl get pods
kubectl get svc
🌍 11. Expor aplicação
👉 Forma simples (NodePort)
kubectl get svc

Procura algo assim:

30007

Acessa:

http://localhost:30007
✅ CHECK FINAL

Se tudo deu certo você terá:

✔ Cluster rodando
✔ Argo CD funcionando
✔ App sincronizado
✔ Pods do frontend/backend/DB rodando
✔ Acesso via browser