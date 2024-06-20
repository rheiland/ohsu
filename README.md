# ohsu

This repository tries to provide some helpful guidance on using PhysiCell + Studio, using simple, illustrative models, with some sample analysis scripts (coming). If you do not yet have PhysiCell + Studio installed, you can try using this repo (https://github.com/rheiland/studio_template) and following the instructions there.

# Background info

* [PhysiCell Studio Guide](https://github.com/PhysiCell-Tools/Studio-Guide/blob/main/README.md)
* [Studio basics video](https://www.youtube.com/watch?v=jkbPP1yDzME) (from PhysiCell 2023 workshop)
* [Digitize your Biology preprint](https://www.biorxiv.org/content/10.1101/2023.09.17.557982v3) ("Rules" for cell behavior paper)

Reminder: since simulations are stochastic (when `# threads` > 1), your results may not exactly match those shown here.

# Model1: no rules vs. 1 rule

<img src="./images/model1_t0.png" width="30%"> 

Initial conditions (ICs) - randomly positioned cells of `ctype1` in the domain. Created using the ICs tab:<br>
<img src="./images/create_ICs.png" width="50%"> 


<hr>
After running the simulation for 1 day of simulation time:

<img src="./images/model1_no_rules.png" width="30%">  <img src="./images/model1_1rule_plot.png" width="30%"> <img src="./images/population_plot1.png" width="30%">
<br>
Showing two different outcomes: no rules (left), 1 rule (right).
I've also created a currently unused `ctype2`. We will have `ctype1` cells differentiate into `ctype2` under certain conditions (next).
<hr>

Some key parameters:
* cell cycle leads to proliferation
* cells are motile (with unbiased movement)
* cells do not die: Death tab (not shown) - both Apoptosis and Necrosis death rates = 0
<img src="./images/model1_cycle.png" width="60%">
<img src="./images/model1_motility.png" width="60%">
<hr>

<img src="./images/model1_1rule.png" width="60%"> <img src="./images/rule_contact_attachrate.png" width="30%">
<br>
1 rule: when one cell comes into contact with another, its (spring-like) attachment rate increases

# Model2: 2 rules, plus chemotaxis

If we add a second rule: when a cell of `ctype1` experiences pressure (from neighboring cells), it differentiates (transforms to) `ctype2`

<img src="./images/model1_2rules_tab.png" width="60%">

<img src="./images/model1_2rules.png" width="30%"><img src="./images/population_plot2.png" width="30%">

# Model1: 2 rules + chemotaxis

* Define a diffusing `signal` in the Microenv
* Tell `ctype2` cells to chemotax toward it

<img src="./images/microenv_signal.png" width="60%">
<img src="./images/ctype2_chemotaxis.png" width="60%"> 

Be sure to select `ctype2` as the ones chemotaxing

<img src="./images/chemotax_9hr.png" width="30%"><img src="./images/chemotax_14hr.png" width="30%"><img src="./images/chemotax_1day.png" width="30%">

<hr>

# Analysis

We provide a Python script which performs a relatively simple analysis - it counts the (approx) number of "cell clusters". The algorithm creates a graph 
from the existing data. If two cells are < "predefined distance" from each other, an "edge" is created between them. We then use a connected components function
from [networkx](https://networkx.org/) (an open source Python package for graph analysis) to tell us how many clusters are found.

<img src="./images/model1_no_rules.png" width="30%">  <img src="./images/model1_1rule_plot.png" width="30%"> 

```
$ python clusters_conn_comp.py output_model1_1rule 0
...
for time=0.0: # of clusters for cell type 0 = 244

$ python clusters_conn_comp.py output_model1_1rule 0
...
for time=1440.0: # of clusters for cell type 0 = 59
```





