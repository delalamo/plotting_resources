library(ggplot2)
library(cowplot)

# Physical units, not scale factors. All widths include axes, legends and margins.
paper_tokens <- list(
  font="Helvetica", tick_pt=7.5, axis_pt=8, legend_pt=7.5, strip_pt=8,
  outer_pt=3, tick_length_pt=2, tick_label_gap_pt=2, axis_title_gap_pt=4,
  facet_gap_pt=8, gutter_in=.14, left_rail_in=.40, right_rail_in=.075,
  frame_mm=.18, grid_mm=.13, line_mm=.40, point_stroke_mm=.20,
  ink="#232B29", secondary="#55615D", frame="#74807A", grid="#E0E6E3",
  aqua="#38AE9F", orange="#E69B35", dark_aqua="#117C72"
)

panel_spec <- function(size, figure_width=6.5, family="standard") {
  columns <- c(compact=4, small=3, medium=2, large=1)[[size]]
  width <- (figure_width-(columns-1)*paper_tokens$gutter_in)/columns
  height <- c(compact=1.65, small=1.80, medium=2.05, large=2.65)[[size]]
  if (family=="facets") height <- c(compact=4.15,small=4.15,medium=2.60,large=3.00)[[size]]
  if (family=="composite") height <- c(compact=2.05,small=2.20,medium=2.55,large=3.15)[[size]]
  list(size=size, columns=columns, width=width, height=height,
       point=c(compact=.85,small=1.0,medium=1.2,large=1.4)[[size]],
       max_xticks=c(compact=3,small=4,medium=5,large=6)[[size]],
       max_yticks=c(compact=4,small=4,medium=5,large=6)[[size]])
}

paper_theme <- function(grid="y") {
  t <- paper_tokens
  theme_minimal(base_family=t$font,base_size=t$tick_pt) + theme(
    text=element_text(colour=t$ink,lineheight=1.05),
    plot.background=element_rect(fill="white",colour=NA),
    panel.background=element_rect(fill="white",colour=NA),
    plot.title=element_blank(),plot.subtitle=element_blank(),plot.caption=element_blank(),
    panel.border=element_rect(fill=NA,colour=t$frame,linewidth=t$frame_mm),
    panel.grid.minor=element_blank(),
    panel.grid.major.x=if(grepl("x",grid)) element_line(colour=t$grid,linewidth=t$grid_mm) else element_blank(),
    panel.grid.major.y=if(grepl("y",grid)) element_line(colour=t$grid,linewidth=t$grid_mm) else element_blank(),
    axis.title=element_text(size=t$axis_pt,face="bold"),
    axis.title.x=element_text(margin=margin(t=t$axis_title_gap_pt)),
    axis.title.y=element_text(margin=margin(r=t$axis_title_gap_pt)),
    axis.text=element_text(size=t$tick_pt,colour=t$ink),
    axis.text.x=element_text(margin=margin(t=t$tick_label_gap_pt)),
    axis.text.y=element_text(margin=margin(r=t$tick_label_gap_pt)),
    axis.ticks=element_line(colour=t$frame,linewidth=t$frame_mm),
    axis.ticks.length=unit(t$tick_length_pt,"pt"),
    legend.position="top",legend.justification="left",legend.direction="horizontal",
    legend.title=element_blank(),legend.text=element_text(size=t$legend_pt),
    legend.key=element_blank(),legend.background=element_blank(),
    legend.key.size=unit(8,"pt"),legend.key.spacing.x=unit(3,"pt"),
    legend.spacing.x=unit(3,"pt"),legend.margin=margin(0,0,3,0),
    legend.box.spacing=unit(1,"pt"),
    strip.background=element_blank(),
    strip.text=element_text(size=t$strip_pt,face="bold",hjust=0,margin=margin(b=3,t=2)),
    panel.spacing=unit(t$facet_gap_pt,"pt"),
    plot.margin=margin(t$outer_pt,t$outer_pt,t$outer_pt,t$outer_pt)
  )
}

