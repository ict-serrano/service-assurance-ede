pipeline {
    environment {
        PROJECT_NAME = 'service-assurance-ede'
        DEPLOY = "${env.GIT_BRANCH == "origin/master" || env.GIT_BRANCH == "origin/develop" ? "true" : "false"}"
        DEPLOY_UVT = "${env.GIT_BRANCH == "origin/master" ? "true" : "false"}"
        CHART_NAME = "${env.GIT_BRANCH == "origin/master" ? "service-assurance-ede" : "service-assurance-ede-staging"}"
        VERSION = '0.0.15'
        DOMAIN = 'localhost'
        REGISTRY = 'serrano-harbor.rid-intrasoft.eu/serrano/service-assurance-ede'
        REGISTRY_URL = 'https://serrano-harbor.rid-intrasoft.eu/serrano'
        REGISTRY_CREDENTIAL = 'harbor-jenkins'
        UVT_KUBERNETES_PUBLIC_ADDRESS = 'api.k8s.cloud.ict-serrano.eu'
        INTEGRATION_OPERATOR_TOKEN = credentials('uvt-integration-operator-token')
    }
    agent {
        kubernetes {
            cloud 'kubernetes'
            defaultContainer 'jnlp'
            yamlFile 'build.yaml'
        }
    }
    stages {
        stage('Install requirements') {
            steps {
                container('python') {
                    sh '/usr/bin/apt -y update && /usr/bin/apt -y install gcc && /usr/bin/apt clean'
                    sh '/usr/local/bin/python -m pip install --upgrade pip'
                    sh 'pip install --no-cache-dir -r requirements_service.txt'
                    sh 'pip install --no-input cyclonedx-bom'
                    sh "openssl s_client -connect ${UVT_KUBERNETES_PUBLIC_ADDRESS}:6443 2>/dev/null </dev/null |  sed -ne '/-BEGIN CERTIFICATE-/,/-END CERTIFICATE-/p' > uvt.cer"
                }
            }
        }
        stage('Sonarqube') {
            environment {
                scannerHome = tool 'SonarQubeScanner'
            }
            steps {
                container('java') {
                    withSonarQubeEnv('sonarqube') {
                        sh "${scannerHome}/bin/sonar-scanner -Dsonar.projectKey=${PROJECT_NAME}"
                    }
                    timeout(time: 10, unit: 'MINUTES') {
                        waitForQualityGate abortPipeline: true
                    }
                }
            }
        }
        stage('Generate BOM') {
            steps {
                container('python') {
                    sh 'cyclonedx-bom -e -F -o ./bom.xml'
                }
            }
        }
        stage('Dependency Track') {
            steps {
                container('python') {
                    dependencyTrackPublisher artifact: 'bom.xml', projectId: '7727e147-419b-4283-af49-c1ef40e5e712', synchronous: true
                }
            }
        }
        stage('Docker Build') {
            when {
                environment name: 'DEPLOY', value: 'true'
            }
            steps {
                container('docker') {
                    sh "docker build -t ${REGISTRY}:${VERSION} ."
                }
            }
        }
        stage('Docker Publish') {
            when {
                environment name: 'DEPLOY', value: 'true'
            }
            steps {
                container('docker') {
                    withDockerRegistry([credentialsId: "${REGISTRY_CREDENTIAL}", url: "${REGISTRY_URL}"]) {
                        sh "docker push ${REGISTRY}:${VERSION}"
                    }
                }
            }
        }
        stage('Deploy Service-Assurance-EDE in INTRA Kubernetes') {
            when {
                environment name: 'DEPLOY', value: 'true'
            }
            steps {
                container('helm') {
                    //sh "helm uninstall --wait --timeout 600s --namespace integration ${CHART_NAME}-integration"
                    sh "helm upgrade --install --force  --wait --timeout 600s --namespace integration --set service.port=5551 --set image.tag=${VERSION} ${CHART_NAME}-integration ./helm"
                }
            }
        }
        stage('Integration Tests') {
            when {
                environment name: 'DEPLOY', value: 'true'
            }
            steps {
                container('java') {
                    script {
                        echo 'Run your Integration Tests here'
                        //sleep 20 // Sleep is not required if the readiness probe is enabled
                        try {
                            String testName = "1. Check that app is running - 200 response code"
                            String url = "http://${CHART_NAME}-integration-${PROJECT_NAME}.integration:5551/ping"
                            String responseCode = sh(label: testName, script: "curl -m 10 -sLI -w '%{http_code}' $url -o /dev/null", returnStdout: true)

                            if (responseCode != '200') {
                                error("$testName: Returned status code = $responseCode when calling $url")
                            }

                            testName = '2. Validate greeting response without request parameters'
                            url = "http://${CHART_NAME}-integration-${PROJECT_NAME}.integration:5551/ping"
                            String responseBody = sh(label: testName, script: "curl -m 10 -sL $url", returnStdout: true)

                            if (responseBody != '{"ok":true,"message":"I am alive"}') {
                                error("$testName: Unexpected response body = $responseBody when calling $url")
                            }
                        } catch (ignored) {
                            currentBuild.result = 'FAILURE'
                            echo "Integration Tests failed"
                        }
                    }
                }
            }
        }
        stage('Cleanup Deployment') {
            when {
                environment name: 'DEPLOY', value: 'true'
            }
            steps {
                container('helm') {
                    sh "helm uninstall ${CHART_NAME}-integration --namespace integration"
                }
            }
        }
        stage('Deploy in UVT Kubernetes') {
            when {
                environment name: 'DEPLOY_UVT', value: 'true'
            }
            steps {
                container('helm') {
                    sh "kubectl config set-cluster kubernetes-uvt --certificate-authority=uvt.cer --embed-certs=true --server=https://${UVT_KUBERNETES_PUBLIC_ADDRESS}:6443"
                    sh "kubectl config set-credentials integration-operator --token=${INTEGRATION_OPERATOR_TOKEN}"
                    sh "kubectl config set-context kubernetes-uvt --cluster=kubernetes-uvt --user=integration-operator"
                    sh 'sed -i "s/__docker__image__tag__/${VERSION}/" ./helm/values-uvt-serrano.yaml'
                    sh "helm upgrade --install --force --wait --timeout 600s --kube-context=kubernetes-uvt --namespace integration ${CHART_NAME} -f ./helm/values-uvt-serrano.yaml ./helm"
                }
            }
        }
    }
}