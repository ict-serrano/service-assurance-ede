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
        UVT_K8S_CA = 'LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSUMvakNDQWVhZ0F3SUJBZ0lCQURBTkJna3Foa2lHOXcwQkFRc0ZBREFWTVJNd0VRWURWUVFERXdwcmRXSmwKY201bGRHVnpNQjRYRFRJeU1EY3lOVEUyTURZd09Wb1hEVE15TURjeU1qRTJNRFl3T1Zvd0ZURVRNQkVHQTFVRQpBeE1LYTNWaVpYSnVaWFJsY3pDQ0FTSXdEUVlKS29aSWh2Y05BUUVCQlFBRGdnRVBBRENDQVFvQ2dnRUJBTTA4CnZHQXNseU1kZDdPSXdJeC8yUk1XeTVyOVVHS0FnL0hWUk80bU5VYkx6K3dJTnZ4ZmNBa1p1blN2dG9hRWFoM28KRFlGbVQ5WTNaVmhSWEpicG5kb1RVTFg2eWV3aW1EMWU1N0NCQWQrcnMvc2hRU0U0VXJkdVYwUmJ0ck11NVJRTgp1K3lkbnpYVHlmVTZIeUVlTTRRQzRNZ1c2dTIvSGZ1Tmd4bVR2USsvZXY1MFY0T2VuY082VTQyMnVlTnZHaS80CnJpcE9vTmxFWnZuWFFORG1tOTA2aDFaR1EvYmQ4Q2swS0RNRWpnWDlEcmJrVGNPMC9uRnJ0YnhJcDhON202ZHYKd0xxR2pERHJoZWMra1hGb2o4bzlmSVdLdldNYzFyT3prRmh0TGxsMjRyc0Z1a0U1Unh5azBMdTFJTXVuRGJwVgpLMDdtQjI5b2xFZTlFK1VxSUM4Q0F3RUFBYU5aTUZjd0RnWURWUjBQQVFIL0JBUURBZ0trTUE4R0ExVWRFd0VCCi93UUZNQU1CQWY4d0hRWURWUjBPQkJZRUZLc25uSTNMZUxoQS9ESnRQeU52bXNlYTcrM0JNQlVHQTFVZEVRUU8KTUF5Q0NtdDFZbVZ5Ym1WMFpYTXdEUVlKS29aSWh2Y05BUUVMQlFBRGdnRUJBRmNLWStzWis1VVNQb0w5Um8xTApMdm1EdlQvd3ZtR1RtbVNRQWdoVFBFMFRoaU44M3VLSENRNUN3RE5YN3NYUzQzUmg1OUwyTC95Vm12dHNDL3NNCkN4YW90M1BzcFJBQ2xEa1JNN3d3VDRZRUg5VUdTcVlNMHJTbEdNTFVCNmhWM1h4VU5VT3pUZFJ0OVo4UTR1a2sKRTk2RlBqcmswWXl0K04rNFpCWXFhVkczdHhUNXZ5NC80YjE0WUs2eGo3cllTTktvTCs4V3c4eTB4d3FwSFJRbApwMmhvRnpMVndleDMvUmZPeWhCMCtwYm9Fb1pQNHhGL0t1MW9CcktobDF4MFgvTHB5UGNzcE9lMzE5eCttUm1CCklDSnBSRk10ZkVaQW1nN2R5SWN2Q3EwSEhJajk5TUR1Mm0zTWJDRmx4QUx6WjRuZWJaVDdEbTlFc2x6T29NaUMKNUxNPQotLS0tLUVORCBDRVJUSUZJQ0FURS0tLS0tCg=='
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
                            String url = "http://${CHART_NAME}-integration.integration:5551/ping"
                            String responseCode = sh(label: testName, script: "curl -m 10 -sLI -w '%{http_code}' $url -o /dev/null", returnStdout: true)

                            if (responseCode != '200') {
                                error("$testName: Returned status code = $responseCode when calling $url")
                            }

                            testName = '2. Validate greeting response without request parameters'
                            url = "http://${CHART_NAME}-integration.integration:5551/ping"
                            String responseBody = sh(label: testName, script: "curl -m 10 -sL $url | tr -d [:space:]", returnStdout: true)

                            if (responseBody != '{"ok":true,"message":"Iamalive"}') {
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
                    sh "echo -n $UVT_K8S_CA | base64 -d > uvt.cer"
                    sh "kubectl config set-cluster kubernetes-uvt --certificate-authority=uvt.cer --embed-certs=true --server=https://${UVT_KUBERNETES_PUBLIC_ADDRESS}:6443"
                    sh "kubectl config set-credentials integration-operator --token=${INTEGRATION_OPERATOR_TOKEN}"
                    sh "kubectl config set-context kubernetes-uvt --cluster=kubernetes-uvt --user=integration-operator"
                    sh 'sed -i "s/__docker__image__tag__/${VERSION}/" ./helm/values-uvt-serrano.yaml'
                    sh "helm upgrade --install --wait --timeout 600s --kube-context=kubernetes-uvt --namespace integration ${CHART_NAME} -f ./helm/values-uvt-serrano.yaml ./helm"
                }
            }
        }
    }
}