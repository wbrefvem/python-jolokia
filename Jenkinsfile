pipeline {
  agent {
    node {
      label 'py3'
    } 
  }  
  stages {
    stage('Render Codeship deps') {
      steps {
        container('python') {
          sh 'pip install pipenv'
          sh 'pipenv lock'
          sh 'pipenv install --dev --system --deploy'
          dir([path: './ci/codeship']) {
            sh 'rm -rf docker'
            sh './render_dockerfiles'
            sh './render_services'
            sh './render_steps'            
          }
        }
      }
    }
    stage('Notifying Codeship') {
      steps {
        echo 'Triggering codeship build'
      }
    }
  }
}