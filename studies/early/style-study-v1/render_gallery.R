# Run from the plotting_resources project root:
# Rscript style-study-v1/render_gallery.R
local_lib <- Sys.getenv("PLOT_GALLERY_R_LIB", "/private/tmp/plot-gallery-r-lib")
if (dir.exists(local_lib)) .libPaths(c(local_lib, .libPaths()))
library(ggplot2)
library(cowplot)
source("style-study-v1/theme_delalamo.R")
set.seed(75751)
out <- "style-study-v1"
dir.create(file.path(out, "charts"), showWarnings = FALSE, recursive = TRUE)
dir.create(file.path(out, "data"), showWarnings = FALSE)

# All observations are synthetic; no biological findings are implied.
n <- 120
scatter <- data.frame(state = rep(c("State A", "State B"), each = n),
                      x = runif(2*n, .70, .99))
scatter$y <- pmin(.995, .25 + .67 * scatter$x +
                   ifelse(scatter$state == "State B", .055, 0) + rnorm(2*n, 0, .025))

raw_line <- expand.grid(step = seq(0, 100, by = 5), replicate = 1:24,
                        state = c("State A", "State B"))
raw_line$response <- with(raw_line, 18 +
  ifelse(state == "State A", 61, 43) * (1-exp(-step/31)) + rnorm(nrow(raw_line), 0, 7))
line <- aggregate(response ~ step + state, raw_line,
                  function(x) c(mean = mean(x), se = sd(x)/sqrt(length(x))))
line <- data.frame(line[1:2], mean = line$response[, "mean"], se = line$response[, "se"])
line$lo <- line$mean - qt(.975, 23)*line$se
line$hi <- line$mean + qt(.975, 23)*line$se

pairs <- data.frame(sample = factor(paste0("Sample ", 1:6), levels = paste0("Sample ", 6:1)),
                    a = c(.51, .58, .66, .69, .77, .81),
                    b = c(.72, .65, .80, .82, .88, .90))
pair_long <- rbind(data.frame(sample = pairs$sample, value = pairs$a, state = "State A"),
                   data.frame(sample = pairs$sample, value = pairs$b, state = "State B"))

effects_raw <- do.call(rbind, lapply(1:6, function(i)
  data.frame(variant = paste0("Variant ", LETTERS[i]), value = rnorm(30, (i-3)*.12, .23))))
effects <- do.call(rbind, lapply(split(effects_raw, effects_raw$variant), function(d)
  data.frame(variant = d$variant[1], mean = mean(d$value),
             se = sd(d$value)/sqrt(nrow(d)), n = nrow(d))))
effects$lo <- effects$mean-qt(.975,effects$n-1)*effects$se
effects$hi <- effects$mean+qt(.975,effects$n-1)*effects$se
effects$variant <- factor(effects$variant, levels = rev(effects$variant))

dist <- expand.grid(state = c("State A", "State B"), condition = c("Low", "Medium", "High"), replicate = 1:55)
dist$condition <- factor(dist$condition, levels = c("Low", "Medium", "High"))
dist$score <- with(dist, pmin(.999, pmax(.3, .44 + as.numeric(condition)*.10 +
  ifelse(state == "State B", .07, 0) + rnorm(nrow(dist), 0, .065))))
medium <- subset(dist, condition == "Medium")

bar <- aggregate(score ~ state + condition, dist, mean)
bar$percent <- 100 * bar$score
heat <- expand.grid(residue = 1:12, sample = factor(paste0("Model ", 1:6), levels = paste0("Model ", 6:1)))
heat$confidence <- pmax(50, pmin(100, 64 + 23*sin(heat$residue/5) +
                           5*cos(as.numeric(heat$sample)) + rnorm(nrow(heat),0,5)))
facets <- do.call(rbind, lapply(1:4, function(i) {
  x <- runif(70, 0, 10)
  data.frame(protein = paste0("Protein ", LETTERS[i]), x = x,
              y = pmax(0, .4 + (.35+i*.09)*x+rnorm(70,0,.6)), confidence = runif(70,50,100))
}))
pc <- data.frame(state = rep(c("State A", "State B"), each = 130),
                  pc1 = c(rnorm(130,-1.2,.8), rnorm(130,1.1,.8)))
