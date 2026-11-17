.libPaths(c("/private/tmp/af2-r-lib", .libPaths()))

library(ggplot2)
library(cowplot)
library(viridis)

script_arg <- grep("^--file=", commandArgs(), value = TRUE)
script_dir <- dirname(normalizePath(sub("^--file=", "", script_arg[[1]])))
source(file.path(script_dir, "bbc_style.R"))

args <- commandArgs(trailingOnly = TRUE)
data_dir <- if (length(args) >= 1) args[[1]] else "."
out_dir <- if (length(args) >= 2) args[[2]] else data_dir
dir.create(out_dir, recursive = TRUE, showWarnings = FALSE)

ink <- "#222222"
muted <- "#6B6B6B"
grid_col <- "#CBCBCB"
teal <- "#007F7F"
orange <- "#FA6400"

theme_bbc_science <- function(base_size = 12, faceted = FALSE) {
  bbc_style() +
    theme(
      plot.title.position = "plot",
      plot.title = element_text(
        family = "Helvetica", face = "bold", size = base_size * 1.75,
        colour = ink, margin = margin(b = 3)
      ),
      plot.subtitle = element_text(
        family = "Helvetica", size = base_size * 1.15,
        colour = ink, margin = margin(t = 4, b = 10)
      ),
      plot.caption = element_blank(),
      axis.title = element_text(
        family = "Helvetica", face = "bold", size = base_size,
        colour = ink
      ),
      axis.title.x = element_text(margin = margin(t = 9)),
      axis.title.y = element_text(margin = margin(r = 9)),
      axis.text = element_text(
        family = "Helvetica", size = base_size * 0.85, colour = ink
      ),
      legend.text = element_text(
        family = "Helvetica", size = base_size * 0.9, colour = ink
      ),
      legend.title = element_text(
        family = "Helvetica", face = "bold", size = base_size * 0.9,
        colour = ink
      ),
      legend.position = "top",
      legend.justification = "left",
      strip.background = element_blank(),
      strip.text = element_text(
        family = "Helvetica", face = "bold",
        size = if (faceted) base_size else base_size * 1.1,
        hjust = 0, colour = ink, margin = margin(b = 5)
      ),
      panel.spacing = grid::unit(if (faceted) 12 else 8, "pt"),
      panel.grid.minor = element_blank(),
      panel.grid.major.y = element_line(colour = grid_col, linewidth = 0.35),
      panel.grid.major.x = element_blank(),
      plot.margin = margin(12, 16, 8, 12)
    )
}

source_footer <- function(text) {
  ggdraw() +
    draw_line(x = c(0, 1), y = c(0.93, 0.93), colour = ink, linewidth = 0.4) +
    draw_label(
      text, x = 0.005, y = 0.38, hjust = 0,
      fontfamily = "Helvetica", size = 9, colour = ink
    )
}

finish_plot <- function(plot, filename, width, height) {
  final <- plot_grid(
    plot,
    source_footer("Source: af2_conformations; del Alamo et al., eLife (2022)"),
    ncol = 1, rel_heights = c(1, 0.05)
  )
  ggsave(
    file.path(out_dir, filename), final,
    width = width, height = height, units = "in", dpi = 180,
    device = ragg::agg_png, bg = "white"
  )
}

# Figure 1 --------------------------------------------------------------------

f1 <- read.csv(file.path(data_dir, "fig1_data_models.csv"), check.names = FALSE)
lat1 <- f1[f1$protein == "Lat1", ]
lat1_median <- aggregate(cbind(tm_IF, tm_OF) ~ nseq, lat1, median)
lat1_median <- lat1_median[order(lat1_median$nseq), ]

