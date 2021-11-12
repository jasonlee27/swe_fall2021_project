#!/bin/bash

readonly _DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
readonly SRC_DIR="${_DIR}/src"
readonly DB_INIT_FILE="${SRC_DIR}/db_init.sql"

function main() {

        (cd ${SRC_DIR}
         python -m pytest
         mysql -u root < ${DB_INIT_FILE}
         python app.py
        )
}

main
