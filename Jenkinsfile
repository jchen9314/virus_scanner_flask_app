pipeline {
    agent any
    stages {
        stage('Get source') {
            // copy source code from local file system and test
            // for a Dockerfile to build the Docker image
            steps {
                git ('https://github.com/jchen9314/virus_scanner_flask_app.git')
                script {
                    if (!fileExists("Dockerfile")) {
                        error('Dockerfile missing.')
                    }
                }
            }
        }
        stage('Build docker image') {
            steps {
                sh 'docker build -t ft-flask:${env.BUILD_TAG} .'
            }
        }
        stage('Run docker image') {
            steps {
                sh 'docker run -d -p 5000:5000 --name flask-container ft-flask'
            }
        }
    }
}