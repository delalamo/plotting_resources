# ggplot2 and cowplot implementation

Use this reference when creating R charts with the `bbplot-data-viz` skill.

## Packages

```r
library(ggplot2)
library(cowplot)
library(bbplot)
```

If `bbplot` is unavailable, source the official `R/bbc_style.R` file from a checked-out copy of `bbc/bbplot`. Do not silently replace it with `theme_minimal()`.

## Scientific wrapper

Add this wrapper after `bbc_style()` to scale the original news theme for scientific figures while preserving its structure.

```r
theme_bbc_science <- function(base_size = 12, faceted = FALSE) {
  bbc_style() +
    theme(
      plot.title.position = "plot",
      plot.title = element_text(
        family = "Helvetica", face = "bold",
        size = base_size * 1.75, colour = "#222222",
        margin = margin(b = 3)
      ),
      plot.subtitle = element_text(
        family = "Helvetica", size = base_size * 1.15,
        colour = "#222222", margin = margin(t = 4, b = 10)
      ),
      axis.title = element_text(
        family = "Helvetica", face = "bold",
        size = base_size, colour = "#222222"
      ),
      axis.text = element_text(
        family = "Helvetica", size = base_size * 0.85,
        colour = "#222222"
      ),
      legend.text = element_text(
        family = "Helvetica", size = base_size * 0.9,
        colour = "#222222"
      ),
      strip.background = element_blank(),
      strip.text = element_text(
        family = "Helvetica", face = "bold",
        size = if (faceted) base_size else base_size * 1.1,
        hjust = 0, colour = "#222222"
      ),
      panel.spacing = grid::unit(if (faceted) 12 else 8, "pt"),
      plot.margin = margin(12, 16, 8, 12)
    )
}
```

For dense 3-by-3 facets, start with `base_size = 10`. For a single 900-by-600 chart, start with `base_size = 12`.

## Palettes

```r
bbc_states <- c(
  "Inward-facing" = "#007F7F",
  "Outward-facing" = "#FA6400"
)

bbc_categories <- c("#1380A1", "#F4A338", "#A95CE4", "#5A7834")
bbc_neutral <- "#6B6B6B"
bbc_grid <- "#CBCBCB"
```

Use `scale_colour_viridis_c()` or `scale_fill_viridis_c()` for ordered scientific values. Keep the same palette limits across comparable panels.

## Small multiples

```r
ggplot(data, aes(x, y)) +
  geom_point(size = 1.2, alpha = 0.65, colour = "#007F7F") +
  facet_wrap(~protein, ncol = 3, scales = "free") +
  labs(subtitle = "Panel scales vary to preserve within-protein structure") +
  theme_bbc_science(base_size = 10, faceted = TRUE)
```

Keep factor levels explicit before plotting so panel order does not change between figures.

## Density plus scatter

Build one density plot and one scatter plot with identical factor order, x limits, and facet layout. Remove the density x-axis and scatter strip labels, then combine:

```r
plot_grid(
  density_plot, scatter_plot,
  ncol = 1, align = "v", axis = "lr",
  rel_heights = c(0.28, 1)
)
```

For more than four facets, build two aligned blocks of four rather than eight unreadably narrow columns.

## Footer and export

```r
source_footer <- function(text) {
  ggdraw() +
    draw_line(x = c(0, 1), y = c(0.93, 0.93), colour = "#222222", linewidth = 0.4) +
    draw_label(text, x = 0.005, y = 0.4, hjust = 0,
               fontfamily = "Helvetica", size = 9, colour = "#222222")
}

final <- plot_grid(
  plot,
  source_footer("Source: ..."),
  ncol = 1,
  rel_heights = c(1, 0.055)
)

ggsave(
  "chart.png", final,
  width = 9, height = 6, units = "in", dpi = 180,
  bg = "white"
)
```

Inspect the exported file for clipping, rasterization, legend wrapping, and unreadable facets.
