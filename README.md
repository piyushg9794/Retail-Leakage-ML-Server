# Retail-Leakage-ML-Server
Machine Learning Server for 'Retail Leakage &amp; Surplus in PDS' project

* This Repo contains the code for ML server of a project.
* Complete Project can be found [here](https://github.com/MMH-MMH/Retail-Leakage-and-Surplus-with-AI).


## Algorithms:


![](https://github.com/piyushg9794/Retail-Leakage-ML-Server/blob/main/Algorithm.png).



* Random Forest Model captures the dependecy of Demand on the Demographic & Geography of the area.
* Gaussian process Regression Model capturs the short-term & long-term trends wrt time.
* In GPR Model kernel used is a combination of 3 kernels:
  * Smooth Kernel (RBF): This kernel is used to learn the long term smooth changes in trends.
  * Periodic Kernel (Exp. Sine Squared * RBF): ESS kernel is a periodic kernel & its multiplication with RBF enables it to adopt the periodicity of trained data.
  * Irregular kernel (Rational Quadratic): This kernel is used to learn short-term to mid-term irregularites in data. In practical sense this will help in modelling some unpredictable features of data.