state_scales <- function(aesthetics=c("fill","shape")) {
  cols <- c(A=paper_tokens$aqua,B=paper_tokens$orange)
  all <- list(fill=scale_fill_manual(values=cols,name=NULL),
    colour=scale_colour_manual(values=cols,name=NULL),
    shape=scale_shape_manual(values=c(A=21,B=24),name=NULL))
  unname(all[aesthetics])
}

physical_breaks <- function(limits,spec,axis="x") {
  usable <- if(axis=="x") spec$width-paper_tokens$left_rail_in-paper_tokens$right_rail_in else spec$height-.65
  # Reserve at least 0.40 in horizontally and 0.28 in vertically between ticks.
  step <- if(axis=="x") .40 else .28
  max_n <- if(axis=="x") spec$max_xticks else spec$max_yticks
  n <- max(2,min(max_n,floor(usable/step)+1))
  spans_zero <- limits[1]<0 && limits[2]>0
  if(spans_zero && n<=3) {
    magnitude <- min(abs(limits))
    power <- 10^floor(log10(magnitude))
    anchor <- floor(magnitude/power)*power
    return(c(-anchor,0,anchor))
  }
  for (target in n:(n+4)) {
    br <- scales::breaks_extended(n=target)(limits)
    br <- br[br>=limits[1]&br<=limits[2]]
    if(length(br)>=2 && (!spans_zero || (any(br<0) && any(br>0)))) break
  }
  if(axis=="x") {
    repeat {
      labels <- format(br,trim=TRUE,scientific=FALSE)
      widths <- vapply(labels,function(label) convertWidth(grobWidth(textGrob(label,
        gp=gpar(fontfamily=paper_tokens$font,fontsize=paper_tokens$tick_pt))),"in",valueOnly=TRUE),numeric(1))
      data_width <- spec$width-max(paper_tokens$left_rail_in,.48)-
        max(paper_tokens$right_rail_in,max(widths)/2+paper_tokens$outer_pt/72)
      gaps <- diff(br)/diff(limits)*data_width-(head(widths,-1)+tail(widths,-1))/2
      if(length(br)<=2 || all(gaps>=4/72)) break
      br <- br[unique(c(seq(1,length(br),by=2),length(br)))]
    }
  }
  br
}

confidence_scale <- function(spec) scale_fill_viridis_c(
  option="cividis",limits=c(50,100),name=NULL,breaks=c(50,75,100),
  guide=guide_colourbar(direction="horizontal",barwidth=unit(min(.95,spec$width-.50),"in"),
                        barheight=unit(3.5,"pt"),ticks=FALSE))

# Pad the entire axis assembly to a consistent rail. Never shrink text or clip it.
# Category labels longer than the rail expand it instead of overlapping the panel.
paper_grob <- function(plot) {
  g <- ggplotGrob(plot)
  panels <- grep("^panel",g$layout$name)
  if (!length(panels)) return(g)
  left <- min(g$layout$l[panels]); right <- max(g$layout$r[panels])
  current <- convertWidth(sum(g$widths[seq_len(left-1)]),"in",valueOnly=TRUE)
  delta <- max(0,paper_tokens$left_rail_in-current)
  g$widths[1] <- g$widths[1]+unit(delta,"in")
  current_r <- convertWidth(sum(g$widths[(right+1):length(g$widths)]),"in",valueOnly=TRUE)
  labels <- unlist(lapply(ggplot_build(plot)$layout$panel_params,function(p) p$x$get_labels()))
  labels <- labels[!is.na(labels)]
  label_width <- if(length(labels)) max(vapply(labels,function(label) {
    convertWidth(grobWidth(textGrob(label,gp=gpar(fontfamily=paper_tokens$font,
      fontsize=paper_tokens$tick_pt))),"in",valueOnly=TRUE)
  },numeric(1))) else 0
  # End labels are centered on ticks: reserve half a label plus the outer margin.
  right_target <- max(paper_tokens$right_rail_in,label_width/2+paper_tokens$outer_pt/72)
  g$widths[length(g$widths)] <- g$widths[length(g$widths)]+unit(max(0,right_target-current_r),"in")
  g
}
