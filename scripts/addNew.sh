#!/bin/bash
#this is for the management of this project
mkdir $1
touch ./$1/$1.sh
echo '#!/bin/bash' >>./$1/$1.sh
touch ./$1/readme.md
echo "# $1" >>./$1/readme.md