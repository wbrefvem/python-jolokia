pipeline {
  agent any
  stages {
    stage('Test') {
      agent {
        node {
          label 'py3'
        }
        
      }
      steps {
        sh '''echo $PATH
python --version'''
        pwd()
        sh 'ls -al'
        sh './run_tests'
      }
    }
    stage('Deploy') {
      steps {
        echo 'Deploying'
      }
    }
  }
}