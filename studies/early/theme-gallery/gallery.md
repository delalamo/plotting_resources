# Plotting style references

Researched 7 September 2026. These are upstream examples and design references, not new versions of the af2_conformations figures. Images are linked from their authors' repositories/documentation; the two FT images are browser captures of its live legacy templates. Visual-fit assessments below are editorial judgments. Packages have not been installed or compatibility-tested.

## 1. BBC — bbplot and rcookbook

[Repository](https://github.com/bbc/bbplot) · [Recipe collection](https://github.com/bbc/rcookbook)

Bold headlines, white backgrounds, restrained grids, direct annotations, and consistent source footers. The example sheet shows histograms, scatter/bubble charts, stacked bars, and connected-dot comparisons. A strong model for consistency across chart types. `bbc_style()` handles theme elements; palettes and chart-specific adjustments are separate decisions.

![BBC example gallery](https://raw.githubusercontent.com/bbc/bbplot/master/chart_examples/bbplot_example_plots.png)

## 2. Urban Institute — urbnthemes

[Repository and examples](https://github.com/UrbanInstitute/urbnthemes)

Lato typography, cyan/yellow/magenta accents, clear baselines and restrained grids. Includes bar, scatter, line, and stacked-area examples, plus map themes and categorical/diverging/sequential palettes. Particularly useful as a model for a complete plotting toolkit with consistent notes, sources, legends, and layout helpers.

| Scatter | Stacked area |
|---|---|
| ![Urban scatter](https://raw.githubusercontent.com/UrbanInstitute/urbnthemes/HEAD/man/figures/README-scatter-plot-2-1.png) | ![Urban area](https://raw.githubusercontent.com/UrbanInstitute/urbnthemes/HEAD/man/figures/README-area-plot-1.png) |

## 3. hrbrthemes — typography and an FT-inspired dark variant

[Repository](https://github.com/hrbrmstr/hrbrthemes)

Typography-focused ggplot themes with airy layouts, deliberate title/subtitle hierarchy, muted palettes, and examples of scatterplots, facets, bars, and stacked areas. The package includes several distinct styles; a personal guide should choose one font/theme family rather than mix all of them. IBM Plex Sans is an appealing starting point for a scientific identity.

![IBM Plex Sans faceted scatterplot](https://raw.githubusercontent.com/hrbrmstr/hrbrthemes/master/man/figures/README-ps-1.png)

The FT-inspired `theme_ft_rc()` is a separate dark direction: charcoal background, condensed type, and bright accents. It is not the FT's familiar salmon-colored print style.

![FT-inspired dark scatterplot](https://raw.githubusercontent.com/hrbrmstr/hrbrthemes/master/man/figures/README-ft-1.png)

## 4. Apricitas — jptheme

[Repository](https://github.com/MattCowgill/jptheme) · [Theme implementation](https://github.com/MattCowgill/jptheme/blob/main/R/theme_apricitas.R)

Your reference is directly related to the previous package: `theme_apricitas()` wraps `hrbrthemes::theme_ft_rc()`, adding white axis lines and title/legend adjustments. Its README supplies one scatterplot, so it is a compact personal-theme example rather than a broad chart cookbook. Strong visual character, although secondary-text contrast in this sample is low.

![Apricitas scatterplot](https://raw.githubusercontent.com/MattCowgill/jptheme/main/man/figures/README-example-1.png)

## 5. Economist-inspired — ggthemes

[Repository](https://github.com/jrnold/ggthemes) · [Economist theme documentation](https://jrnold.github.io/ggthemes/reference/theme_economist.html)

Blue-gray surroundings, horizontal guides, compact bold headlines and a coordinated palette. The package includes `theme_economist()`, a white-background variant, and matching color scales. It also contains separate FiveThirtyEight and Wall Street Journal themes. These are community implementations, not official newsroom packages. Useful for studying recognizable editorial framing; recipes for a scientific gallery would still need to be developed.

![Economist-inspired scatterplot](https://raw.githubusercontent.com/jrnold/ggthemes/main/man/figures/README-theme_economist-1.png)

## 6. Grattan Institute — grattantheme

[Repository](https://github.com/grattan/grattantheme) · [Vignette](https://grattan.github.io/grattantheme/articles/using_grattantheme.html)

A warm orange/gold/burgundy palette, sparse grids and strong baselines. Beyond the theme, the repository documents chart-orientation handling, annotations, and consistent export formats. The vignette is largely variations on iris scatterplots, so its displayed chart-type breadth is narrower than BBC's. Its architecture is nevertheless a useful reference for a full style guide.

![Grattan palette applied to an iris scatterplot](https://grattan.github.io/grattantheme/articles/using_grattantheme_files/figure-html/unnamed-chunk-12-1.png)

The upstream example labels the x-axis “Species” despite mapping sepal length; retain it as a visual reference, not a labeling template.

## 7. Claus Wilke — dataviz and dviz.supp

[Book-source repository](https://github.com/clauswilke/dataviz) · [Supporting R package](https://github.com/clauswilke/dviz.supp) · [Visual directory](https://clauswilke.com/dataviz/directory-of-visualizations.html)

The strongest reference here for breadth of scientific chart types: distributions, boxplots, violins, ridgelines, uncertainty, scatterplots, heatmaps, and small multiples. The directory below uses stylized schematic examples; the book's full data figures use a more restrained treatment. Study its scientific recipes alongside an editorial theme to develop a distinct identity. The book artwork and supporting R package have different licenses; consult each before redistributing or adapting source assets.

![Wilke distribution chart directory: schematic examples](https://clauswilke.com/dataviz/directory_of_visualizations_files/figure-html/multiple-distributions-1.png)

![Wilke full-data violin plot](https://clauswilke.com/dataviz/boxplots_violins_files/figure-html/lincoln-temp-violins-1.png)

## 8. Financial Times — official Visual Vocabulary templates

[Repository](https://github.com/ft-interactive/visual-vocabulary) · [Live gallery](https://ft-interactive.github.io/visual-vocabulary/) · [Chart Doctor reference](https://github.com/Financial-Times/chart-doctor/tree/main/visual-vocabulary)

Broad official D3 template collection, including lines, bars, boxplots, histograms, scatterplots, heatmaps, slopes, small multiples, and flows. This is a design/coverage reference for an R implementation. These legacy templates contain dummy data and placeholder copy; the captures below show their current browser rendering, including fallback typography, rather than polished current FT journalism.

| [Line template](https://ft-interactive.github.io/visual-vocabulary/line/) | [Boxplot template](https://ft-interactive.github.io/visual-vocabulary/boxplot/) |
|---|---|
| ![FT line template](ft-line.png) | ![FT boxplot template](ft-boxplot.png) |

## Implications for af2_conformations

Inspected the three original plotting scripts:

- [Figure 1](https://github.com/delalamo/af2_conformations/blob/main/figures/fig1/lat1.R): outlined scatter points, TM-score reference lines, cividis on a log2 MSA-depth scale, square panel.
- [Figure 2](https://github.com/delalamo/af2_conformations/blob/main/figures/fig2/fig2_script.R): faceted scatterplots with viridis pLDDT color, panel borders, and 5-point text.
- [Figure 3](https://github.com/delalamo/af2_conformations/blob/main/figures/fig3/fig3_script.R): densities above faceted scatterplots, orange/aquamarine conformational-state colors, cowplot alignment.

All use theme_minimal() plus local overrides. The Figure 2 and 3 comments also describe manual layout fixes; a reusable style guide should handle long facet titles and panel alignment in R.

Recommended next comparison: render identical scientific data in three original directions—light typographic, warm editorial, and dark editorial. Test each on scatter, faceted scatter, line/ribbon, histogram/density, violin/box, heatmap, point/interval, and a cowplot composite. The first, second, and last directly extend existing repository figures; the rest test breadth.

A recognizable personal style should fix typography, spacing, categorical color meaning, quantitative color scales, annotation treatment, and panel labels. My preferred starting point is hrbrthemes' typographic discipline plus Wilke's scientific recipes and BBC/Urban's consistent presentation conventions. Preserve quantitative meaning: a signature categorical palette does not need to replace useful sequential scales for pLDDT and MSA depth. Use one visual identity with separate manuscript and online export sizes.
