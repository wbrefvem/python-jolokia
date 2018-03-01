pipeline {
  agent {
    node {
      label 'pytest'
    }
    
  }
  stages {
    stage('Test') {
      steps {
        sh '''pipenv install
pipenv shell
pytest -v'''
      }
    }
    stage('Deploy') {
      steps {
        echo 'Deploying'
      }
    }
  }
}