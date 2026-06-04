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
        PYTHON_EXE = 'C:\\Users\\SEU_USUARIO\\AppData\\Local\\Programs\\Python\\Python312\\python.exe'
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

                    function Resolve-PythonExecutable {
                        $candidates = New-Object System.Collections.Generic.List[string]

                        if ($env:PYTHON_EXE) {
                            $candidates.Add($env:PYTHON_EXE)
                        }

                        $pythonCommand = Get-Command python -ErrorAction SilentlyContinue
                        if ($pythonCommand) {
                            $candidates.Add($pythonCommand.Source)
                        }

                        $pyLauncher = Get-Command py -ErrorAction SilentlyContinue
                        if ($pyLauncher) {
                            try {
                                $launcherPython = (& $pyLauncher.Source -3 -c "import sys; print(sys.executable)").Trim()
                                if ($launcherPython) {
                                    $candidates.Add($launcherPython)
                                }
                            } catch {
                                Write-Host "Python Launcher encontrado, mas não conseguiu localizar Python 3."
                            }
                        }

                        @(
                            "$env:ProgramFiles\\Python312\\python.exe",
                            "$env:ProgramFiles\\Python311\\python.exe",
                            "$env:ProgramFiles\\Python310\\python.exe",
                            "${env:ProgramFiles(x86)}\\Python312\\python.exe",
                            "${env:ProgramFiles(x86)}\\Python311\\python.exe",
                            "${env:ProgramFiles(x86)}\\Python310\\python.exe",
                            "C:\\Python312\\python.exe",
                            "C:\\Python311\\python.exe",
                            "C:\\Python310\\python.exe"
                        ) | ForEach-Object {
                            if ($_ -and (Test-Path $_)) {
                                $candidates.Add($_)
                            }
                        }

                        foreach ($candidate in ($candidates | Select-Object -Unique)) {
                            if ([string]::IsNullOrWhiteSpace($candidate)) {
                                continue
                            }

                            $candidate = $candidate.Trim().Trim('"')

                            try {
                                & $candidate -c "import sys; raise SystemExit(0 if sys.version_info >= (3, 10) else 1)"
                                if ($LASTEXITCODE -eq 0) {
                                    return $candidate
                                }
                            } catch {
                                Write-Host "Candidato Python inválido: $candidate"
                            }
                        }

                        $message = @(
                            "Python 3.10+ não foi encontrado pelo Jenkins.",
                            "",
                            "Correções recomendadas no Windows:",
                            "1. Instale o Python para todos os usuários.",
                            "2. Marque a opção 'Add python.exe to PATH' durante a instalação.",
                            "3. Reinicie o serviço do Jenkins após alterar o PATH.",
                            "4. Alternativa: configure uma variável de ambiente do Jenkins chamada PYTHON_EXE apontando para o executável, por exemplo:",
                            "   C:\\Users\\SEU_USUARIO\\AppData\\Local\\Programs\\Python\\Python312\\python.exe"
                        ) -join [Environment]::NewLine

                        throw $message
                    }

                    $resolvedPython = Resolve-PythonExecutable
                    Set-Content -Path $env:PYTHON_EXE_FILE -Value $resolvedPython -Encoding ASCII

                    & $resolvedPython --version
                    git --version

                    if (-not (Test-Path $env:INNO_COMPILER)) {
                        throw "ISCC.exe não encontrado em: $env:INNO_COMPILER"
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
                        throw "Executável não gerado: $appExe"
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
            echo 'Pipeline concluída com sucesso. Instalador disponível nos artefatos do build.'
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
                    [pattern: '*.spec', type: 'INCLUDE']
                ]
            )
        }
    }
}