pc$similarity <- pmin(.995, .79 + .13*plogis(ifelse(pc$state == "State A", -pc$pc1, pc$pc1)) + rnorm(nrow(pc),0,.018))

datasets <- list(scatter = scatter, trajectory_observations = raw_line,
  trajectory_summary = line, paired = pair_long, effects_observations = effects_raw,
  effects_summary = effects, distributions = dist, heatmap = heat, facets = facets, composite = pc)
for (nm in names(datasets)) write.csv(datasets[[nm]], file.path(out,"data",paste0(nm,".csv")),row.names=FALSE)

plots <- list()
plots$A <- ggplot(scatter,aes(x,y)) +
  geom_abline(slope=1,intercept=0,colour=style$muted,linetype=3,linewidth=.45) +
  geom_point(aes(fill=state,shape=state),colour=style$ink,stroke=.28,size=2.3,alpha=.73) +
  state_scales(c("fill","shape")) + coord_fixed(xlim=c(.68,1.01),ylim=c(.68,1.01)) +
  annotate("text",x=.705,y=.98,label="Dotted line: equal similarity",hjust=0,size=3.1,colour=style$muted,family=style$font) +
  labs(title="A  Scatterplot",subtitle="Outlined points retain your original figure style",
       x="Reference similarity (a.u.)",y="Model similarity (a.u.)") + theme_delalamo("xy")

plots$B <- ggplot(line,aes(step,mean,colour=state)) +
  geom_ribbon(aes(ymin=lo,ymax=hi,fill=state),colour=NA,alpha=.18) +
  geom_line(linewidth=.85) +
  geom_point(data=subset(line,step %% 20 == 0),aes(fill=state,shape=state),colour=style$ink,stroke=.25,size=2.3) +
  state_scales() + scale_x_continuous(breaks=seq(0,100,25)) +
  labs(title="B  Line + uncertainty",subtitle="Mean and 95% confidence interval; 24 replicates",
       x="Simulation step",y="Response (a.u.)") + theme_delalamo()

plots$C <- ggplot(pairs,aes(y=sample)) +
  geom_segment(aes(x=a,xend=b,yend=sample),colour="#BEC7C4",linewidth=1.2) +
  geom_point(data=pair_long,aes(x=value,fill=state,shape=state),size=3.3,colour=style$ink,stroke=.35) +
  state_scales(c("fill","shape")) + scale_x_continuous(limits=c(.45,.95),breaks=seq(.5,.9,.1)) +
  labs(title="C  Paired comparison",subtitle="Connect matched observations across two states",
       x="Similarity score (a.u.)",y=NULL) + theme_delalamo("x")

plots$D <- ggplot(effects,aes(mean,variant)) +
  geom_vline(xintercept=0,linetype=3,linewidth=.5,colour=style$muted) +
  geom_errorbar(aes(xmin=lo,xmax=hi),orientation="y",width=.14,colour=style$teal_dark,linewidth=.65) +
  geom_point(shape=21,size=3.2,fill=style$teal,colour=style$ink,stroke=.35) +
  labs(title="D  Point + interval",subtitle="Mean difference and 95% CI; 30 observations per variant",
       x="Difference from reference (a.u.)",y=NULL) + theme_delalamo("x")

plots$E <- ggplot(dist,aes(condition,score,fill=state)) +
  geom_boxplot(width=.60,position=position_dodge(.72),outlier.shape=NA,colour=style$ink,linewidth=.4,alpha=.65) +
  geom_point(aes(shape=state),position=position_jitterdodge(jitter.width=.16,dodge.width=.72,seed=1),
               colour=style$ink,size=1.25,stroke=.15,alpha=.43) +
  state_scales(c("fill","shape")) + scale_y_continuous(limits=c(.3,1),breaks=seq(.4,1,.2)) +
  labs(title="E  Boxplot + observations",subtitle="Median, IQR and 1.5×IQR whiskers; all observations shown",
       x="Sampling level",y="Similarity score (a.u.)") + theme_delalamo()

