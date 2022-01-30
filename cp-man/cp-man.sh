#!/bin/bash
#help
help(){
    echo "cp-man -p CF -t div-2 -n 999 -u j.com"
}
#main prog
while getopts ":p:t:n:u:" opt; do
    case $opt in
        p) plat="$OPTARG";;
        t) type="$OPTARG";;
        u) url="$OPTARG";;
        n) name="$OPTARG";;
        \?) help
        exit 1;;
    esac
    
    case $OPTARG in
        -*) echo "Option $opt needs a valid argument"
            exit 1
        ;;
    esac
done

this=`pwd`
#codeforces-div-2
if [[ "$plat" == "CF" ]]
then
    if [[ "$type" == "div-2" ]]
    then
        cd $project/Competitive-Coding/Codeforces/division-2/
        mkdir "$name"
        printf "\n1. [round-$name](./$name)|[link to questions]($url)">>./readme.md
        code "$project/Competitive-Coding/Codeforces/division-2/$name"
    elif [[ "$type" == "div-1" ]]
    then
        cd $project/Competitive-Coding/Codeforces/division-1/
        mkdir "$name"
        printf "\n1. [round-$name](./$name)|[link to questions]($url)">>./readme.md
        code "$project/Competitive-Coding/Codeforces/division-1/$name"
    elif [[ "$type" == "div-3" ]]
    then
        cd $project/Competitive-Coding/Codeforces/division-3/
        mkdir "$name"
        printf "\n1. [round-$name](./$name)|[link to questions]($url)">>./readme.md
        code "$project/Competitive-Coding/Codeforces/division-3/$name"
    fi
    #random questions
elif [[ "$plat" == "R" ]]
then
    cd $project/Competitive-Coding/Random-Questions/
    mkdir $name
    cd $name/
    touch "Solution.java"
    printf "//$url\npublic class Solution{}">>./"Solution.java"
    cd ..
    printf "\n\n1. [$name](./$name/Solution.java)\n\t-[Problem-statement]($url)">>./readme.md
    code $project/Competitive-Coding/Random-Questions/$name/
    #coustom args
fi
cd $this

