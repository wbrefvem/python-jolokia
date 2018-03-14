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
          sh 'rm -rf ./ci/codeship/docker'
          sh './ci/codeship/render_dockerfiles'
          sh './ci/codeship/render_services'
          sh './ci/codeship/render_steps'
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