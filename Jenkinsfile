pipeline {
  agent none
  stages {
    stage('Test') {
      agent {
        node {
          label 'py3'
        } 
      }
      steps {
        container('python') {
          git url: 'https://github.com/wbrefvem/python-jolokia.git', branch: 'pipeline'
          sh 'pip install pipenv'
          sh 'pipenv lock'
          sh 'pipenv install --dev --system --deploy'
          sh 'pytest -v --junit-xml test-reports/results.xml'            
          junit 'test-reports/results.xml'
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