for i in {1..3}; 
do 
    pytest -n 1 --dist load --parallel-threads 4 >> parallel_load.log
    pytest -n 1 --dist no --parallel-threads 4 >> parallel_no.log
done
