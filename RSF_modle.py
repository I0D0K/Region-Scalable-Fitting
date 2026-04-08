import numpy as np
import cv2
import matplotlib.pyplot as plt


# Define Gaussian kernel function
def gaussian_kernel(sigma):
    kernel = cv2.getGaussianKernel(int(round(4 * sigma)) + 1, sigma)
    kernel = np.dot(kernel, kernel.T)
    return kernel


# Define smoothed Heaviside function
def heaviside_epsilon(z, epsilon=1.0):
    return 0.5 * (1 + (2 / np.pi) * np.arctan(z / epsilon))


# Define smoothed Dirac delta function
def dirac_epsilon(z, epsilon=1.0):
    return (epsilon / np.pi) / (epsilon * epsilon + z * z)


# RSF model evolution function
def RSF(phi, img, lambda1, lambda2, mu, nu, kernel, step, epsilon=1.0, max_iter=1000):
    for i in range(max_iter):
        Hea = heaviside_epsilon(phi, epsilon)
        Drc = dirac_epsilon(phi, epsilon)

        # Compute gradient and curvature
        Iy, Ix = np.gradient(phi)
        s = np.sqrt(Ix * Ix + Iy * Iy)
        Nx = Ix / (s + 1e-8)
        Ny = Iy / (s + 1e-8)
        Mxx, Nxx = np.gradient(Nx)
        Nyy, Myy = np.gradient(Ny)
        cur = Nxx + Nyy  # curvature

        Length = nu * Drc * cur

        # Compute Laplacian term
        Lap = cv2.Laplacian(phi, -1)
        Penalty = mu * (Lap - cur)

        # Compute local intensity fitting functions
        f1 = cv2.filter2D(Hea * img, -1, kernel) / cv2.filter2D(Hea, -1, kernel)
        f2 = cv2.filter2D((1 - Hea) * img, -1, kernel) / cv2.filter2D(1 - Hea, -1, kernel)

        # Compute data fitting terms
        R1 = (lambda1 - lambda2) * img ** 2
        R2 = 2 * lambda2 * img * cv2.filter2D(f2, -1, kernel) - 2 * lambda1 * img * cv2.filter2D(f1, -1, kernel)
        R3 = lambda1 * cv2.filter2D(f1 ** 2, -1, kernel) - lambda2 * cv2.filter2D(f2 ** 2, -1, kernel)

        # Combine all energy terms
        RSFterm = -Drc * (R1 + R2 + R3)

        # Update level set function
        phi = phi + step * (RSFterm + Length + Penalty)

    return phi


# Initialize level set function
def initialize_phi(shape, radius=20):
    h, w = shape
    Y, X = np.ogrid[:h, :w]
    cX, cY = w // 2, h // 2
    phi = np.sqrt((X - cX) ** 2 + (Y - cY) ** 2) - radius
    return phi


# Main function
if __name__ == "__main__":
    img = cv2.imread("your .bmp", cv2.IMREAD_GRAYSCALE)  # Load grayscale image
    phi = initialize_phi(img.shape)  # Initialize level set function

    # Perform RSF model evolution
    phi = RSF(
        phi,
        img,
        kernel=gaussian_kernel(sigma=8.0),  # Generate Gaussian kernel
        epsilon=1.0,  # Smoothing parameter for Heaviside and Dirac functions
        # Define model parameters
        lambda1=1.0,
        lambda2=1.0,
        mu=1.0,
        nu=1.0,
        step=0.1,
        max_iter=10000
    )

    # Display original image and segmentation result
    plt.figure(figsize=(10, 5))

    # Original image
    plt.subplot(1, 2, 1)
    plt.imshow(img, cmap='gray')
    plt.title("Original Image")
    plt.axis('off')

    # Segmentation result
    plt.subplot(1, 2, 2)
    plt.imshow(img, cmap='gray')
    plt.contour(phi, levels=[0], colors='r')
    plt.title("Final Segmentation")
    plt.axis('off')

    plt.show()