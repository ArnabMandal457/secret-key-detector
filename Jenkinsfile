pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                echo 'Cloning repository...'
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                echo 'Checking Python...'
                sh 'python3 --version'
            }
        }

        stage('Run Secret Scan') {
            steps {
                echo 'Scanning for secrets...'
                sh 'mkdir -p reports'
                sh 'python3 scripts/scan.py . > reports/scan_results.json'
            }
        }

        stage('Generate Report') {
            steps {
                echo 'Generating HTML report...'
                sh 'python3 scripts/generate_report.py reports/scan_results.json reports/report.html'
            }
        }

        stage('Deploy Report') {
            steps {
                echo 'Deploying report...'
                sh 'cp reports/report.html /var/www/html/report.html'
            }
        }
        
        stage('Archive to S3') {
            steps {
                echo 'Archiving report to S3...'
                sh '/home/ubuntu/.local/bin/aws s3 cp reports/report.html s3://secret-key-detector-reports-092040680611-ap-south-1-an/report-$(date +%Y%m%d-%H%M%S).html'
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed. Report deployed.'
        }
        failure {
            echo 'Pipeline failed. Check logs.'
        }
    }
}