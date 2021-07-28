Task default -depends Build

Task Restore {
    Exec { python -m pip install --upgrade build twine }
}

Task Build -depends Restore {
    Set-Location src/main
    Write-Output "Build main ..."
    Exec { python -m build -o ../../dist }
    Set-Location ../extensions
    foreach ($ext in Get-Childitem -Attributes Directory) {
        Set-Location $ext
        Write-Output "Build $ext ..." 
        Exec { python -m build -o ../../../dist }
        Set-Location ..
    }
    Set-Location ..
}

Task Deploy -depends Build {
    Exec { python -m twine upload --skip-existing --repository pypi dist/* }
}

Task Test {
    Set-Location ./dist
    Write-Output "Install main ..."
    Exec { python -m pip install $(Get-Childitem "schemdule-*.whl")[0] }

    foreach ($ext in Get-Childitem "schemdule_*.whl") {
        Write-Output "Install $ext ..."
        Exec { python -m pip install $ext }
    }

    Exec { python -m schemdule demo }
    Exec { schemdule demo }

    foreach ($ext in Get-Childitem "schemdule_*.whl") {
        Write-Output "Uninstall $ext ..."
        Exec { python -m pip uninstall $ext -y }
    }

    Write-Output "Uninstall main ..."
    Exec { python -m pip uninstall $(Get-Childitem "schemdule-*.whl")[0] -y }
}
