pipeline {
    agent any

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
                sh 'venv/bin/python3 ./keta/manage.py test'
            }
        }
        stage('Deploy') {
            steps {
                sh 'docker-compose build'
                sh 'docker tag keta-app:latest carlosharo/keta-app:latest'
                sh 'docker login -u carlosharo -p C@r1oS+2023='
                sh 'docker push carlosharo/keta-app:latest'
            }
        }
    }

    post {
        always {
            echo 'The process was a success'
        }
    }
}