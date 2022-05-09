# Intelligent-Logistics-Project
Github repo for the intelligent logistics project in the summer semester 2022 at potsdam university.
Contributors: Benjamin Glätzer and Mert Akil


Execute in Windows:
clingo Instances\corridor_2_instance.lp Encodings\input.lp Encodings\plans.lp Encodings\merge.lp Encodings\output.lp -V0 --out-atomf=%s. -c horizon=25 > Out\final_plans.lp

Execute in Linux:
clingo Instances/corridor_2_instance.lp Encodings/input.lp Encodings/plans.lp Encodings/merge.lp Encodings/output.lp -V0 --out-atomf=%s. -c horizon=25 > Out/final_plans.lp

Truncate last line to visualize with asprilo-visualizer.


General properties of the project:
 - non-anonymous MAPF
 - detection for vertex, edge and following conflicts
 - apply MetaAgent-CBS in ASP and extend it with some interesting features