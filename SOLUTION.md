# Solution

## What Has Been Done
1. The Python code has been modified:
    1.1. Readiness and liveness probe endpoints have been added.  
    1.2. The `/download_external_logs` endpoint has been added to the backend API. This API interacts with the `data_api` and returns a value. It also accepts an integration key, but it does not use it anywhere.  
    1.3. The `requirements.txt` file has been cleaned of unnecessary dependencies to reduce the image size.  
2. A Helm chart has been created in the `.helm` directory. It is a simple Helm chart with two sets of default values for the `dev` and `prod` environments.  
3. Two simple Ansible roles (docker & helm) have been created and stored in the `roles` directory.  
4. A simple script, `deploy.sh`, has been created to emulate the deployment pipeline.  
5. Dockerfiles have been created.  
6. The `healthcheck.sh` script has been modified.

## How to Run

### Prerequisites
1. You need to install a Minikube cluster (it should also work on EKS/AKS with the NGINX ingress controller) with the metrics and ingress addons.  
2. Run a port-forward to be able to communicate with the API exposed via ingress:
    ```zsh
    kubectl port-forward -n kube-system service/ingress-nginx-controller 8080:80 -n ingress-nginx
    ```
3. Add a record to the `/etc/hosts` file with a fake FQDN (e.g., `127.0.0.1 api.abnamro.test`).  
4. You need to be authorized against the container registry to push publicly available Docker images.  
5. Ansible must be installed.  
6. Your `~/.kube/config` must be configured, and the proper context should be selected.

### Deploying
**Simply run the `deploy.sh` script with the following parameters:**  
1. `repo` - Docker Hub repo name (e.g., `cardiffc`).  
2. `image_tag` - Tag of the new image.  
3. `project_name` - Name of the project.  
4. `env` - Name of the environment (`dev` or `prod`).

    Example:
    ```zsh
    ./deploy.sh cardiffc 1 abn-test dev
    ```

**It will:**  
1. Build and push Docker images using the provided repo name and tag.  
2. Render the Helm chart.  
3. Install the Helm chart to the Kubernetes cluster in a namespace named after the project, using the previously built Docker images for the provided environment.

### How to Test
1. Run the `curl` command against the backend API (change the FQDN if needed):
    ```zsh
    curl http://api.abnamro.test:8080/download_external_logs
    ```
2. Run the `health_check.sh` script (change the FQDN if needed).

### Monitoring
1. To monitor pods based on labels, ensure that `kube-prometheus-state-metrics` is configured to push labels. This can be done by adding the argument `--metric-labels-allowlist=pods=[*]` to its deployment.  
2. PROMQL query to get CPU usage for pods based on label:
    ```promQL
    sum(rate(container_cpu_usage_seconds_total{namespace="namespace_name"}[1m])) by (pod) * on(pod) group_left(app) kube_pod_labels{namespace="namespace_name", label_k8s_app="kube-Devops"}
    ```
3. PROMQL query to get memory usage for pods based on label:
    ```promQL
    sum(rate(container_memory_usage_bytes{namespace="namespace_name"}[1m])) by (pod) * on(pod) group_left(app) kube_pod_labels{namespace="namespace_name", label_k8s_app="kube-Devops"}
    ```

### What Could Have Been Done Better
1. For this test task, I have created secrets for the backend API service with values and committed them to Git. The secret that will be created depends on the environment. In a real-world scenario, I would use an external secrets storage (like AWS SSM or HashiCorp Vault) and a Kubernetes operator to sync them.  
2. For this test task, I am using HTTP instead of HTTPS for the exposed services. In a real-world scenario, it should be HTTPS.  
3. The Helm chart could be further tuned to allow for Service Accounts, ImagePullSecrets, NetworkPolicies (if needed), and so on.  
4. The `deploy.sh` script should be replaced with a proper CI/CD pipeline.  
5. As I hadn't used Ansible for a while, I created simple roles, but it can be much more complex and flexible with more parameterization.
