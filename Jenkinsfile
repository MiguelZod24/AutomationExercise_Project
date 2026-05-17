pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                echo 'Clonando repositorio desde GitHub'
                checkout scm
            }
        }

        stage('Instalar Python y dependencias') {
            steps {
                echo 'Instalando Python y dependencias'
                sh '''
                    apt-get update -q
                    apt-get install -y python3 python3-pip
                    pip3 install -r requirements.txt --break-system-packages
                '''
            }
        }

        stage('Ejecutar tests') {
            steps {
                echo 'Ejecutando tests con Pytest'
                sh 'pytest --tb=short'
            }
        }

    }
}

    

