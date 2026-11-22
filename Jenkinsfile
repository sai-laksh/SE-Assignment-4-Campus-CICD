
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
                bat '"C:\\Users\\anand\\AppData\\Local\\Programs\\Python\\Python39\\python.exe" -m unittest discover -s tests -v'
            }
        }

        stage('Build Docker Image') {
            steps {
                bat '"C:\\Users\\anand\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin\\docker.exe" build -t campus-welcome:%BUILD_NUMBER% .
            }
        }

        stage('Deploy Website') {
            steps {
                bat '"C:\\Users\\anand\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin\\docker.exe" rm -f campus-welcome || exit /b 0'
                bat '"C:\\Users\\anand\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin\\docker.exe" run -d --name campus-welcome -p 8081:80 campus-welcome:%BUILD_NUMBER%'
            }
        }

        stage('Smoke Test') {
            steps {
                 bat 'powershell -NoProfile -Command "$ok = $false; for ($i = 0; $i -lt 10; $i++) { try { Invoke-WebRequest http://localhost:8081 -UseBasicParsing -TimeoutSec 3; $ok = $true; break } catch { Start-Sleep -Seconds 2 } }; if (-not $ok) { throw \'Website smoke test failed\' }"'
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
