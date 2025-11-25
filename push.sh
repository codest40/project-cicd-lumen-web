
msg=$1
now=$(date +"%Y-%m-%d %H:%M:%S")

if [ -z "$msg" ]; then
  msg=$now
  echo "Empty Imput for $0"
#  echo "Default input now is $msg"

fi

git add . && git commit -m "New Commit Number $msg" && git push
