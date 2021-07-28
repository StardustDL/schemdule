Task default -depends Build

Task Restore {
    Exec { python -m pip install --upgrade build twine }
}

Task Build -depends Restore {
    Set-Location src/main
    Exec { python -m build -o ../../dist }
    # cd ../prompters
    # cd simplemessagebox && python -m build -o ../../../dist
    # cd ../..
}

Task Deploy -depends Build {
    Exec { python -m twine upload --skip-existing --repository pypi dist/* }
}

Task Test {
    Exec { python -m pip install ./dist/schemdule-0.0.4-py3-none-any.whl }
    Exec { python -m schemdule demo }
    Exec { schemdule demo }
}
