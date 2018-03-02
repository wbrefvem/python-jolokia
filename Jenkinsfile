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
        container('python') {
          sh 'echo $PATH'
          sh 'python --version'
          pwd()
          sh 'ls -al'
          sh './run_tests'          
        }

      }
    }
    stage('Deploy') {
      steps {
        echo 'Deploying'
      }
    }
  }
}