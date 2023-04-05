def c_program(x, y):
    code = """
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <omp.h>
#include <unistd.h>

#define MAX_ITERATIONS 1000

int min(int a, int b){return a < b ? a : b;}

signed char sign(long double x){return x < 0 ? -1 : 1;}

unsigned int iterate(long double cx, long double cy, int max_iterations, long double clipping)
{
    unsigned int iterations = 0;
    long double x = 0;
    long double y = 0;
    long double x1;
    long double y1;
    while (iterations < max_iterations)
    {
        x1 = """ + x + """;
        y1 = """ + y + """;
        if (x1 * x1 + y1 * y1 > clipping * clipping)
        {
            return iterations;
        }
        x = x1;
        y = y1;
        iterations++;
    }
    return iterations;
}

unsigned char *compute_set(long double zoom, long double c0x, long double c0y, int width, int height, int max_iterations, long double clipping, int offset_i, int offset_j, int thread_id)
{
    unsigned char *image = malloc(width * height * sizeof(unsigned char));
    register int i, j;
    for (j = 0; j < height; j++)
    {
        for (i = 0; i < width; i++)
        {
            long double x0 = (zoom * (i + offset_i) / height + c0x);
            long double y0 = (zoom * (j + offset_j) / height + c0y);

            int iterations = iterate(x0, y0, max_iterations, clipping);
            unsigned char p = min(iterations, 255);

            image[(j * width + i)] = p;
        }
    }
    return image;
}

void save_ppm(unsigned char *image, int width, int height, char *filename)
{
    register int i, j;
    FILE *fp = fopen(filename, "w");
    fprintf(fp, "P6\\n%d %d\\n255\\n", width, height);
    for (j = 0; j < height; j++)
    {
        for (i = 0; i < width; i++)
        {
            register unsigned char p = image[(j * width + i)];
            // write as grayscale luminance
            fprintf(fp, "%c%c%c", p, p, p);
        }
    }
    fclose(fp);
}

unsigned char *paste_left_right(unsigned char *im1, unsigned char *im2, int width, int height)
{
    unsigned char *image = malloc(2 * width * height * sizeof(unsigned char));
    register int i, j;
    for (j = 0; j < height; j++)
    {
        for (i = 0; i < width; i++)
        {
            image[j * 2 * width + i] = im1[j * width + i];
            image[(2 * j + 1) * width + i] = im2[j * width + i];
        }
    }
    return image;
}
unsigned char *paste_top_bottom(unsigned char *im1, unsigned char *im2, int width, int height)
{
    unsigned char *image = malloc(2 * width * height * sizeof(unsigned char));
    register int i, j;
    for (j = 0; j < height; j++)
    {
        for (i = 0; i < width; i++)
        {
            image[j * width + i] = im1[j * width + i];
            image[(j + height) * width + i] = im2[j * width + i];
        }
    }
    return image;
}

int main(int argc, char *argv[])
{
    long double zoom = 1.0;
    long double c0x = 0.0;
    long double c0y = 0.0;
    int width = 1000;
    int height = 1000;
    long double clipping = 2.0;
    char *filename = "out.ppm";

    int opt;
    while ((opt = getopt(argc, argv, "z:x:y:w:h:c:o:")) != -1)
    {
        switch (opt)
        {
        case 'z':
            zoom = atof(optarg);
            break;
        case 'x':
            c0x = atof(optarg);
            break;
        case 'y':
            c0y = atof(optarg);
            break;
        case 'w':
            width = atoi(optarg);
            break;
        case 'h':
            height = atoi(optarg);
            break;
        case 'c':
            clipping = atof(optarg);
            break;
        case 'o':
            filename = optarg;
            break;
        default:
            exit(EXIT_FAILURE);
        }
    }

    unsigned char *im[16];
#pragma omp parallel for
    for (int i = 0; i < 16; i++)
    {
        int x_offset = (i % 4) * width / 4 - width / 2;
        int y_offset = (i / 4) * height / 4 - height / 2;
        im[i] = compute_set(zoom, c0x, c0y, width / 4, height / 4, MAX_ITERATIONS, clipping, x_offset, y_offset, i);
    }
#pragma endregion
    unsigned char *im2[8];
#pragma omp for
    for (int i = 0; i < 4; i++)
    {
        im2[2 * i] = paste_left_right(im[4 * i], im[4 * i + 1], width / 4, height / 4);
        im2[2 * i + 1] = paste_left_right(im[4 * i + 2], im[4 * i + 3], width / 4, height / 4);
    }
    unsigned char *im3[4];
#pragma endregion

#pragma omp for
    for (int i = 0; i < 4; i++)
    {
        im3[i] = paste_left_right(im2[2 * i], im2[2 * i + 1], width / 2, height / 4);
    }
    unsigned char *im4[2];
#pragma endregion

#pragma omp for
    for (int i = 0; i < 2; i++)
    {
        im4[i] = paste_top_bottom(im3[2 * i], im3[2 * i + 1], width, height / 4);
    }
    save_ppm(paste_top_bottom(im4[0], im4[1], width, height / 2), width, height, filename);
#pragma endregion
    return 0;
}
"""
    # save the file
    with open("py_code.c", "w") as f:
        f.write(code)
        f.close()
        return 0
    return 1
