Task default -depends Build

Task Restore {
    Exec { python -m pip install --upgrade build twine }
}

Task Build -depends Restore {
    $readme = $(Get-Childitem "README.md")[0]

    Set-Location src/main
    Write-Output "Build main"

    Copy-Item $readme ./README.md
    Exec { python -m build -o ../../dist }
    Remove-Item ./README.md
    
    Set-Location ../extensions
    foreach ($ext in Get-Childitem -Attributes Directory) {
        Set-Location $ext
        Write-Output "Build $ext" 
        Exec { python -m build -o ../../../dist }
        Set-Location ..
    }
    Set-Location ..
}

Task Deploy -depends Build {
    Exec { python -m twine upload --skip-existing --repository pypi dist/* }
}

Task Install {
    Set-Location ./dist
    Write-Output "Install main"
    Exec { python -m pip install $(Get-Childitem "schemdule-*.whl")[0] }

    foreach ($ext in Get-Childitem "schemdule_*.whl") {
        Write-Output "Install $ext"
        Exec { python -m pip install $ext }
    }
    Set-Location ..
}

Task Uninstall {
    Set-Location ./dist
    foreach ($ext in Get-Childitem "schemdule_*.whl") {
        Write-Output "Uninstall $ext"
        Exec { python -m pip uninstall $ext -y }
    }

    Write-Output "Uninstall main"
    Exec { python -m pip uninstall $(Get-Childitem "schemdule-*.whl")[0] -y }
    Set-Location ..
}

Task Demo {
    Exec { python -m schemdule demo }
    Exec { schemdule demo }
}

Task Test -depends Install, Demo, Uninstall

Task Clean {
    foreach ($dist in Get-Childitem ./dist) {
        Write-Output "Remove $dist"
        Remove-Item $dist
    }
    foreach ($egg in Get-Childitem -Recurse *.egg-info) {
        Write-Output "Remove $egg"
        Remove-Item -Recurse $egg
    }
}