/* 
  tiff2raw - Convert TIFF images to raw format

  This program converts 8 bit/pixel grayscale and 24 bit/pixel TIFF images as
  used in the SIPI Image Database to raw format.  It should properly convert
  the TIFF images in the database back to the raw data format originally used
  in the database.  Image files in raw format contains only image data.  There
  are no headers, trailers, etc.  Pixels are in the file in a left-right,
  top-bottom sequence.

  Examples:

  To convert a grayscale TIFF image (image.tiff) to a raw image in 
  image.raw do 

      tiff2raw image.tiff image.raw

  If the output filename is not specified, the raw data is writting to the
  standard output

      tiff2raw image.tiff

  To convert a 24-bit/pixel TIFF image (image.tiff) to three raw images,
  the basename of the output files must be specified.

      tiff2raw image.tiff output

  The raw image output will be written to three files: "output.red",
  "output.grn" and "output.blu".

  NOTE: This program has NOT been tested on too many other TIFF image and there
  are probably many TIFF images it doesn't work on.

  Program requires the "libtiff" library from http://www.libtiff.org

  Allan G. Weber
  weber@sipi.usc.edu
  Updated: June 9, 2004
*/


#include <stdio.h>
#include "tiffio.h"

int debug;

/* for RGB image create three output files with these extensions */
char *color[3] = { "red", "grn", "blu" };

char text[80];
FILE *ofp[3];
unsigned char *obuf[3];

main(argc, argv)
int argc;
char *argv[];
{
    char c;
    int errflg;
    extern int optind;
    extern char *optarg;
    TIFF* tif;
    uint32 width, height, *raster, *p;
    uint16 depth;
    size_t npixels;
    int i;
    uint32 x, y, z;
    unsigned char *pr, *pg, *pb;

    debug = errflg = 0;

    while ((c = getopt(argc,argv,"d")) != EOF)
	switch (c) {
	  case 'd':
	    debug = 1;
	    break;
	  case '?':
	    errflg = 1;
	    break;
	}
    if (errflg) {
	usage(argv[0]);
	exit(1);
    }

    if (optind < argc) {
	if ((tif = TIFFOpen(argv[optind], "r")) == NULL) {;
	    fprintf(stderr, "Can't open input file \"%s\"\n", argv[optind]);
	    exit(1);
	}
	optind++;
    }
    else {
	fprintf(stderr, "Must specify input file\n");
	usage(argv[0]);
	exit(1);
    }

    TIFFGetField(tif, TIFFTAG_IMAGEWIDTH, &width);
    TIFFGetField(tif, TIFFTAG_IMAGELENGTH, &height);
    npixels = width * height;

    /* See if this is a color or gray image */
    TIFFGetField(tif, TIFFTAG_SAMPLESPERPIXEL, &depth);
    if (depth == 3) {		/* RGB color image */
	if (optind < argc) {
            for (i = 0; i < 3; i++) {
                if ((obuf[i] = (unsigned char *) malloc(width)) == NULL) {
                    fprintf(stderr, "Can't malloc output buffer\n");
		    TIFFClose(tif);
                    exit(1);
                }
		/* Use the output file name as the basename for the file
		   and add extensions for each color */
                sprintf(text, "%s.%s", argv[optind], color[i]);
                if ((ofp[i] = fopen(text, "w")) == NULL) {
                    fprintf(stderr, "Can't open %s for output\n", text);
		    TIFFClose(tif);
                    exit(1);
                }
            }
	}
	else {
	    fprintf(stderr, "Must specify output file for color output\n");
	    TIFFClose(tif);
	    exit(1);
	}
    }
    else if (depth == 1) {
	if ((obuf[0] = (unsigned char *) malloc(width)) == NULL) {
	    fprintf(stderr, "Can't malloc output buffer\n");
	    TIFFClose(tif);
	    exit(1);
	}
	if (optind < argc) {
            if ((ofp[0] = fopen(argv[optind], "w")) == NULL) {
                fprintf(stderr, "Can't open %s for output\n", argv[optind]);
		TIFFClose(tif);
                exit(1);
            }
	}
	else
	    ofp[0] = stdout;
    }
    else {
	fprintf(stderr, "Unrecognized image depth = %d\n");
	TIFFClose(tif);
	exit(1);
    }

    if (debug)
	printf("%d x %d x %d = %d pixels\n", width, height, depth, npixels);

    raster = (uint32*) _TIFFmalloc(npixels * sizeof (uint32));
    if (raster != NULL) {
	if (TIFFReadRGBAImageOriented(tif, width, height, raster,
				      ORIENTATION_TOPLEFT, 0)) {
	    if (depth == 3) {
		p = raster;
		for (y = 0; y < height; y++) {
		    pr = obuf[0];
		    pg = obuf[1];
		    pb = obuf[2];
		    for (x = 0; x < width; x++) {
			z = *p++;
			*pr++ = TIFFGetR(z);
			*pg++ = TIFFGetG(z);
			*pb++ = TIFFGetB(z);
		    }
		    for (i = 0; i < 3; i++)
			fwrite(obuf[i], 1, width, ofp[i]);
		}
	    }
	    else {		/* depth must be 1 */
		p = raster;
		for (y = 0; y < height; y++) {
		    pr = obuf[0];
		    for (x = 0; x < width; x++) {
			z = *p++;
			*pr++ = TIFFGetR(z);
		    }
		    fwrite(obuf[0], 1, width, ofp[0]);
		}
	    }
	}
	_TIFFfree(raster);
    }
    TIFFClose(tif);
    exit(0);
}

usage(s)
char *s;
{
    fprintf(stderr, "Usage: %s [-d] input-TIFF-file output-raw-file\n", s);
}
