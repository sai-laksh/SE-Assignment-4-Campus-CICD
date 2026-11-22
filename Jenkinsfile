
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
                bat '''"C:\\Users\\anand\\AppData\\Local\\Programs\\Python\\Python39\\python.exe" -m unittest discover -s tests -v'''
            }
        }

        stage('Build Docker Image') {
            steps {
                bat '''"C:\\Users\\anand\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin\\docker.exe" build -t campus-welcome:%BUILD_NUMBER% .'''
            }
        }

        stage('Deploy Website') {
            steps {
                bat(returnStatus: true, script: '''"C:\\Users\\anand\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin\\docker.exe" rm -f campus-welcome''')

                bat '''"C:\\Users\\anand\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin\\docker.exe" run -d --name campus-welcome -p 8081:80 campus-welcome:%BUILD_NUMBER%'''
            }
        }

        stage('Smoke Test') {
            steps {
                bat '''powershell -NoProfile -Command "Start-Sleep -Seconds 3; Invoke-WebRequest http://localhost:8081 -UseBasicParsing"'''
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
