pipeline {
  agent { dockerfile { filename 'Containerfile' } }
  stages {
    stage('Unit tests') { steps { sh 'python -m pytest -q tests' } }
    stage('Syntax check') {
      steps {
        dir('ansible') {
          sh 'for p in patch rt_check proxmox_vm; do ansible-playbook --syntax-check playbooks/$p.yml; done'
        }
      }
    }
    stage('SLA report') {
      steps { sh 'python -m patchsla.sla findings.json' }  // fails the build on a breach
    }
  }
}
