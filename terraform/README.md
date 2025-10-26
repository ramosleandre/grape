## Infrastructure as Code (GCP) — Story 5.1

Ce dossier contient la configuration Terraform pour provisionner l'infrastructure GCP nécessaire aux environnements `dev`, `staging` et `prod` pour le projet Grape.

But
- Fournir les ressources GCP nécessaires pour exécuter le backend (Cloud Run), le frontend (Firebase Hosting), un dépôt d'artefacts (Artifact Registry), Vertex AI, Secret Manager, IAM et le réseau.
- Respecter le principe du moindre privilège et ne pas stocker de secrets en clair.

Structure
```
infrastructure/terraform/
├── README.md
├── backend.tf
├── providers.tf
├── variables.tf
├── main.tf
├── outputs.tf
├── iam.tf
├── networking.tf
├── secretmanager.tf
├── cloudrun.tf
├── firebase.tf
├── artifact_registry.tf
├── vertexai.tf
├── database.tf
├── dev/terraform.tfvars
├── staging/terraform.tfvars
└── prod/terraform.tfvars
```

Pré-requis
- Installer `terraform` (>= 1.1 recommandé).
- Installer et configurer `gcloud` et s'authentifier (ex: `gcloud auth application-default login` ou `gcloud auth login`).

Initialisation
1. Choisir un environnement (`dev`, `staging`, `prod`).
2. Placer/éditer le fichier `*-terraform.tfvars` dans le répertoire racine (les exemples existent déjà dans chaque dossier env).
3. Initialiser Terraform en fournissant la configuration du backend GCS (le backend n'est pas fixé dans le code; cf. plus bas) :

Exemple :
```bash
# Depuis infrastructure/terraform/
terraform init -backend-config="bucket=grape-terraform-state-<YOUR_BUCKET>" -backend-config="prefix=${env}/terraform.tfstate"
terraform plan -var-file=dev/terraform.tfvars
terraform apply -var-file=dev/terraform.tfvars
```

Remarques importantes
- Aucuns secrets en clair dans les fichiers `.tf` ou `.tfvars`. Les ressources `google_secret_manager_secret` sont créées mais les versions (valeurs) doivent être ajoutées via `gcloud` ou un flux sécurisé après `apply`. Voir la section "Gestion des secrets" ci-dessous.
- Le backend GCS pour l'état distant doit être fourni via `-backend-config` au moment du `terraform init` (le bloc backend contient des exemples commentés).

Gestion des secrets
- Après `terraform apply`, créez les versions de secrets (valeurs réelles) en local ou via CI sécurisé :

```bash
gcloud secrets versions add projects/PROJECT_ID/secrets/graphdb_password --data-file=<(echo -n "<SECRET_VALUE>")
```

Décisions/limitations
- Neo4j Aura ou autres services GraphDB managés peuvent ne pas avoir de provider Terraform officiel couvrant tout. Le fichier `database.tf` fournit un placeholder et instructions pour intégrer Neo4j Aura manuellement en stockant les credentials dans Secret Manager.
- Firebase Hosting peut nécessiter quelques étapes manuelles (associer site, config CLI) — des instructions sont fournies plus bas.

Checklist de validation post-apply
- Cloud Run : un service existe et l'output `cloud_run_url` est présent.
- Artifact Registry : repository Docker créé.
- Secrets : ressources créées dans Secret Manager (sans versions) et SA backend a accès.
- APIs activées (liste dans `main.tf`).

Si vous avez besoin d'ajustements (par ex. backend GCS centralisé automatisé), je peux le faire ensuite mais la présente livraison se concentre uniquement sur la Story 5.1.

---
## Étapes manuelles restantes (résumé)
- Ajouter les versions (valeurs) des secrets via `gcloud secrets versions add` ou via votre secret management sécurisé.
- Si vous utilisez Neo4j Aura ou un service managé privé, suivez les instructions de `database.tf` pour le peering ou la configuration réseau; la création manuelle du service peut être nécessaire.
- Pour Firebase Hosting, finaliser la configuration via `firebase` CLI si nécessaire (documenté ci-dessous).
