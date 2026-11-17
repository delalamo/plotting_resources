local_lib <- Sys.getenv("PLOT_GALLERY_R_LIB","/private/tmp/plot-gallery-r-lib")
if(dir.exists(local_lib)) .libPaths(c(local_lib,.libPaths()))
options(device=function(...) grDevices::pdf(file=tempfile(fileext=".pdf"),...))
library(grid)
library(ggplot2)
library(cowplot)
source("style-study-v2/paper_theme.R")
t <- paper_tokens
args <- commandArgs(trailingOnly=TRUE)
figure_width <- if(length(args)) as.numeric(args[1]) else 6.5
out <- file.path("style-study-v2",if(figure_width==5.5) "neurips-5.5in" else "requested-6.5in")
dir.create(file.path(out,"panels"),recursive=TRUE,showWarnings=FALSE)
dir.create(file.path(out,"proofs"),recursive=TRUE,showWarnings=FALSE)
read_data <- function(name) {
  d <- read.csv(file.path("style-study-v1","data",paste0(name,".csv")))
  if("state" %in% names(d)) d$state <- factor(sub("State ","",d$state),levels=c("A","B"))
  if("condition" %in% names(d)) d$condition <- factor(d$condition,levels=c("Low","Medium","High"),labels=c("Low","Med","High"))
  d
}
scatter <- read_data("scatter"); line <- read_data("trajectory_summary")
paired <- read_data("paired"); paired$sample <- factor(sub("Sample ","S",paired$sample),levels=paste0("S",6:1))
pairs <- reshape(paired,idvar="sample",timevar="state",direction="wide")
effects <- read_data("effects_summary"); effects$variant <- factor(sub("Variant ","",effects$variant),levels=rev(LETTERS[1:6]))
dist <- read_data("distributions"); medium <- subset(dist,condition=="Med")
bar <- aggregate(score~condition+state,dist,mean); bar$score <- bar$score*100
heat <- read_data("heatmap"); heat$sample <- factor(sub("Model ","M",heat$sample),levels=paste0("M",6:1))
facets <- read_data("facets"); facets$protein <- sub("Protein ","",facets$protein)
pc <- read_data("composite")

titles <- c(A="Scatterplot",B="Line and uncertainty",C="Paired comparison",D="Point and interval",
 E="Boxplot and observations",F="Violin plot",G="Histogram",H="Density plot",
 I="Grouped bars",J="Heatmap",K="Small multiples",L="Density and scatter")
notes <- c(
 A="Same limits on both axes. Reference line means y = x; preserve it at every size.",
 B="Mean and pointwise 95% CI. Keep the ribbon; reduce marker frequency before shrinking text.",
 C="Matched endpoints stay connected. Short sample IDs reserve width for the comparison.",
 D="Mean and 95% CI. Keep the zero reference and all interval endpoints at every size.",
 E="All observations remain visible. L/M/H abbreviate Low/Medium/High in compact panels.",
 F="White dots mark group medians. L/M/H abbreviate Low/Medium/High in compact panels.",
 G="Use the same 0.035 bin width at every size. Tick density changes, the distribution does not.",
 H="Common bandwidth 0.035. Keep identical limits and smoothing across sizes.",
 I="Bars start at zero. Compact labels use L/M/H for Low/Medium/High; wider panels add values.",
 J="Confidence scale: 50-100. Keep all cells; reduce tick labels, never coarsen the data.",
 K="Four shared-scale facets. Narrow panels reflow to one column instead of shrinking type.",
 L="Shared x-axis. Hide repeated density ticks; give the scatter panel most of the height."
)

