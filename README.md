# Intelligent-Logistics-Project
Github repo for the intelligent logistics project in the summer semester 2022 at potsdam university.
Contributors: Benjamin Glätzer and Mert Akil


Execute in Windows (example):
```
python Scripts\cbs_main.py -i Instances\corridor_2_instance.lp -o 25 -a Out\out.lp
```

Command for visualization with apsrilo viz:
```
python Scripts\cbs_main.py -i Instances\corridor_2_instance.lp -o 25 -a Out\out.lp -v
```

For benchmarking: 
```
python Scripts\cbs_main.py -i Instances\corridor_2_instance.lp -o 25 -b out\benchmark.csv
```

You can change the behaviour at goal for the agents from disappear to stay at target (careful, not fully tested):
```
python Scripts\cbs_main.py -i Instances\corridor_2_instance.lp -o 25 -s
```

General properties of the project:
 - non-anonymous MAPF
 - detection for vertex and edge conflicts
 - apply MetaAgent-CBS in ASP and extend it with some interesting features