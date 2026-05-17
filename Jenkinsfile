pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                echo 'Clonando repositorio desde GitHub'
                checkout scm
            }
        }

        stage('Instalar dependencias') {
            steps {
                echo 'Instalando dependencias de Python'
                sh 'pip install -r requirements.txt'
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
