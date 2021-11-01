# ImageToColorLUT
Deep learning based - Image To [3D Color Lookup tables](https://en.wikipedia.org/wiki/3D_lookup_table)
All tools for training the model.

## Objective:
Color LUTs are a storage medium used to map a set of color values to another, this is widely used in photogeraphy and cinema to preserve the hard work of color artists from one scene to another. The creation of a Color LUT is time-consuming and requires the expertise of [color grading artists](https://en.wikipedia.org/wiki/Color_grading).
The objective of this machine learning model is to automate the creation of LUT from source material (e.g. a movie or photo) with understanding og color, light and the scene it could be possible to transform the image to a universal Color lookup table.

## Dataset:
 - Movie stills from a wide variety of movies from the moviestillsdb.com database. Crawled using Python and Selenium.
 - A few hundered luts gathered from the internet, then mixed and combined together to create new variations. Mixed and randomized to have a large database of acceptable luts.
 - Dataset is composed of pairs of resized movie stills with a LUT applied and the LUT applied (interpolated to a constant dimension).

## How it works
The model uses a convolutional network where the input from the database is the altered movie still, and the desired output is the LUT used to alter said movie still.


## Future improvments
With the same dataset it would be possible to create a network that inverts the effects of color luts making the stills more neutral. Such a network could learn how to remove the effects color luts. This could be a better foundation for creating a new dataset where the movie stills are neutral to begin with and later altered. As the current implementation makes it so that the still in reality has two color grades applied (the original and the dataset LUT).
