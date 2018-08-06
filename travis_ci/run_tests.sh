function find_files {
    file_names=$(find . -name '*.py' | grep --invert-match 'test' | grep --invert-match '__init__')
    echo ${file_names}
}

function my_mypy {
    echo
    echo "##############"
    echo "MYPY"
    echo "##############"
    echo
    file_names=($(find_files))
    error=false
    for name in "${file_names[@]}"
    do
        echo ${name}
        mypy --ignore-missing-import ${name}
        if [[ ${?} != 0 ]]
        then
            error=true
        fi
    done
    if [[ ${error} = true ]]
    then
        return 1
    else
        return 0
    fi
}


function my_pyflakes {
    echo
    echo "##############"
    echo "PYFLAKES"
    echo "##############"
    echo
    file_names=($(find_files))
    error=false
    for name in "${file_names[@]}"
    do
        echo ${name}
        pyflakes ${name}
        if [[ ${?} != 0 ]]
        then
            error=true
        fi
    done
    if [[ ${error} = true ]]
    then
        return 1
    else
        return 0
    fi
}

function my_pylint {
    echo
    echo "##############"
    echo "PYLINT"
    echo "##############"
    echo
    file_names=($(find_files))
    error=false
    for name in "${file_names[@]}"
    do
        echo ${name}
        pylint ${name}
        if [[ ${?} != 0 ]]
        then
            error=true
        fi
    done
    if [[ ${error} = true ]]
    then
        return 1
    else
        return 0
    fi
}

function my_pytest {
    echo
    echo "##############"
    echo "PYTEST"
    echo "##############"
    echo
    rm -r OUTPUT_TEST_FOLDER
    pytest --cov=transphire_transform --cov-report term-missing -s
    return ${?}
}

my_${1}
exit ${?}
