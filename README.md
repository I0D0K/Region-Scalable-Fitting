# Region-Scalable-Fitting
This project was developed collaboratively by me and ChatGPT.
The Region Scalable Fitting (RSF) model is an image segmentation technique based on variational methods.

## RSF Energy Functional

The energy functional of the Region Scalable Fitting (RSF) model is defined as:
<p align="center">
  <img src="https://latex.codecogs.com/png.image?\dpi{110}E(\phi)=\int_{\Omega}[\lambda_1H(\phi)(I(x)-c_1)^2+\lambda_2(1-H(\phi))(I(x)-c_2)^2]dx+\mu\int_{\Omega}|\nabla\phi(x)|dx+\nu\int_{\Omega}\kappa(\phi(x))^2dx" alt="RSF Equation" />
</p>

## Components

**Data term:**

<p align="center">
  <img src="https://latex.codecogs.com/png.image?\dpi{110}E_{\text{data}}(\phi)=\int_\Omega[\lambda_1H(\phi)(I(x)-c_1)^2+\lambda_2(1-H(\phi))(I(x)-c_2)^2]dx" alt="Data term" />
</p>

**Heaviside function:**

<p align="center">
  <img src="https://latex.codecogs.com/png.image?\dpi{110}H(\phi)=\frac{1}{2}\left(1+\frac{2}{\pi}\arctan(\frac{\phi}{\epsilon})\right)" alt="RSF Equation" />
</p>

**Smoothness term:**

<p align="center">
  <img src="https://latex.codecogs.com/png.image?\dpi{110}E_{\text{smooth}}(\phi)=\mu\int_\Omega|\nabla\phi(x)|dx" alt="RSF Equation" />
</p>

**Curvature term:**

<p align="center">
  <img src="https://latex.codecogs.com/png.image?\dpi{110}E_{\text{curvature}}(\phi)=\nu\int_\Omega\kappa(\phi(x))^2dx" alt="RSF Equation" />
</p>

**Curvature definition:**

<p align="center">
  <img src="https://latex.codecogs.com/png.image?\dpi{110}\kappa(\phi(x))=\text{div}\left(\frac{\nabla\phi}{|\nabla\phi|}\right)" alt="RSF Equation" />
</p>

## Program Design Workflow

- **Gaussian Kernel Function**:
  First, define a Gaussian kernel function to perform local smoothing on the image and compute neighborhood information for each pixel.
- **Approximate Heaviside and Dirac Functions**:
  Use approximate Heaviside and Dirac functions to handle the boundary and curvature terms in the level set framework.
- **RSF Model Implementation**:
  In each iteration, compute the contributions from the data term, boundary term, and Laplacian term, and update the level set function by combining these energy components.
- **Initialization**:Initialize the level set function using a distance transform, assigning a distance value to each pixel, and define the initial contour of the target region by setting a threshold.
- **Iterative Update**:
  Perform iterative updates according to the RSF model, and eventually obtain the final segmentation result of the target region.

## Segmentation Result
The following results are obtained using the RSF model on sample images.

<p align="center">
  <img src="figures/cirno result.png" width="60%" />
</p>

<p align="center">
  <img src="figures/tom result.png" width="60%" />
</p>

## Limitations

The current implementation demonstrates the feasibility of the RSF model for image segmentation; however, several limitations remain:

- **Color image handling**: The model currently operates on grayscale images and lacks full support for color-aware energy modeling.
- **Computational cost**: The iterative level set evolution is computationally intensive and may be slow for large-scale images.
- **Parameter sensitivity**: Model performance depends on manually tuned hyperparameters.
- **Convergence criteria**: A strict and adaptive stopping condition has not yet been fully established.
