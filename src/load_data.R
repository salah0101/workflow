#!/usr/bin/env Rscript

library(docopt)
library(ggplot2)
library(broom)
library(randomForest)
library(gridExtra)


'usage: tool.R <input1> <input2> [--out=<output1>] [--out2=<output2>] [--out3=<output3>]
tool.R -h | --help

options:
 <input1>        Data
 <input2>        Vector of policices
--out=<output1>  linear regression selection table [Default: LR.pdf]
--out2=<output2>  random forest selection table [Default: RF.pdf]
--out3=<output3>  performance table  [Default: default.statv]
' -> doc


args<- docopt(doc)
#print(args)

#----------------reading aaks file----------------------------------------------------------
aaks_read <- function(f)
{
  df <- read.table(f)
  colnames(df) <- c('avgwait', 'maxwait', 'avgbsld', 'maxbsld', 'avgflow', 'maxflow',
                    'name', 'id1', 'id2', 'policy', 'sqff',
                    'AvgRun','MaxRun','MinRun','SumRun', 'TenRun', 'MedRun', 'goRun',
                    'AvgTReq','MaxTReq','MinTReq','SumTReq', 'TenTReq', 'MedTReq', 'goTReq',
                    'AvgSize','MaxSize','MinSize','SumSize', 'TenSize', 'MedSize', 'goSize',
                    'AvgArea','MaxArea','MinArea','SumArea', 'TenArea', 'MedArea', 'goArea',
                    'AvgRR','MaxRR','MinRR','SumRR', 'TenRR', 'MedRR', 'goRR',
                    'AvgRJ','MaxRJ','MinRJ','SumRJ', 'TenRJ', 'MedRJ', 'goRJ',
                    'AvgCos','MaxCos','MinCos','SumCos', 'TenCos', 'MedCos', 'goCos',
                    'AvgSin','MaxSin','MinSin','SumSin', 'TenSin', 'MedSin', 'goSin')
  return(df)
}
#-------------------------------------------------------------------------------------------
#file = "/home//vasya//class2sched//o.KTH-SP2.aaks"
#file = "/home//vasya//Documents/o.KTH-SP2.aaks"
#df <- aaks_read(file)

df <- aaks_read(args$input1)

inp2<-args$input2

inp2 = "fcfs, lcfs, lpf, spf, sqf, lqf, lexp, sexp, lrf, srf, laf, saf"
policies <- array(unlist(strsplit(inp2, ", ")))
#print(policies)
K <- length(policies)


#absolutely useless features
drops <- c("MinRun","MaxTReq","MinTReq","MinSize","TenSize",
           "MinArea","MaxCos","MinCos","MaxSin", "MinSin")
data <- df[,!(names(df) %in% drops)]


#transformation of data (gathering of simulations for each week)----------------------------
for(i in 1:K){
  data[,paste(policies[i])] <- 0
}

maxid1<-max(data$id1)
maxid2<-max(data$id2)
l <- maxid1 * maxid2
w <- length(data)
L <- length(data[,1])
temp <- data
for(k in 1:L){
  if(k%%K!=0){
    i<-(k %/% K) + 1
    j<-w-K+(k%%K)
  } else {
    i<-(k %/% K)
    j<-w
    for (t in 1:(w-K)){
      temp[i,t]<-data[k,t]
    }
  }
  temp[i,j]<-data[k,1]
}
data <- temp[1:l,-(1:11)]
#-------------------------------------------------------------------------------------------

P <- ncol(data) - K




#--------------Performance-Table-----------------------------------
L <- length(data[,1])
BestTime<-apply(data[,(P+1):(P+K)],1,min)
BestTimeInd<-numeric(L)
NumTimeBest<-numeric(K)
for(i in 1:L){
  BestTimeInd[i]<-min(which(data[i,(P+1):(P+K)]== BestTime[i]))
}
for(i in 1:K){
  NumTimeBest[i] <- length(which(BestTimeInd == i))
}
names(NumTimeBest)<-NULL
#NumTimeBest<-c(table(BestTimeInd))
AverOfPerf<-apply(data[,(P+1):(P+K)],2,mean)
names(AverOfPerf)<-NULL
tab <- data.frame(policies,NumTimeBest,AverOfPerf)
tab$AvgBest <- 0
for(i in 1:K){
  tab$AvgBest[i]<-mean(subset(BestTime, BestTimeInd == i))
}






#shifting relatively to average--------------------------------
datashift<-data
l<-length(datashift)
avg<-apply(datashift[,((l-K+1):l)],1,mean)
for (i in 0:(K-1)){
  datashift[,l-i]<- datashift[,l-i] - avg
}
data <- datashift
#--------------------------------------------------------------

#summary(data)

#-----------------lm + drawing coefficients--------------------


#-----linear regression for each policy + making a result table of t-test for all models
for(i in 1:K){
  fo <- paste(names(data)[P+i], "~", paste(names(data)[(1:P)], collapse=" + "))
  fit <- lm(fo,data)
  ti <- tidy(fit)
  ti$pcon <- ti$p.value<0.1
  ti$name <- policies[i]
  summar <- summary(fit)
  if(i==1){
    tibig<-ti[,c(1,5,6,7)]
    bigsummar <- c(summar$r.squared, unname(summar$fstatistic[1]))
  } else {
    tibig<-rbind(tibig,ti[,c(1,5,6,7)]) #result table
    bigsummar <- rbind(bigsummar,c(summar$r.squared, unname(summar$fstatistic[1])))
  }
}