plots$F <- ggplot(dist,aes(condition,score,fill=state)) +
  geom_violin(position=position_dodge(.78),width=.75,colour=style$ink,linewidth=.38,alpha=.60,trim=TRUE) +
  stat_summary(aes(group=interaction(condition,state)),fun=median,geom="point",position=position_dodge(.78),shape=21,fill="white",colour=style$ink,size=2,stroke=.4) +
  state_scales("fill") + scale_y_continuous(limits=c(.3,1),breaks=seq(.4,1,.2)) +
  labs(title="F  Violin plot",subtitle="Distribution shapes; white dots mark medians",
       x="Sampling level",y="Similarity score (a.u.)") + theme_delalamo()

plots$G <- ggplot(subset(dist,state=="State A"),aes(score)) +
  geom_histogram(binwidth=.035,boundary=.3,fill=style$teal,colour="white",linewidth=.4) +
  scale_x_continuous(limits=c(.3,1),breaks=seq(.4,1,.2)) +
  scale_y_continuous(expand=expansion(mult=c(0,.08))) +
  labs(title="G  Histogram",subtitle="State A pooled across sampling levels; bin width 0.035",
       x="Similarity score (a.u.)",y="Observations") + theme_delalamo()

plots$H <- ggplot(medium,aes(score,fill=state,colour=state)) +
  geom_density(alpha=.24,linewidth=.8,bw=.035) + state_scales(c("fill","colour")) +
  scale_x_continuous(limits=c(.3,1),breaks=seq(.4,1,.2)) +
  scale_y_continuous(expand=expansion(mult=c(0,.08))) +
  labs(title="H  Density plot",subtitle="Medium sampling level; common bandwidth 0.035",
       x="Similarity score (a.u.)",y="Density") + theme_delalamo("")

plots$I <- ggplot(bar,aes(condition,percent,fill=state)) +
  geom_col(position=position_dodge(.72),width=.58) +
  geom_text(aes(label=sprintf("%.0f",percent)),position=position_dodge(.72),vjust=-.65,
              family=style$font,size=3.2,colour=style$ink) +
  state_scales("fill") + scale_y_continuous(limits=c(0,100),breaks=seq(0,100,25),expand=expansion(mult=c(0,0))) +
  labs(title="I  Grouped bars",subtitle="Mean score on a 0–100 scale; direct value labels",
       x="Sampling level",y="Mean score") + theme_delalamo()

plots$J <- ggplot(heat,aes(residue,sample,fill=confidence)) +
  geom_tile(colour="white",linewidth=.8) +
  scale_fill_viridis_c(option="cividis",limits=c(50,100),name="Confidence",breaks=c(50,75,100),
    guide=guide_colourbar(title.position="top",barwidth=grid::unit(110,"pt"),barheight=grid::unit(6,"pt"))) +
  scale_x_continuous(expand=c(0,0),breaks=c(1,3,6,9,12)) + scale_y_discrete(expand=c(0,0)) +
  labs(title="J  Heatmap",subtitle="Continuous values keep a perceptually ordered scale",
       x="Residue block",y=NULL) + theme_delalamo("") + theme(panel.border=element_blank())

plots$K <- ggplot(facets,aes(x,y)) +
  geom_point(aes(fill=confidence),shape=21,size=1.6,stroke=.2,colour=style$ink,alpha=.8) +
  scale_fill_viridis_c(option="cividis",limits=c(50,100),name="Confidence",breaks=c(50,75,100),
    guide=guide_colourbar(title.position="top",barwidth=grid::unit(110,"pt"),barheight=grid::unit(6,"pt"))) +
  facet_wrap(~protein,ncol=2) +
  scale_x_continuous(breaks=c(0,5,10)) + scale_y_continuous(breaks=c(0,4,8)) +
  labs(title="K  Small multiples",subtitle="Shared axes and confidence scale across all four panels",
       x="Reference displacement (a.u.)",y="Model displacement (a.u.)") + theme_delalamo("xy")

upper <- ggplot(pc,aes(pc1,fill=state,colour=state)) +
  geom_density(alpha=.20,linewidth=.55,bw=.4) + state_scales(c("fill","colour")) +
  scale_x_continuous(limits=c(-4,4),breaks=seq(-4,4,2),expand=c(0,0)) +
  labs(x=NULL,y=NULL) + theme_delalamo("") +
  theme(legend.position="none",axis.text.x=element_blank(),axis.text.y=element_blank(),panel.border=element_blank(),
        plot.margin=margin(0,20,0,16))
