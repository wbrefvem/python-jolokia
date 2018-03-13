pipeline {
  agent none
  stages {
    stage('Test') {
      agent {
        docker {
          image 'python:3.6.4'
        }
      }
      steps {
        git url: 'https://github.com/wbrefvem/python-jolokia.git', branch: 'docker'
        sh 'pip install pipenv --upgrade'
        sh 'pipenv lock'
        sh 'pipenv install --dev --system'
        sh 'pytest -v --junit-xml test-reports/results.xml'
        junit 'test-reports/results.xml'
      }
    }
    stage('Deploy') {
      steps {
        echo 'Deploying'
      }
    }
  }
}