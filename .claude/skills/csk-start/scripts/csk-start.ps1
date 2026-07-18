$ErrorActionPreference = "Stop"

$tool = Join-Path $PSScriptRoot "csk_start.py"
$candidates = @(
    @{ Command = "python3"; Prefix = @() },
    @{ Command = "python"; Prefix = @() },
    @{ Command = "py"; Prefix = @("-3") }
)

foreach ($candidate in $candidates) {
    $resolved = Get-Command $candidate.Command -ErrorAction SilentlyContinue
    if ($null -eq $resolved) {
        continue
    }
    & $resolved.Source @($candidate.Prefix) $tool @args
    exit $LASTEXITCODE
}

[Console]::Error.WriteLine('{"error":"CSK tooling requires Python 3.10+; tried python3, python, and py -3. Start remains read-only."}')
exit 127
