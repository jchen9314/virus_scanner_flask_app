pipeline {
    agent any
    stages {
        stage('Get Source') {
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
        stage('Build Docker Image') {
            steps {
                // sh 'docker build -t ft-flask:latest .'
                script {
                    def dockerImage = docker.build("jc2592/virus-scanner-flask:${env.BUILD_TAG}")
                }
            }
        }
        // stage('Run docker image') {
        //     steps {
        //         sh 'docker run -d -p 5000:5000 --name flask-container ft-flask'
        //     }
        // }
        stage('Push Docker Image'){
            steps {
                script {
                    docker.withRegistry('', 'dockerhub') {
                        dockerImage.push()
                        dockerImage.push('latest')
                    }
                }
            }
        }
    }
}