# A parallel framework in C for generating fractals

## Table of Contents

1.  [Usage](#usage)
2.  [Examples](#examples)

---

## 1. Usage

### 1.1 Installation

Simply clone the repository and you are ready to go.

```bash
git clone https://github.com/VTrelat/Fractals.git
```

### 1.2 Compilation

This program makes use of the [OpenMP](https://www.openmp.org/) library. To compile it, you need to have the OpenMP library installed on your system. If you are using GCC, make sure to have GCC 4.9 or higher.

```bash
gcc --version
```

Then, you can compile the program using the following command:

```bash
gcc -O3 -fopenmp -o fractals parallel.c
```

> **Note:** the `O3` flag is optional. It enables the compiler to optimize the code. It is recommended to use it, but depending on the versions of GCC, using `fopenmp` will set the optimization level to `O3` by default.

Before compiling, you may want to change the equation used to generate the fractal. To do so, you need to modify the values for `x1` and `y1` in the function `iterate` in `parallel.c`:

```c
unsigned int iterate(...)
{
    ...
    while (iterations < max_iterations)
    {
        x1 = // your equation for x1
        y1 = // your equation for y1
        ...
    }
    ...
}
```

Variable `x1` (resp. `y1`) represents the real (resp. imaginary) part of the complex number for the next iteration. For instance, for the Mandelbrot set, the equation is $z_{n+1} = z_n^2 + c$, which defines two sequences $x_{n+1} = Re(z_{n+1}) = x_n^2 - y_n^2 + Re(c)$ and $y_{n+1} = Im(z_{n+1}) = 2 x_n y_n + Im(c)$.
This would be programmed as:

```c
x1 = x0 * x0 - y0 * y0 + c0x;
y1 = 2 * x0 * y0 + c0y;
```

### 1.3 Execution

The program takes 6 arguments:

-   `zoom`: float, the zoom level
-   `c0x`: float, the initial x coordinate of the center of the image
-   `c0y`: float, the initial y coordinate of the center of the image
-   `width`: int, the width of the image
-   `height`: int, the height of the image
-   `clipping`: int, the maximal modulus from the origin to be considered in the set

```bash
Usage: ./fractal <zoom> <c0x> <c0y> <width> <height> <clipping>
```

We obtain a ppm image `out.ppm` in the current directory.

---

## 2. Examples

### 2.1 Mandelbrot set

The recursive equation used to generate the Mandelbrot set is:

$$
z_{n+1} = z_n^2 + c
$$

where $z_0 = 0$ and $c$ is a complex number.

It can be shown that any number in the Mandelbrot set is bounded by a modulus of $2$. Therefore, the clipping value can be set to $2$.
We could also only compute the upper half of the image and then mirror it since the Mandelbrot set is symmetrical with respect to the real axis, but this is specific to the Mandelbrot set.

With the following command:

```bash
./fractal 1.0 0.0 0.0 1000 1000 2.0
```

We obtain the following image:

<div style="text-align:center">
<img src="./images/mandelbrot.png" width=250 height=250 />
</div>

### 2.2 Julia Island

Julia Island is part of the Mandelbrot set.
It can be obtained with the following command:

```bash
./fractal 0.00000011 -1.76877883 -0.00173891 2000 1000 2.0
```

We obtain the following image:

<div style="text-align:center">
<img src="./images/juliaisland.png" width=500 height=250 />
</div>

### 2.3 Burning ship fractal

The recursive equation used to generate the Burning Ship fractal is:

$$
z_{n+1} = \left| z_n \right|^2 + c
$$

where $z_0 = 0$ and $c$ is a complex number.

It can also be shown that any number in the set is bounded by a modulus of $2$. Therefore, the clipping value can be set to $2$.

With the following command:

```bash
./fractal 0.025 -1.7 -0.04 2000 1000 4.0
```

We obtain the following image:

<div style="text-align:center">
<img src="./images/burningship.png" width=500 height=250 />
</div>
