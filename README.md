# Physics Lab - Best Fit Line, Error Analysis and Plotting

This Jupyter notebook and streamlit app automate the calculations required for the experiments in which the best fit line needs to be plotted for the observed data points, so that there is no need to do each calculation manually.

It will generate the following output: best fit line slope and intercept and also the errors in these values, and also a sample plot to get an idea of the scale to be chosen for drawing the plot.

**[App Link](https://physics-lab-calculations.streamlit.app/)**

<details>
<summary>Formulae Used</summary>
  
  <br>
  
```math

m = \frac{\sum{(x_i - \bar{x}) y_i}}{\sum{(x_i - \bar{x})^2}}     \quad \quad \quad

c = \bar{y} - m \bar{x}       \quad \quad \quad \quad \quad \quad

\Delta m^2 \approx \frac{1}{D} \frac{1}{{N-2}} \sum_{i=1}^{N} (S_i)^2   \quad \quad \quad

\Delta c^2 \approx \left( \frac{1}{N} + \frac{\bar{x}^2}{D} \right)  \frac{1}{{N-2}} \sum_{i=1}^{N} (S_i)^2

```

```math

D = \sum{(x_i - \bar{x})^2}   \quad  \quad \quad
N = total \ number \ of \ observed \ data \ points   \quad  \quad \quad
S_i = y_i - m x_i - c
```
  
</details>
