#!/bin/bash

readonly _DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
readonly SRC_DIR="${_DIR}/src"
readonly DB_INIT_FILE="${SRC_DIR}/db_init.sql"
readonly OS_TYPE="${OSTYPE}"


function main() {
        if [[ "$OSTYPE" == "linux-gnu"* ]]; then
                # linux
                main_linux
        elif [[ "$OSTYPE" == "darwin"* ]]; then
                # Mac OSX
                main_macos
        fi
}

function main_linux() {
        service mysql start # start mysql server
        # sudo service mysql status
        mysql -u root < ${DB_INIT_FILE}
        (cd ${SRC_DIR}
         python -m pytest
         python app.py
        )
        service mysql stop # stop mysql server
        # sudo service mysql status
}

function main_macos() {
        mysql.server start
        mysql -u root < ${DB_INIT_FILE}
        (cd ${SRC_DIR}
         python -m pytest
         python app.py
        )
        mysql.server stop
}

main