build_plot <- function(id,s) {
  common_points <- function(mapping,size=s$point,alpha=.72,data=NULL) geom_point(mapping=mapping,
    data=data,size=size,stroke=t$point_stroke_mm,colour=t$ink,alpha=alpha)
  xscale <- function(lim) scale_x_continuous(limits=lim,breaks=physical_breaks(lim,s),expand=expansion(mult=.025))
  yscale <- function(lim) scale_y_continuous(limits=lim,breaks=physical_breaks(lim,s,"y"),expand=expansion(mult=.025))
  p <- switch(id,
   A=ggplot(scatter,aes(x,y))+geom_abline(slope=1,intercept=0,colour=t$secondary,linetype=3,linewidth=.25)+
     common_points(aes(fill=state,shape=state))+state_scales()+xscale(c(.68,1.01))+yscale(c(.68,1.01))+
     labs(x="Reference (a.u.)",y="Model (a.u.)")+paper_theme("xy"),
   B=ggplot(line,aes(step,mean,colour=state))+geom_ribbon(aes(ymin=lo,ymax=hi,fill=state),alpha=.19,colour=NA)+
     geom_line(linewidth=t$line_mm)+common_points(aes(fill=state,shape=state),data=subset(line,step%%25==0),alpha=1)+
     state_scales(c("fill","colour","shape"))+xscale(c(0,100))+yscale(c(10,90))+
     labs(x="Step",y="Response (a.u.)")+paper_theme(),
   C=ggplot(pairs,aes(y=sample))+geom_segment(aes(x=value.A,xend=value.B,yend=sample),colour="#AFBAB5",linewidth=.65)+
     common_points(aes(x=value,fill=state,shape=state),data=paired,size=s$point+.30,alpha=1)+
     state_scales()+xscale(c(.45,.95))+labs(x="Similarity",y=NULL)+paper_theme("x"),
   D=ggplot(effects,aes(mean,variant))+geom_vline(xintercept=0,colour=t$secondary,linetype=3,linewidth=.25)+
     geom_errorbar(aes(xmin=lo,xmax=hi),orientation="y",width=.12,colour=t$dark_aqua,linewidth=.35)+
     geom_point(shape=21,size=s$point+.20,fill=t$aqua,colour=t$ink,stroke=t$point_stroke_mm)+
     xscale(c(-.40,.50))+labs(x="Difference (a.u.)",y="Variant")+paper_theme("x"),
   E=ggplot(dist,aes(condition,score,fill=state))+geom_boxplot(position=position_dodge(.74),width=.59,
     colour=t$ink,linewidth=.27,alpha=.60,outlier.shape=NA)+
     common_points(aes(shape=state),size=s$point*.55,alpha=.40)+state_scales()+
     yscale(c(.3,1))+labs(x="Sampling level",y="Similarity")+paper_theme(),
   F=ggplot(dist,aes(condition,score,fill=state))+geom_violin(position=position_dodge(.78),width=.76,
      colour=t$ink,linewidth=.27,alpha=.62,trim=TRUE)+
     stat_summary(aes(group=interaction(condition,state)),fun=median,geom="point",position=position_dodge(.78),
      shape=21,size=s$point*.75,fill="white",colour=t$ink,stroke=.20)+state_scales("fill")+
     yscale(c(.3,1))+labs(x="Sampling level",y="Similarity")+paper_theme(),
   G=ggplot(subset(dist,state=="A"),aes(score))+geom_histogram(binwidth=.035,boundary=.3,
      fill=t$aqua,colour="white",linewidth=.20)+xscale(c(.3,1))+
     scale_y_continuous(limits=c(0,23),breaks=physical_breaks(c(0,23),s,"y"),expand=c(0,0))+
     labs(x="Similarity",y="Count")+paper_theme(),
   H=ggplot(medium,aes(score,fill=state,colour=state))+geom_density(bw=.035,linewidth=t$line_mm,alpha=.23)+
     state_scales(c("fill","colour"))+xscale(c(.3,1))+
     scale_y_continuous(limits=c(0,7.5),breaks=physical_breaks(c(0,7.5),s,"y"),expand=c(0,0))+
     labs(x="Similarity",y="Density")+paper_theme(),
   I=ggplot(bar,aes(condition,score,fill=state))+geom_col(position=position_dodge(.74),width=.60)+state_scales("fill")+
     scale_y_continuous(limits=c(0,100),breaks=physical_breaks(c(0,100),s,"y"),expand=c(0,0))+
     labs(x="Sampling level",y="Mean score")+paper_theme(),
   J=ggplot(heat,aes(residue,sample,fill=confidence))+geom_tile(colour="white",linewidth=.30)+confidence_scale(s)+
     scale_x_continuous(breaks=if(s$size%in%c("compact","small"))c(1,6,12) else c(1,3,6,9,12),expand=c(0,0))+
     scale_y_discrete(expand=c(0,0))+labs(x="Residue block",y=NULL)+paper_theme("")+
     theme(axis.ticks=element_blank(),panel.border=element_blank()),
   K=ggplot(facets,aes(x,y))+geom_point(aes(fill=confidence),shape=21,size=s$point*.75,colour=t$ink,stroke=.12,alpha=.85)+
     confidence_scale(s)+facet_wrap(~protein,ncol=if(s$size%in%c("compact","small"))1 else 2)+
     scale_x_continuous(limits=c(0,10),breaks=if(s$size=="large")c(0,5,10) else c(0,10))+
     scale_y_continuous(limits=c(0,9),breaks=c(0,4,8))+
     labs(x="Reference (a.u.)",y="Model (a.u.)")+paper_theme("xy")+
     theme(panel.spacing=unit(6,"pt")),
   L=NULL)
  if(id %in% c("E","F","I") && s$width<1.6) p <- p+
    scale_x_discrete(labels=c(Low="L",Med="M",High="H"))
  if(id=="E") {
    # Explicit dodge/jitter uses exactly the same state grouping as the boxes.
    p$layers[[2]]$position <- position_jitterdodge(jitter.width=.12,dodge.width=.74,seed=1)
  }
  if(id=="I" && s$size%in%c("medium","large")) p <- p+
    geom_text(aes(label=round(score)),position=position_dodge(.74),vjust=-.45,
      family=t$font,size=7.5/.pt,colour=t$ink)
  if(id!="L") return(paper_grob(p))

  upper <- ggplot(pc,aes(pc1,fill=state,colour=state))+geom_density(bw=.4,linewidth=.30,alpha=.20)+
    state_scales(c("fill","colour"))+xscale(c(-4,4))+paper_theme("")+
    labs(x=NULL,y=NULL)+theme(axis.text.x=element_blank(),axis.text.y=element_blank(),
      axis.ticks=element_blank(),panel.border=element_blank(),legend.position="none",
      plot.margin=margin(0,3,0,3))
  lower <- ggplot(pc,aes(pc1,similarity))+common_points(aes(fill=state,shape=state),alpha=.68)+
    state_scales()+xscale(c(-4,4))+yscale(c(.78,.96))+labs(x="PC1 (a.u.)",y="Similarity")+paper_theme()+
    theme(legend.position="none",plot.margin=margin(0,3,3,3))
  aligned <- align_plots(paper_grob(upper),paper_grob(lower),align="v",axis="lr")
  # One physical key, aligned with the common panel start.
  key <- ggdraw()+annotate("point",x=.08,y=.5,shape=21,fill=t$aqua,colour=t$ink,size=1,stroke=.2)+
    draw_label("A",x=.18,y=.5,hjust=0,fontfamily=t$font,size=t$legend_pt)+
    annotate("point",x=.43,y=.5,shape=24,fill=t$orange,colour=t$ink,size=1,stroke=.2)+
    draw_label("B",x=.53,y=.5,hjust=0,fontfamily=t$font,size=t$legend_pt)
  body <- plot_grid(plotlist=aligned,ncol=1,rel_heights=c(.24,.76))
  ggdraw()+draw_plot(key,x=t$left_rail_in/s$width,y=1-.17/s$height,width=.62/s$width,height=.17/s$height)+
    draw_plot(body,x=0,y=0,width=1,height=1-.17/s$height)
}

