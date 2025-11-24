
msg=$1

if [ -z "$msg" ]; then
  msg="None"
  echo "Empty Imput for $0"
#  echo "Default input now is $msg"

fi

git add . && git commit -m "New Commit Number $msg" && git push