#plotting a beautiful table
tibig$name = factor(tibig$name,levels = policies)
tbl<-ggplot(tibig, aes(term, name))+
  geom_tile(aes(fill = pcon),colour = "black",size=2)+
  labs(title ="Table", x = "Policies", y = "Feature", colour="Is the cofficient\n significant?")+
  scale_fill_manual(values=c("red","green"))+
  theme(axis.text.x = element_text(angle = 45, hjust = 1),
        axis.title.y=element_text(size=17),
        axis.title.x=element_text(size=17),
        legend.text=element_text(size=12),
        title=element_text(size=14),
        axis.text=element_text(size=15),
        plot.title=element_text(size=17))

#-----------------------------------------------------------------




#--------------------polynomial-----------------------------------------------
#fo2 <- paste(names(data)[P+2], "~", paste(names(data)[(1:P)], collapse=" + "), 
#             "+ I(", paste(names(data)[(1:P)], collapse="^2) + I("),"^2)",
#             "+ I(", paste(names(data)[(1:P)], collapse="^3) + I("),"^3)",
#             "+ I(", paste(names(data)[(1:P)], collapse="^4) + I("),"^4)",
#             "+ I(", paste(names(data)[(1:P)], collapse="^5) + I("),"^5)",
#             "+ I(", paste(names(data)[(1:P)], collapse="^6) + I("),"^6)",
#             "+ I(", paste(names(data)[(1:P)], collapse="^7) + I("),"^7)")
#------------------------------------------------------------------------------
#--------------MARS-----------------------------------------------------------------------
#fit_mars <- earth(cbind(,saf) ~ MaxSize * AvgArea, data=data) 
#fit_mars <- earth(formula = paste(cbind(names(data)[(P+1):(P+K)]), "~", 
#                                  paste(names(data)[(1:P)], collapse=" + ")), data = data) 
#fit_mars$cuts
#fit_mars <- earth(x=data[,(1:P)],y=data[,(P+1)],thresh = 0.001)
#fit_mars$rsq
#-----------------------------------------------------------------------------------------


#-----------Random Forest-----------------------------------------------------------------

#train_size <- floor(0.8 * nrow(data))
#set.seed(123)
#indexes <- sample(seq_len(nrow(data)), size = train_size)
#train <- data[indexes, ]
#test <- data[-indexes, ]


for (i in 1:K){
  fitRF <- randomForest(x=data[,(1:P)],y=data[,(P+i)],importance=TRUE)
  mm <- apply(fitRF$importance,2,sum)
  if(i==1){
    resrf <- data.frame(term = names(data)[1:P],
                        sig = ifelse((fitRF$importance[,1]/mm[1])>=0.05, "Yes", "No"),
                        policy = policies[i])
    row.names(resrf)<-NULL
  } else {
    resrf <- rbind(resrf,data.frame(term = names(data)[1:P],
                                    sig = ifelse((fitRF$importance[,1]/mm[1])>=0.05, "Yes", "No"),
                                    policy = policies[i]))
    row.names(resrf)<-NULL
  }
}

#plotting a beautiful table fo RF
resrf$policy = factor(resrf$policy,levels = policies)
tblrf<-ggplot(resrf, aes(term, policy))+
  geom_tile(aes(fill = sig),colour = "black",size=2)+
  labs(title ="Table", x = "Policies", y = "Feature", colour="Is the cofficient\n significant?")+
  scale_fill_manual(values=c("red","green"))+
  theme(axis.text.x = element_text(angle = 45, hjust = 1),
        axis.title.y=element_text(size=17),
        axis.title.x=element_text(size=17),
        legend.text=element_text(size=12),
        title=element_text(size=14),
        axis.text=element_text(size=15),
        plot.title=element_text(size=17))

#ggsave(plot = tblrf, file = "RF_Table.pdf",width=40,height=14)



#write.table(tab, file = "Performance_Table")
#-------------------------------------------------------------  

#loss<- sum((forecast-test[,(P+1)])^2)

#sum(  ( forecast- mean(test[,(P+1)]) )^2  )/ sum(  (test[,(P+1)]- mean(test[,(P+1)]) )^2 )


#mnt <- mean(test[,(P+1)])
#mnf <- mean(forecast)
#100* ((mnf-mnt)/mnt)

#importance(fitRF)

#mm<-apply(fitRF$importance,2,sum)
#round(fitRF$importance[,1]/mm[1], digits = 4)

#lol<-cvFit(fit, data = data, y = data[,(P+1)], K = 10)
#lol1<-cvFit(fitRF, data = train, y = train[,(P+1)], K = 10)
#-----------------------------------------------------------------------------------------



#----------------Output-of-results--------------------------------------------------------

#Output 1
pdf(file=args$out,width=40,height=14)
tbl

#Output 2
pdf(file=args$out2,width=40,height=14)
tblrf

#Output 3
ggsave(file=args$out3,plot=tableGrob(tab[K:1,]),width=5,height=7)

##print(tibig)
##table of results: feature - p.value - is significant? - for which policy

#for (i in 1:nrow(tab)){
#  cat(unlist(tab[i,]))
#  cat("\n")
#}

#write.table(tab,file=args$out3)

#for (i in 1:nrow(tibig)){
#  cat(unlist(bigsummar[i,]))
#  cat("\n")
#}

