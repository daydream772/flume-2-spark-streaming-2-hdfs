# flume-2-spark-streaming-2-hdfs
前言
=====
根據官方文件，Spark Streaming + Flume integreation有兩種方式：
  1. Flume-style Push-based Approach: 在SparkStreaming上設置一個Avro的接收器供Flume使用，然後由Flume推送資料進SparkStreaming中。
  2. Pull-based Approach using a Custom Sink: 將資料在Flume中作緩衝，然後由SparkStreaming設置一個客製化的Flume Sink接收資料，與第一種方法不同的是：只有當SparkStreaming處理完資料後，transcation才算成功。

這裡採用第一種方法。

實現此步驟分為三個部分：
  1. Weblog: 模擬weblog，將weblog以avro格式丟進flume中。
  2. Flume: 將收到的weblog以avro格式送進SparkStreaming做後續處理。
  3. Spark-Streaming: 收到weblog後，進行檔案處理 - word count，算完後輸出至HDFS中儲存。

版本
=====
CentOS 6.6
CDH 5.9.1
Apache Spark 2.1.0

步驟
=====
1. 啟動SparkStreaming程式
------
執行SaprkStreaming程式
		./${SPARK_HOME}/bin/spark-submit --jars ${SPARK_HOME}/lib/spark-streaming-flume-assembly_2.11-2.1.0.jar \
		flume_wc_2_hdfs.py 2>error.log

啟動後，會出現每兩秒的處理時間戳。

2. 啟動Flume Agent
------
啟動Flume agent，將其log輸出至console
		flume-ng agent -c /etc/flume-ng/conf -f flume_wc.conf -n agent1 \
		-Dflume.root.logger=INFO.console

3. 將資料傳送至Agent Source
------
將weblog所在資料透過設定之ip&port轉成avro格式並送入agent-source中。
		python weblogs.py

4. 檢查Agent運作情形
------
若正常運作，可透過agent's log看到agent正在作業。

5. 檢查SparkStreaming運作情形
------
若正常運作，可透過輸出畫面觀察到每個時間戳之內所處理的資料

6. 檢查HDFS有無資料
------
至HDFS檢查輸出路徑有無資料
		hadoop fs -cat /tmp/flume/日期/*
