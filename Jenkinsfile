pipeline {
    agent any

    environment {
        DOCKER_REGISTRY = 'https://registry.hub.docker.com'
        DOCKER_CREDENTIALS_ID = 'docker-credentials'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
                script {
                        sh 'git log HEAD^..HEAD --pretty="%h %an - %s" > GIT_CHANGES'
                    }
            }
        }
        stage('Build') {
            steps {
                sh 'python3 -m venv venv'
                sh 'venv/bin/pip install -r requirements.txt'
                sh 'cp /var/env/.env .'
                sh 'venv/bin/python3 ./keta/manage.py makemigrations'
                sh 'venv/bin/python3 ./keta/manage.py migrate --fake-initial'
                sh 'venv/bin/python3 ./keta/manage.py collectstatic --noinput'
            }
        }
		stage('Test') {
            steps {
                sh 'venv/bin/python3 ./keta/manage.py test users tickets'
            }
        }
        stage('Deploy') {
            steps {
                script {
                    // Authenticate with the Docker registry using Docker Plugin credentials
                    docker.withRegistry(env.DOCKER_REGISTRY, env.DOCKER_CREDENTIALS_ID) {
                    // Use docker-compose to build the Docker image
                    sh 'docker-compose build'

                    // Optionally, tag the image
                    sh 'docker tag keta-app:latest carlosharo/keta-app:latest'

                    // Push the Docker image
                    sh 'docker push carlosharo/keta-app:latest'
                    }
            }
        }
    }

    post {
        always {
            echo 'The process was a success'
        }
    }
}