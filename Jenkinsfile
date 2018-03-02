pipeline {
  agent {
    node {
      label 'python'
    }
    
  }
  stages {
    stage('Test') {
      steps {
        sh '''set -ex
pip install pipenv --upgrade
pipenv install --dev --system --deploy
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