# Advanced-Algorithms
Final Individual Project work by implementing Dijkstra's Algorithm or A Algorithm with a runnable code.

/Five Pathfinding Scenarios for Düsseldorf/
Scenario	Start Point	Target Hospitals	Description
- 1	Düsseldorf Hbf (Main Station)	All hospitals	Urban center to nearest emergency care
- 2	Flughafen DUS (Airport)	All hospitals	Airport district to nearest hospital
- 3	Medienhafen	All hospitals	Modern waterfront district routing
- 4	Benrath Palace	All hospitals	Southern district crossing the city
- 5	Altstadt (Rathaus)	Marien Hospital only	Specific destination in north

The expected output should be:
========
Scenario 1: Hbf to Nearest Hospital
========

Nearest hospital by straight-line: Uni_Klinikum

[Dijkstra] to Uni_Klinikum
  Distance: 1.80 km
  Path: Hbf → Uni_Klinikum
  Time: 0.12 ms
  Memory: 25.34 KB
  Nodes Explored: 4

[A*] to Uni_Klinikum
  Distance: 1.80 km
  Path: Hbf → Uni_Klinikum
  Time: 0.08 ms
  Memory: 22.17 KB
  Nodes Explored: 3

========
Comparison
========
Scenario                             Dijkstra (ms)    A* (ms)         Speedup   
---------------------------------------------------------------------------
Scenario 1: Hbf to Nearest Hospital  0.12            0.08            1.50x
Scenario 2: Airport to Nearest Hosp 0.35            0.21            1.67x
Scenario 3: Medienhafen to Nearest H 0.28           0.19            1.47x
Scenario 4: Benrath to Nearest Hosp  0.41           0.26            1.58x
Scenario 5: Altstadt to Marien Hosp  0.19           0.12            1.58x