lower <- ggplot(pc,aes(pc1,similarity)) +
  geom_point(aes(fill=state,shape=state),colour=style$ink,size=1.75,stroke=.22,alpha=.67) +
  state_scales(c("fill","shape")) + scale_x_continuous(limits=c(-4,4),breaks=seq(-4,4,2),expand=c(0,0)) +
  scale_y_continuous(breaks=c(.8,.85,.9,.95)) +
  labs(x="Conformational coordinate (PC1, a.u.)",y="Similarity (a.u.)") + theme_delalamo("y") +
  theme(legend.position="none",plot.margin=margin(0,20,14,16))
aligned <- align_plots(upper,lower,align="v",axis="lr")
composite_body <- plot_grid(plotlist=aligned,ncol=1,rel_heights=c(.25,.75))
composite_head <- ggdraw() +
  draw_label("L  Density + scatter",x=.034,y=.81,hjust=0,fontfamily=style$font,fontface="bold",size=18,colour=style$ink) +
  draw_label("A shared x-axis, following your Figure 3 composition",x=.034,y=.46,hjust=0,fontfamily=style$font,size=10.8,colour=style$muted) +
  annotate("point", x=.047,y=.12,shape=21,size=2.7,fill=style$teal,colour=style$ink,stroke=.3) +
  draw_label("State A",x=.07,y=.12,hjust=0,fontfamily=style$font,size=9.5,colour=style$ink) +
  annotate("point", x=.245,y=.12,shape=24,size=2.7,fill=style$orange,colour=style$ink,stroke=.3) +
  draw_label("State B",x=.27,y=.12,hjust=0,fontfamily=style$font,size=9.5,colour=style$ink)
plots$L <- plot_grid(composite_head,composite_body,ncol=1,rel_heights=c(.23,.77))

footer <- function() ggdraw() +
  draw_line(x=c(.025,.975),y=c(.90,.90),colour=style$frame,linewidth=.35) +
  draw_label("SYNTHETIC DATA  ·  Styling study only",x=.025,y=.37,hjust=0,fontfamily=style$font,size=9,colour=style$muted) +
  draw_label("DEL ALAMO  /  V1",x=.975,y=.37,hjust=1,fontfamily=style$font,size=9,fontface="bold",colour=style$ink)

save_png <- function(p,name,w,h,dpi=180) ggsave(file.path(out,name),p,width=w,height=h,
                                               units="in",dpi=dpi,device=ragg::agg_png,bg="white")
for (id in names(plots)) {
  final <- plot_grid(plots[[id]],footer(),ncol=1,rel_heights=c(1,.075))
  save_png(final,paste0("charts/",id,".png"),7.2,5.8)
}
sheet <- function(ids,title,number) {
  head <- ggdraw() +
    draw_label(title,x=.028,y=.67,hjust=0,fontfamily=style$font,fontface="bold",size=25,colour=style$ink) +
    draw_label("Minimal scientific figures, with a little editorial clarity",x=.029,y=.17,hjust=0,fontfamily=style$font,size=12,colour=style$muted) +
    draw_label(number,x=.975,y=.6,hjust=1,fontfamily=style$font,size=12,colour=style$muted)
  body <- plot_grid(plotlist=plots[ids],ncol=2)
  plot_grid(head,body,footer(),ncol=1,rel_heights=c(.085,.87,.045))
}
sheets <- list(
  "01-relationships"=sheet(LETTERS[1:4],"Relationships & uncertainty","01 / 03"),
  "02-distributions"=sheet(LETTERS[5:8],"Distributions","02 / 03"),
  "03-comparisons"=sheet(LETTERS[9:12],"Comparisons & structure","03 / 03")
)
for (nm in names(sheets)) save_png(sheets[[nm]],paste0(nm,".png"),14.4,12.5)
overview <- plot_grid(plotlist=plots,ncol=3)
save_png(overview,"overview.png",21.6,22,110)
writeLines(capture.output(sessionInfo()),file.path(out,"session-info.txt"))
cat("Rendered 12 individual charts, three gallery sheets, and an overview.\n")
