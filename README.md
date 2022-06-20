# Intelligent-Logistics-Project
Github repo for the intelligent logistics project in the summer semester 2022 at potsdam university.
Contributors: Benjamin Glätzer and Mert Akil


Execute in Windows (example):
python Scripts\cbs_main.py -i Instances\corridor_2_instance.lp -o 25 -a Out\out.lp

Command for visualization with clingraph (CURRENTLY NOT RECOMMENDED, BUGGY AND GIGA-SLOW):
python Scripts\cbs_main.py -i Instances\corridor_2_instance.lp -o 25 -a Out\out.lp -v \PATH\TO\CLINGRAPH\OF\CURRENT\CONDA\ENV

General properties of the project:
 - non-anonymous MAPF
 - detection for vertex and edge conflicts
 - apply MetaAgent-CBS in ASP and extend it with some interesting features