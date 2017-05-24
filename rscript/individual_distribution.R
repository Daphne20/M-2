#!/usr/bin/env R
rm(list=ls())
library(RColorBrewer)
library(ggplot2)

args<-commandArgs(T)
id_file=args[1]
bacteria_file=args[2]
bgc_file=args[3]
compounds_file=args[4]
outputdir=args[5]

setwd(outputdir)
id_table=read.table(id_file,header = F,sep = "\t")
bacteria_table=read.table(bacteria_file,header = F,sep = "\t")
bgc_table=read.table(bgc_file,header = F,sep = "\t")
compounds_table=read.table(compounds_file,header = F,sep = "\t")



read_density_log=log(id_table[,2])
read_density <- density(read_density_log)
density_file="mappedread_density.pdf"
pdf(file=density_file)
plot(read_density, main="mapped read density",xlab="log RPKM")
polygon(read_density, col="red", border="blue")
dev.off()


bgc_distribution_file="bgc_distribution.pdf"
pdf(file=bgc_distribution_file,width = 8.5,height = 14)
bgc_table_percent<-data.frame(bgc=bgc_table[,1],percentage=bgc_table[,2]/sum(bgc_table[,2]))
p<-ggplot(data=bgc_table_percent,aes(x=reorder(bgc,percentage),y=percentage,fill=percentage))+labs(x = "BGC", y = "Percentage", title = "BGC distribution")
p+scale_fill_gradientn(colors=c("blue","red"))+coord_flip()+geom_bar(stat = "identity",position = "dodge")
dev.off()


bactiera_distribution_file <- "bactiera_distribution.pdf"
pdf(file=bactiera_distribution_file)
bacteria_percent <- data.frame(organism=bacteria_table[,1],percentage=bacteria_table[,2]/sum(bacteria_table[,2]))
bacteria_percent_sort <- bacteria_percent[order(bacteria_percent$percentage,decreasing = T),]
bacteria_percent_top <- data.frame(organism=c(as.vector(bacteria_percent_sort$organism[1:10]),"other"),percentage=c(bacteria_percent_sort$percentage[1:10],
                                            sum(bacteria_percent_sort$percentage)-sum(bacteria_percent_sort$percentage[1:10])))

label <- round(100*bacteria_percent_top$percentage,1)
label<- paste(label, "%", sep = "")
pie(bacteria_percent_top$percentage, labels=label,main="top 10 bacteria distribution", col=topo.colors(length(bacteria_percent_top$percentage)))
legend(locator(1),label, cex=0.8, fill=topo.colors(length(bacteria_percent_top$percentage)))
                                                                                                





