pipeline {
    agent any

    environment {
        APP_NAME = 'Finkado'
        APP_VERSION = '1.0.0'
        PYTHON_ENTRY = 'finance_app\\main.py'
        VENV_DIR = '.venv'
        PYTHON_EXE_FILE = '.jenkins-python.txt'
        PYINSTALLER_DIST_DIR = 'dist'
        PYINSTALLER_BUILD_DIR = 'build'
        ISS_SCRIPT = 'installer\\setup.iss'
        INSTALLER_OUTPUT_DIR = 'build_output'
        INNO_COMPILER = 'C:\\Program Files (x86)\\Inno Setup 6\\ISCC.exe'
    }

    options {
        timestamps()
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Validate Tools') {
            steps {
                powershell '''
                    $ErrorActionPreference = "Stop"

                    # Testa os comandos globais diretamente no PATH do sistema.
                    $pythonCommand = Get-Command python -ErrorAction Stop
                    & $pythonCommand.Source --version
                    git --version

                    Set-Content -Path $env:PYTHON_EXE_FILE -Value $pythonCommand.Source -Encoding ASCII

                    # Valida o compilador do Inno Setup configurado no Jenkinsfile.
                    if (-not (Test-Path $env:INNO_COMPILER)) {
                        throw "Compilador do Inno Setup nao encontrado: $env:INNO_COMPILER"
                    }

                    & $env:INNO_COMPILER /?
                '''
            }
        }

        stage('Prepare Python Environment') {
            steps {
                powershell '''
                    $ErrorActionPreference = "Stop"

                    if (Test-Path $env:VENV_DIR) {
                        Remove-Item -Recurse -Force $env:VENV_DIR
                    }

                    $resolvedPython = (Get-Content $env:PYTHON_EXE_FILE -Raw).Trim()
                    & $resolvedPython -m venv $env:VENV_DIR

                    $pythonExe = Join-Path $env:VENV_DIR "Scripts\\python.exe"
                    & $pythonExe -m pip install --upgrade pip
                    & $pythonExe -m pip install -r requirements.txt
                    & $pythonExe -m pip install --upgrade pyinstaller
                '''
            }
        }

        stage('Validate Python Code') {
            steps {
                powershell '''
                    $ErrorActionPreference = "Stop"

                    $pythonExe = Join-Path $env:VENV_DIR "Scripts\\python.exe"
                    & $pythonExe -m compileall finance_app
                '''
            }
        }

        stage('Build Executable') {
            steps {
                powershell '''
                    $ErrorActionPreference = "Stop"

                    if (Test-Path $env:PYINSTALLER_DIST_DIR) {
                        Remove-Item -Recurse -Force $env:PYINSTALLER_DIST_DIR
                    }

                    if (Test-Path $env:PYINSTALLER_BUILD_DIR) {
                        Remove-Item -Recurse -Force $env:PYINSTALLER_BUILD_DIR
                    }

                    $pythonExe = Join-Path $env:VENV_DIR "Scripts\\python.exe"
                    & $pythonExe -m PyInstaller `
                        --noconfirm `
                        --clean `
                        --onedir `
                        --windowed `
                        --name $env:APP_NAME `
                        $env:PYTHON_ENTRY

                    $appExe = Join-Path $env:PYINSTALLER_DIST_DIR "$($env:APP_NAME)\\$($env:APP_NAME).exe"
                    if (-not (Test-Path $appExe)) {
                        throw "Executavel nao gerado: $appExe"
                    }
                '''
            }
        }

        stage('Package Installer') {
            steps {
                powershell '''
                    $ErrorActionPreference = "Stop"

                    if (Test-Path $env:INSTALLER_OUTPUT_DIR) {
                        Remove-Item -Recurse -Force $env:INSTALLER_OUTPUT_DIR
                    }

                    New-Item -ItemType Directory -Force -Path $env:INSTALLER_OUTPUT_DIR | Out-Null
                    & $env:INNO_COMPILER $env:ISS_SCRIPT
                '''
            }
        }

        stage('Archive Installer') {
            steps {
                archiveArtifacts artifacts: 'build_output/*.exe', fingerprint: true, followSymlinks: false
            }
        }
    }

    post {
        success {
            echo 'Pipeline concluida com sucesso. Instalador disponivel nos artefatos do build.'
        }
        failure {
            echo 'Pipeline falhou. Verifique o log de console do Jenkins.'
        }
        always {
            cleanWs(
                deleteDirs: true,
                notFailBuild: true,
                patterns: [
                    [pattern: '.venv/**', type: 'INCLUDE'],
                    [pattern: 'build/**', type: 'INCLUDE'],
                    [pattern: 'dist/**', type: 'INCLUDE'],
                    [pattern: 'build_output/**', type: 'INCLUDE'],
                    [pattern: '*.spec', type: 'INCLUDE'],
                    [pattern: '.jenkins-python.txt', type: 'INCLUDE']
                ]
            )
        }
    }
}