draw_object <- function(obj) if(inherits(obj,"grob")) grid.draw(obj) else print(obj)
save_object <- function(obj,path,w,h) {
  if (Sys.info()[["sysname"]]=="Darwin") {
    grDevices::quartz(type="pdf",file=paste0(path,".pdf"),width=w,height=h,family=t$font)
  } else {
    grDevices::cairo_pdf(paste0(path,".pdf"),width=w,height=h,family=t$font,onefile=FALSE)
  }
  draw_object(obj); dev.off()
  ragg::agg_png(paste0(path,".png"),width=w,height=h,units="in",res=300,background="white")
  draw_object(obj); dev.off()
}

manifest <- list()
for(id in names(titles)) {
  family <- if(id=="K") "facets" else if(id=="L") "composite" else "standard"
  specs <- lapply(c("small","compact","medium","large"),panel_spec,figure_width=figure_width,family=family)
  names(specs) <- c("small","compact","medium","large")
  # Build within a real device so fixed-width text measurements are physical.
  ragg::agg_png(tempfile(fileext=".png"),width=figure_width,height=9,units="in",res=72)
  objs <- lapply(specs,function(s) build_plot(id,s))
  dev.off()
  for(size in names(specs)) {
    s <- specs[[size]]
    save_object(objs[[size]],file.path(out,"panels",paste(id,size,sep="-")),s$width,s$height)
    manifest[[length(manifest)+1]] <- data.frame(id=id,type=titles[[id]],size=size,
      figure_width_in=figure_width,panel_width_in=s$width,panel_height_in=s$height,
      columns=s$columns,gutter_in=t$gutter_in,tick_pt=t$tick_pt,axis_pt=t$axis_pt)
  }
  # Proof sheets place finished grobs at their actual physical sizes.
  # Their headers/notes are review apparatus, not part of the manuscript assets.
  top_h <- max(specs$small$height,specs$compact$height)
  mid_h <- specs$medium$height; large_h <- specs$large$height
  page_h <- .65 + .22+top_h + .26+.22+mid_h + .26+.22+large_h + .31
  proof <- ggdraw()
  text_at <- function(label,x,y,size=7.5,face="plain",colour=t$secondary) {
    draw_label(label,x=x/figure_width,y=1-y/page_h,hjust=0,vjust=1,
      fontfamily=t$font,size=size,fontface=face,colour=colour,lineheight=1.15)
  }
  proof <- proof+text_at(paste(id,titles[[id]],sep="  "),.04,.04,13,"bold",t$ink)+
    text_at(sprintf("Size study v2  |  %.1f-inch figure budget  |  Synthetic data",figure_width),.04,.29,7.5)
  y <- .65
  sx <- 0; cx <- specs$small$width+.22
  proof <- proof+text_at(sprintf("SMALL  /  3 across  /  %.2f in",specs$small$width),sx+.04,y,7,"bold")+
    text_at(sprintf("COMPACT  /  4 across  /  %.2f in",specs$compact$width),cx+.04,y,7,"bold")
  y <- y+.22
  proof <- proof+draw_plot(objs$small,x=0,y=1-(y+specs$small$height)/page_h,
    width=specs$small$width/figure_width,height=specs$small$height/page_h)+
    draw_plot(objs$compact,x=cx/figure_width,y=1-(y+specs$compact$height)/page_h,
    width=specs$compact$width/figure_width,height=specs$compact$height/page_h)
  nx <- cx+specs$compact$width+.15
  if(figure_width-nx > .95) proof <- proof+
    text_at("FIXED TYPE",nx,y+.07,7,"bold")+
    text_at("Ticks  7.5 pt\nAxes  8 pt\nKey  7.5 pt",nx,y+.25,7.5)+
    text_at("Labels stay legible.\nTick count adapts.",nx,y+.85,7)
  y <- y+top_h+.26
  proof <- proof+text_at(sprintf("MEDIUM  /  2 across  /  %.2f in",specs$medium$width),.04,y,7,"bold")
  y <- y+.22
  proof <- proof+draw_plot(objs$medium,x=0,y=1-(y+mid_h)/page_h,
    width=specs$medium$width/figure_width,height=mid_h/page_h)
  nx <- specs$medium$width+.25
  wrapped <- paste(strwrap(notes[[id]],width=if(figure_width==5.5) 32 else 42),collapse="\n")
  proof <- proof+text_at("LAYOUT RULE",nx,y+.18,7,"bold")+
    text_at(wrapped,nx,y+.40,8)+
    text_at("3 pt outer margin\n2 pt ticks + 2 pt label gap\n4 pt axis-title gap\n0.14 in between figure panels",nx,y+1.04,7.5)
  y <- y+mid_h+.26
  proof <- proof+text_at(sprintf("LARGE  /  1 across  /  %.2f in",specs$large$width),.04,y,7,"bold")
  y <- y+.22
  proof <- proof+draw_plot(objs$large,x=0,y=1-(y+large_h)/page_h,width=1,height=large_h/page_h)
  proof <- proof+text_at("All widths include axis titles and legends. View the PDF at 100% for physical sizing.",.04,page_h-.16,6.5)
  save_object(proof,file.path(out,"proofs",paste0(id,"-sizes")),figure_width,page_h)
  cat(id,"rendered\n")
}
write.csv(do.call(rbind,manifest),file.path(out,"dimensions.csv"),row.names=FALSE)
writeLines(capture.output(sessionInfo()),file.path(out,"session-info.txt"))
