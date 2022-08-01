CHECK="do while"

while [[ ! -z $CHECK ]]; do
    PORT=`python -c "import random; print random.randint(30000,50000)"`
    CHECK=$(sudo netstat -ap | grep $PORT)
    echo $CHECK
done

echo $PORT
