
pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                echo 'Checking project source'
                checkout scm
            }
        }

        stage('Automated Tests') {
            steps {
                bat 'py -m unittest discover -s tests -v'
            }
        }

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t campus-welcome:%BUILD_NUMBER% .'
            }
        }

        stage('Deploy Website') {
            steps {
                bat 'docker rm -f campus-welcome || exit /b 0'
                bat 'docker run -d --name campus-welcome -p 8081:80 campus-welcome:%BUILD_NUMBER%'
            }
        }

        stage('Smoke Test') {
            steps {
                bat 'powershell -NoProfile -Command "Invoke-WebRequest http://localhost:8081 -UseBasicParsing"'
            }
        }
    }

    post {
        success {
            echo 'Website deployed successfully!'
        }

        failure {
            echo 'Pipeline failed. Check the stage logs.'
        }
    }
}
