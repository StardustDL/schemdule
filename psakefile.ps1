Task default -depends Build

Task Restore {
    Exec { python -m pip install --upgrade build twine }
}

Task Build -depends Restore {
    $readme = $(Get-Childitem "README.md")[0]

    Set-Location src/main
    Write-Output "📦 Build main"

    Copy-Item $readme ./README.md
    Exec { python -m build -o ../../dist }
    Remove-Item ./README.md
    
    Set-Location ../extensions
    foreach ($ext in Get-Childitem -Attributes Directory) {
        Set-Location $ext
        Write-Output "📦 Build $ext" 
        Exec { python -m build -o ../../../dist }
        Set-Location ..
    }
    Set-Location ../..
}

Task Deploy -depends Build {
    Exec { python -m twine upload --skip-existing --repository pypi "dist/*" }
}

Task Install {
    Set-Location ./dist

    Write-Output "🛠 Install dependencies"
    if ([System.Runtime.InteropServices.RuntimeInformation]::IsOSPlatform([System.Runtime.InteropServices.OSPlatform]::Linux)) {
        Exec { sudo apt-get update >/dev/null }
        Exec { sudo apt-get install -yq python3-dev libasound2-dev >/dev/null }
        Exec { sudo apt-get install -yq ffmpeg >/dev/null }
    }
    elseif ([System.Runtime.InteropServices.RuntimeInformation]::IsOSPlatform([System.Runtime.InteropServices.OSPlatform]::OSX)) {
        Exec { brew install ffmpeg >/dev/null }
    }
    elseif ([System.Runtime.InteropServices.RuntimeInformation]::IsOSPlatform([System.Runtime.InteropServices.OSPlatform]::Windows)) {
        Exec { choco install ffmpeg -y >$null}
    }

    Write-Output "🛠 Install main"
    Exec { python -m pip install $(Get-Childitem "schemdule-*.whl")[0] }

    foreach ($ext in Get-Childitem "schemdule_*.whl") {
        Write-Output "🛠 Install $ext"
        Exec { python -m pip install $ext }
    }
    Set-Location ..
}

Task Uninstall {
    Set-Location ./dist
    foreach ($ext in Get-Childitem "schemdule_*.whl") {
        Write-Output "⚒ Uninstall $ext"
        Exec { python -m pip uninstall $ext -y }
    }

    Write-Output "⚒ Uninstall main"
    Exec { python -m pip uninstall $(Get-Childitem "schemdule-*.whl")[0] -y }
    Set-Location ..
}

Task Demo {
    Write-Output "⏳ 1️⃣ Version ⏳"
    Exec { schemdule --version }
    Write-Output "⏳ 2️⃣ Help ⏳"
    Exec { schemdule --help }
    Write-Output "⏳ 3️⃣ Extensions ⏳"
    Exec { schemdule ext }
    Write-Output "⏳ 4️⃣ Demo ⏳"
    Exec { python -m schemdule demo }
    Write-Output "⏳ 5️⃣ Demo in verbose ⏳"
    Exec { schemdule -vvv demo }
    Write-Output "⏳ 6️⃣ Demo from file in preview ⏳"
    Exec { python -m schemdule run ./test/demo.py --preview }
    Write-Output "⏳ 7️⃣ Demo from file ⏳"
    Exec { python -m schemdule run ./test/demo.py }
    Write-Output "⏳ 8️⃣ Demo from file in verbose ⏳"
    Exec { schemdule -vvv run ./test/demo.py }
}

Task Test -depends Install, Demo, Uninstall

Task Clean {
    foreach ($dist in Get-Childitem ./dist) {
        Write-Output "🗑 Remove $dist"
        Remove-Item $dist
    }
    foreach ($egg in Get-Childitem -Recurse *.egg-info) {
        Write-Output "🗑 Remove $egg"
        Remove-Item -Recurse $egg
    }
}

Task Format {
    autopep8 -r --in-place .

    foreach ($file in Get-Childitem "*.py" -Recurse) {
        isort $file
    }
}