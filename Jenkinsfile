#!/usr/bin/env groovy

// Link this build with Gitlab
properties([gitLabConnection('gitlab')])

// Include custom utilities
@Library('jenkins-utils@master') _

pipeline{
  agent any

  stages {

    stage('Clean workspace') {
      steps {
        sh("""
          rm -rf env
          python3.6 -m venv env
          """)
        } //steps
    } // stage: Clean workspace

    stage('Run unit tests') {
      steps {
      	sh("""
          . env/bin/activate
          export PYTHONPATH="`pwd`"
          pip3.6 install -r requirements.txt
          python3.6 setup.py test
          """)
        } // steps
        post {
          always {
            junit 'reports/*.xml'
          } // always
        } // post
    } // stage: Run unit tests

    stage('Build and deploy') {
      steps {
        sh("rm -rf build/ dist/")
        grxUploadPipLibrary() {
          sh("""
            . env/bin/activate
            pip3.6 install "twin-sister>=1.1.0.0"
            pip3.6 install -r requirements.txt
            python3.6 setup.py bdist_wheel
            twine upload -r nexus-internal-repo `ls dist/*.whl | head -n1`
            """
            )
          } // grxUploadPipLibrary
        } // steps
      } // stage: build and deploy
  } // stages
} // pipeline
