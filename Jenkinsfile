pipeline {
  agent {
    node {
      label 'python'
    }
    
  }
  stages {
    stage('Test') {
      steps {
        sh '''sudo pip install pipenv
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