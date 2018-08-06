function find_files {
    file_names=$(find . -name '*.py' | grep --invert-match 'test' | grep --invert-match '__init__')
    echo ${file_names}
}

function my_mypy {
    echo
    echo "##############"
    echo "MYPY"
    echo "##############"
    file_names=($(find_files))
    for name in "${file_names[@]}"
    do
        echo ${name}
        mypy --ignore-missing-import ${name}
    done
}


function my_pyflakes {
    echo
    echo "##############"
    echo "PYFLAKES"
    echo "##############"
    file_names=($(find_files))
    for name in "${file_names[@]}"
    do
        echo ${name}
        pyflakes ${name}
    done
}

function my_pylint {
    echo
    echo "##############"
    echo "PYLINT"
    echo "##############"
    file_names=($(find_files))
    for name in "${file_names[@]}"
    do
        echo ${name}
        pylint ${name}
    done
}

function my_pytest {
    echo
    echo "##############"
    echo "PYTEST"
    echo "##############"
    rm -r OUTPUT_TEST_FOLDER
    pytest --cov=transphire_transform --cov-report term-missing -s
}

my_pytest
my_mypy
my_pyflakes
my_pylint
