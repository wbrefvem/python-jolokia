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
          git url: 'https://github.com/wbrefvem/python-jolokia.git' branch: 'pipeline'
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