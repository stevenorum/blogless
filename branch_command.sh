
branchify(){
    if [ -z "$1" ]; then
        bname="`whoami``date +%Y%m%d`"
    else
	bname=$1
    fi
    git checkout $bname && return
    git checkout -b $bname
    git push --set-upstream origin $bname
}
