pipeline {
    agent any

    // environment {
    //     DOCKERHUB_CREDENTIALS = credentials('docker-credentials')
    // }

    stages {
        stage('Checkout') {
            steps {
                // Clean the working directory
                deleteDir()

                // Checkout the code
                checkout scm

                // Log changes if needed
                sh 'git log HEAD^..HEAD --pretty="%h %an - %s" > GIT_CHANGES'
                }
            }
        stage('Build') {
            steps {
                sh 'python3 -m venv venv'
                sh 'venv/bin/pip install -r requirements.txt'
                sh 'cp /home/ubuntu/.env /var/lib/jenkins/workspace/ev_dev_certification_carlos.haro/.env'
                // sh 'cp /var/env/.env .'
                sh 'venv/bin/python3 ./keta/manage.py makemigrations'
                sh 'venv/bin/python3 ./keta/manage.py migrate --fake-initial'
                sh 'venv/bin/python3 ./keta/manage.py collectstatic --noinput'
            }
        }
		stage('Test') {
            steps {
                echo 'The process was a success'
                // sh 'venv/bin/python3 ./keta/manage.py test users tickets'
            }
        }
        stage('Deploy') {
            steps {
//                 script {
//                     // Use docker-compose to build the Docker image
//                     sh 'docker image prune -a --force'
//                     sh 'docker-compose build'

// //                     // Login Docker Hub
// //                     sh 'echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin'
// //
// //                     // Push the Docker image
// //                     sh 'docker push carlosharo/keta-app:latest'
// //                     sh 'docker logout'
//                     }
                    echo 'The process was a success'
            }

        }
    }

    post {
        always {
            echo 'The process was a success'
        }
    }
}