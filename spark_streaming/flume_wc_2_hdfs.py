# ‐*‐ coding: UTF‐8 ‐*‐
###spark streaming&&Flume
from pyspark import SparkContext
from pyspark.streaming import StreamingContext 
from pyspark.streaming.flume import FlumeUtils

sc=SparkContext("yarn","FlumeWordCount")

# 處理時間間隔為2秒
ssc=StreamingContext(sc,2)

# 開啟TCP socket ip & port
lines = FlumeUtils.createStream(ssc, "1.1.1.1",12345) lines1=lines.map(lambda x:x[1])

# 對兩秒內收到的字串做分割
words=lines1.flatMap(lambda line:line.split(" "))

# word count
pairs=words.map(lambda word:(word,1)) wordcounts=pairs.reduceByKey(lambda x,y:x+y)

# 輸出檔案至HDFS 格式為/tmp/flume‐日期
wordcounts.saveAsTextFiles("/tmp/flume")

# 檢查檔案內容
wordcounts.pprint()

# 啟動spark streaming
ssc.start()

# 等待計算終止
ssc.awaitTermination()
