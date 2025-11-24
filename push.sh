

if [ -z "$1" ]; then
  $1="None"
  echo "Empty Imput for $0"
  echo "Default input now is $1"
else
  echo "Imput $1 is given for $0"
fi

git add . && git commit -m "New Commit Number $1" && git push
