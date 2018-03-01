pipeline {
  agent any
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