p1 <- ggplot(lat1, aes(tm_IF, tm_OF)) +
  geom_hline(yintercept = 0.86337, colour = muted, linewidth = 0.45, linetype = 3) +
  geom_vline(xintercept = 0.86337, colour = muted, linewidth = 0.45, linetype = 3) +
  geom_point(aes(colour = log2(nseq)), size = 1.45, alpha = 0.58) +
  geom_point(
    data = lat1_median, aes(tm_IF, tm_OF, fill = log2(nseq)), inherit.aes = FALSE,
    colour = ink, shape = 21, stroke = 0.4, size = 2.8
  ) +
  annotate(
    "text", x = lat1_median$tm_IF[[1]] - 0.002,
    y = lat1_median$tm_OF[[1]] + 0.004,
    label = "16 sequences", hjust = 1, family = "Helvetica",
    size = 3.5, colour = ink
  ) +
  annotate(
    "text", x = lat1_median$tm_IF[[nrow(lat1_median)]] + 0.002,
    y = lat1_median$tm_OF[[nrow(lat1_median)]] - 0.003,
    label = "5,120 sequences", hjust = 0, vjust = 1,
    family = "Helvetica", size = 3.5, colour = teal
  ) +
  annotate(
    "text", x = 0.865, y = 0.866, label = "Reference threshold",
    hjust = 0, vjust = 1, family = "Helvetica", size = 3.1,
    colour = muted
  ) +
  scale_x_continuous(breaks = c(0.85, 0.90, 0.95, 1.00)) +
  scale_y_continuous(breaks = c(0.85, 0.90, 0.95, 1.00)) +
  scale_colour_viridis_c(
    name = "MSA depth", option = "C",
    breaks = log2(c(16, 128, 1024, 5120)),
    labels = c("16", "128", "1,024", "5,120"),
    guide = guide_colourbar(
      title.position = "top",
      barwidth = grid::unit(110, "pt"),
      barheight = grid::unit(7, "pt")
    )
  ) +
  scale_fill_viridis_c(
    option = "C", limits = range(log2(lat1$nseq)), guide = "none"
  ) +
  coord_equal(xlim = c(0.85, 1), ylim = c(0.85, 1), expand = FALSE, clip = "on") +
  labs(
    title = "Deeper MSAs favor inward-facing Lat1 models",
    subtitle = "Colour shows alignment depth; outlined points mark the median at each tested depth",
    x = "Similarity to inward-facing structure (TM-score)",
    y = "Similarity to outward-facing structure (TM-score)"
  ) +
  theme_bbc_science(base_size = 11) +
  theme(
    panel.grid.major.x = element_line(colour = grid_col, linewidth = 0.35),
    legend.key.width = grid::unit(28, "pt")
  )

finish_plot(p1, "af2-bbplot-skill-fig1.png", 8.6, 7.0)

# Figure 2 --------------------------------------------------------------------

f2 <- read.csv(file.path(data_dir, "fig2_data.csv"), check.names = FALSE)
protein_order <- c(
  "CGRPR", "FZD7", "PTH1R", "ASCT2", "Lat1", "STP10", "ZnT8",
  "MCT1 (without templates)", "MCT1 (with templates)"
)
f2$protein <- factor(f2$protein, levels = protein_order)

cor_labels <- do.call(rbind, lapply(split(f2, f2$protein), function(d) {
  data.frame(
    protein = factor(as.character(d$protein[[1]]), levels = protein_order),
    label = sprintf("r = %.2f", cor(d$exp_dist, d$sim_rmsf, use = "complete.obs"))
  )
}))

p2 <- ggplot(f2, aes(exp_dist, sim_rmsf)) +
  geom_smooth(
    method = "lm", formula = y ~ x, se = FALSE,
    colour = muted, linewidth = 0.45, linetype = 2
  ) +
  geom_point(aes(colour = avg_plddt), size = 1.15, alpha = 0.68) +
  geom_text(
    data = cor_labels,
    aes(x = -Inf, y = Inf, label = label), inherit.aes = FALSE,
    hjust = -0.12, vjust = 1.25, family = "Helvetica",
    fontface = "bold", size = 3.2, colour = ink
  ) +
  facet_wrap(~protein, ncol = 3, scales = "free") +
  scale_colour_viridis_c(
    name = "Average pLDDT", option = "C",
    limits = range(f2$avg_plddt, na.rm = TRUE)
  ) +
  scale_x_continuous(expand = expansion(mult = c(0.03, 0.06))) +
  scale_y_continuous(expand = expansion(mult = c(0.04, 0.10))) +
  labs(
    title = "ASCT2 and template-guided MCT1 track experimental motion best",
    subtitle = "Pearson correlation is shown in each panel; panel scales vary to preserve within-protein structure",
    x = "Experimental displacement (Å)",
    y = "Simulated flexibility (RMSF, Å)"
  ) +
  theme_bbc_science(base_size = 9.5, faceted = TRUE) +
  theme(
    legend.key.width = grid::unit(30, "pt"),
    legend.position = "top",
    plot.margin = margin(10, 14, 6, 10)
  )

finish_plot(p2, "af2-bbplot-skill-fig2.png", 12.0, 8.8)

# Figure 3 --------------------------------------------------------------------

f3 <- read.csv(file.path(data_dir, "fig3_data.csv"), check.names = FALSE)
protein_order3 <- c("CGRPR", "FZD7", "PTH1R", "ASCT2", "Lat1", "STP10", "ZnT8", "MCT1")
f3$protein <- factor(f3$protein, levels = protein_order3)
models3 <- f3[f3$type == "Model", ]
structures3 <- f3[f3$type == "Structure", ]

