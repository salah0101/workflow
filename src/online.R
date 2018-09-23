table_read<-function(file, is_x = T){
  data <- read.table(file, sep =",")
  if(is_x){
    data<-data[,-18]
    colnames(data)<- c("free", "lwait", "maxw_queue", "maxq_queue","maxp_queue","minq_queue", "minp_queue",
                       "sumw_queue", "sumq_queue", "sumq2_queue", "sumqlog_queue", "sumpq_queue", 
                       "sumr_queue", "maxpq_queue", "maxr_queue", "minpq_queue", "minr_queue", 
                       "sump_queue","sump_rem_run","sump_elap_run", "sumpq_rem_run", "sumpq_elap_run")
  } else {
    colnames(data)<- c("fcfs", "spf", "lqf", "laf")
  }
  return(data)
}


file="class2sched/o/zymakefile_online_classify/o.KTH-SP2.table.prf"
Y = table_read(file, is_x=F)
file="class2sched/o/zymakefile_online_classify/o.KTH-SP2.table.features"
X = table_read(file)

Data = cbind(X,Y)
P<-length(X)
K<-length(Y)
N<-length(X[,1])
policies<- c("fcfs", "spf", "lqf", "laf")

library(randomForestSRC)
fit<-rfsrc(cbind(fcfs,spf,lqf,laf)~.,Data)

mean((fit$regrOutput$fcfs$predicted.oob - Data$fcfs)^2)+
mean((fit$regrOutput$spf$predicted.oob - Data$spf)^2)+
mean((fit$regrOutput$lqf$predicted.oob - Data$lqf)^2)+
mean((fit$regrOutput$laf$predicted.oob - Data$laf)^2)





sum(apply((SRF - Data[,(P+1):(P+4)])^2,2,mean))



library(randomForest)
fitRF <- randomForest(x=Data[,(1:P)],y=Data[,(P+1)],importance=TRUE)
SRF<-data.frame(fcfs=predict(fitRF,Data[,1:(P+1)]))

fitRF <- randomForest(x=Data[,(1:P)],y=Data[,(P+2)],importance=TRUE)
SRF$spf<-predict(fitRF,Data[,c(1:P,(P+2))])

fitRF <- randomForest(x=Data[,(1:P)],y=Data[,(P+3)],importance=TRUE)
SRF$lqf<-predict(fitRF,Data[,c(1:P,(P+3))])

fitRF <- randomForest(x=Data[,(1:P)],y=Data[,(P+4)],importance=TRUE)
SRF$laf<-predict(fitRF,Data[,c(1:P,(P+4))])




BestFixed<-Y[,which(apply(Y,2,sum)==min(apply(Y,2,sum)))]

BestLast <- numeric(N)
BestLast[1] <- min(Y[1,])
for(i in 2:N){
  tmp<-which(Y[i-1,]==min(Y[i-1,]))
  BestLast[i] <- Y[i, ifelse( length(tmp)==1, tmp, sample(tmp, 1) ) ]
}


PredictVal<-data.frame(matrix(rep(NA,N*K),nrow=N,ncol=K))
names(PredictVal)<-policies
step<-15
for (i in (step+1):N){
  for (j in 1:K){
    #df<-cbind(X[(i-step):(i-1),],Y[(i-step):(i-1),j])
    #names(df)[P+1]<-policies[j]
    fitRF <- randomForest(x=X[(i-step):(i-1),],y=Y[(i-step):(i-1),j],importance=TRUE)
    #fitRF <- lm(paste(policies[j],"~.", sep=""),data=df)
    PredictVal[i,j]<-predict(fitRF,newdata=X[i,])
  }
}


LearnPredict<- apply(PredictVal[-(1:step),],1,min)
PredictIndex<-numeric(N-step)

for(i in 1:(N-step)){
  tmp<-which(PredictVal[i+step,]==LearnPredict[i])
  PredictIndex[i] <- ifelse( length(tmp)==1, tmp, sample(tmp, 1) )
}


#timeLearn<-
sum(Y[cbind(seq_along(PredictIndex)+step, PredictIndex)])
#timeFixed<-
sum(BestFixed[-(1:step)])

sum(BestLast[-(1:step)])



#second approach







