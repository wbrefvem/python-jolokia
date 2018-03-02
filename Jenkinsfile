pipeline {
  agent {
    node {
      label 'python'
    }
    
  }
  stages {
    stage('Test') {
      steps {
        sh './run_tests.sh'
        pwd()
      }
    }
    stage('Deploy') {
      steps {
        echo 'Deploying'
      }
    }
  }
}