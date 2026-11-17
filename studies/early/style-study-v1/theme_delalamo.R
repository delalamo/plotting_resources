# Style study v1: af2_conformations geometry + selected BBC presentation rules.
# The foundation deliberately remains theme_minimal(); panel frames and outlined
# scientific marks preserve the original figures rather than the BBC defaults.
library(ggplot2)
source(file.path("bbplot-data-viz", "scripts", "bbc_style.R"))

style <- list(
  ink = "#242B2A", muted = "#626D6A", grid = "#E1E7E5", frame = "#77817E",
  teal = "#37B6A6", orange = "#EDA13A", teal_dark = "#087F76",
  paper = "#FFFFFF", font = "Helvetica"
)
state_colours <- c("State A" = style$teal, "State B" = style$orange)
state_shapes <- c("State A" = 21, "State B" = 24)

theme_delalamo <- function(grid = "y", base_size = 11) {
  theme_minimal(base_size = base_size, base_family = style$font) +
    bbc_style() +
    theme(
      text = element_text(family = style$font, colour = style$ink),
      plot.background = element_rect(fill = style$paper, colour = NA),
      panel.background = element_rect(fill = style$paper, colour = NA),
      panel.border = element_rect(fill = NA, colour = style$frame, linewidth = .35),
      plot.title.position = "plot",
      plot.title = element_text(size = 18, face = "bold", hjust = 0,
                                margin = margin(b = 5), colour = style$ink),
      plot.subtitle = element_text(size = 10.8, hjust = 0, colour = style$muted,
                                   margin = margin(b = 12)),
      axis.title = element_text(size = 10.5, face = "bold", colour = style$ink),
      axis.title.x = element_text(margin = margin(t = 9)),
      axis.title.y = element_text(margin = margin(r = 9)),
      axis.text = element_text(size = 9.5, colour = style$ink),
      axis.text.x = element_text(margin = margin(t = 5, b = 0)),
      axis.text.y = element_text(margin = margin(r = 4)),
      axis.ticks = element_blank(), axis.line = element_blank(),
      panel.grid.minor = element_blank(),
      panel.grid.major.x = if (grepl("x", grid)) element_line(colour = style$grid, linewidth = .3) else element_blank(),
      panel.grid.major.y = if (grepl("y", grid)) element_line(colour = style$grid, linewidth = .3) else element_blank(),
      legend.position = "top", legend.justification = "left",
      legend.title = element_text(size = 9.5, face = "bold"),
      legend.text = element_text(size = 9.5),
      legend.key.size = grid::unit(12, "pt"),
      legend.margin = margin(0, 0, 5, 0),
      legend.box.spacing = grid::unit(2, "pt"),
      strip.text = element_text(size = 10, face = "bold", hjust = 0,
                                margin = margin(b = 6, t = 5)),
      strip.background = element_blank(), panel.spacing = grid::unit(12, "pt"),
      plot.margin = margin(15, 20, 14, 16), plot.caption = element_blank()
    )
}

state_scales <- function(aesthetics = c("fill", "colour", "shape")) {
  scales <- list(
    fill = scale_fill_manual(values = state_colours, name = NULL),
    colour = scale_colour_manual(values = state_colours, name = NULL),
    shape = scale_shape_manual(values = state_shapes, name = NULL)
  )
  unname(scales[aesthetics])
}