scores3 <- rbind(
  data.frame(
    protein = models3$protein, pc1 = models3$pc1,
    score = models3$TM_IF, state = "Inward-facing"
  ),
  data.frame(
    protein = models3$protein, pc1 = models3$pc1,
    score = models3$TM_OF, state = "Outward-facing"
  )
)
scores3$state <- factor(scores3$state, levels = c("Inward-facing", "Outward-facing"))

state_colours <- c("Inward-facing" = teal, "Outward-facing" = orange)
state_shapes <- c("Inward-facing" = 16, "Outward-facing" = 17)

make_density <- function(proteins) {
  d <- models3[models3$protein %in% proteins, ]
  s <- structures3[structures3$protein %in% proteins, ]
  d$protein <- factor(d$protein, levels = proteins)
  s$protein <- factor(s$protein, levels = proteins)

  ggplot(d, aes(pc1)) +
    geom_density(fill = "#D9D9D9", colour = muted, linewidth = 0.65, adjust = 0.85) +
    geom_vline(
      data = s, aes(xintercept = pc1), inherit.aes = FALSE,
      colour = ink, linewidth = 0.45, linetype = 3
    ) +
    facet_wrap(~protein, nrow = 1, scales = "free") +
    labs(x = NULL, y = NULL) +
    theme_bbc_science(base_size = 9.5, faceted = TRUE) +
    theme(
      axis.text = element_blank(), axis.title = element_blank(),
      panel.grid.major.y = element_blank(), panel.grid.major.x = element_blank(),
      panel.grid.minor = element_blank(),
      legend.position = "none",
      plot.margin = margin(2, 12, 0, 10)
    )
}

make_scatter <- function(proteins, show_x_title = FALSE) {
  d <- scores3[scores3$protein %in% proteins, ]
  s <- structures3[structures3$protein %in% proteins, ]
  d$protein <- factor(d$protein, levels = proteins)
  s$protein <- factor(s$protein, levels = proteins)

  ggplot(d, aes(pc1, score, colour = state, shape = state)) +
    geom_point(size = 1.05, alpha = 0.48) +
    geom_vline(
      data = s, aes(xintercept = pc1), inherit.aes = FALSE,
      colour = ink, linewidth = 0.45, linetype = 3
    ) +
    geom_point(
      data = s, aes(pc1, max_tm), inherit.aes = FALSE,
      shape = 23, size = 2.3, fill = ink, colour = "white", stroke = 0.45
    ) +
    facet_wrap(~protein, nrow = 1, scales = "free_x") +
    scale_colour_manual(values = state_colours) +
    scale_shape_manual(values = state_shapes) +
    scale_y_continuous(limits = c(0.55, 1.01), breaks = c(0.6, 0.8, 1.0)) +
    labs(
      x = if (show_x_title) "Principal component 1" else NULL,
      y = "Similarity to reference (TM-score)",
      colour = NULL, shape = NULL
    ) +
    theme_bbc_science(base_size = 9.5, faceted = TRUE) +
    theme(
      strip.text = element_blank(),
      legend.position = "top",
      legend.margin = margin(0, 0, 0, 0),
      plot.margin = margin(0, 12, 3, 10)
    )
}

top_proteins <- protein_order3[1:4]
bottom_proteins <- protein_order3[5:8]

density_top <- make_density(top_proteins)
density_bottom <- make_density(bottom_proteins)
scatter_top <- make_scatter(top_proteins, show_x_title = FALSE)
scatter_bottom <- make_scatter(bottom_proteins, show_x_title = TRUE)

legend3 <- get_legend(scatter_top + theme(legend.position = "top"))
scatter_top <- scatter_top + theme(legend.position = "none")
scatter_bottom <- scatter_bottom + theme(legend.position = "none")

pair_top <- plot_grid(
  density_top, scatter_top, ncol = 1, align = "v", axis = "lr",
  rel_heights = c(0.30, 1)
)
pair_bottom <- plot_grid(
  density_bottom, scatter_bottom, ncol = 1, align = "v", axis = "lr",
  rel_heights = c(0.30, 1)
)

header3 <- ggdraw() +
  draw_label(
    "Conformational coverage differs sharply across proteins",
    x = 0, y = 0.76, hjust = 0, fontfamily = "Helvetica",
    fontface = "bold", size = 20, colour = ink
  ) +
  draw_label(
    "PC1 density above; similarity to inward- and outward-facing references below; dotted lines mark experimental structures",
    x = 0, y = 0.23, hjust = 0, fontfamily = "Helvetica",
    size = 12, colour = ink
  )

body3 <- plot_grid(
  header3, legend3, pair_top, pair_bottom,
  ncol = 1, rel_heights = c(0.12, 0.07, 1, 1)
)

finish_plot(body3, "af2-bbplot-skill-fig3.png", 12.0, 9.8)

cat("Rendered AF2 examples with bbplot-data-viz\n")
