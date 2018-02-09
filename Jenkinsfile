#!/usr/bin/env groovy

// Link this build with Gitlab
properties([gitLabConnection('gitlab')])

// Include custom utilities
@Library('jenkins-utils@master') _

node {
  def module = "younger_twin_sister"

  //Checkout source code before we tie this pipeline to GitLab
  checkout scm

  grxBuild(['Build Prep', 'Run Unit Tests', 'Build Library']) {

    grxStage('Build Prep') {
      sh("""
        rm -rf env
        python3.6 -m venv env
        """)
    }

    grxStage('Run Unit Tests') {
    	sh("""
        . env/bin/activate
        export PYTHONPATH="`pwd`"
        pip3.6 install -r requirements.txt
        python3.6 setup.py test
        """)
    }

    grxStage('Build Library') {
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
      } // Upload
    } // grxStage
  } // grxBuild
} // node
