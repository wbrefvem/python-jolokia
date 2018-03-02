pipeline {
  agent {
    node {
      label 'python'
    }
    
  }
  stages {
    stage('Test') {
      steps {
        pwd()
        sh 'ls -al'
        sh './run_tests.sh'
      }
    }
    stage('Deploy') {
      steps {
        echo 'Deploying'
      }
    }
  }
}