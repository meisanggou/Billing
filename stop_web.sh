for port in 2200
do
        lsof -i:$port | awk '{print $2}' | tail -n +2| while read id
        do
                kill -9 $id
        done
done