param([Parameter(ValueFromRemainingArguments = $true)][string[]]$PythonArgs)
$ErrorActionPreference = 'Stop'
$repoRoot = Split-Path -Parent $PSScriptRoot
$extraPackages = Join-Path $repoRoot 'work/python-deps'
$codexPython = 'C:\Users\15704\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
if (-not (Test-Path -LiteralPath $codexPython)) { throw 'Required Codex Python runtime is missing.' }
if (-not (Test-Path -LiteralPath $extraPackages)) { throw 'Project dependency directory is missing; restore dependencies before fetching data.' }
$priorPythonPath = $env:PYTHONPATH
$priorEncoding = $env:PYTHONIOENCODING
try {
    $env:PYTHONPATH = if ($priorPythonPath) { "$extraPackages;$priorPythonPath" } else { $extraPackages }
    $env:PYTHONIOENCODING = 'utf-8'
    & $codexPython @PythonArgs
    if ($LASTEXITCODE -ne 0) { throw "Codex Python exited with code $LASTEXITCODE." }
} finally {
    $env:PYTHONPATH = $priorPythonPath
    $env:PYTHONIOENCODING = $priorEncoding
}
