---
title: 避免Android开发中的ANR
date: '2010-08-27 18:03:45 +0800'
---
via:  <a href="https://code.google.com/events/io/2010/sessions/writing-zippy-android-apps.html" target="_blank">Writing Zippy Android Apps</a>

## ANR是什么

ANRs ("Application Not Responding")，意思是"应用没有响应"。

在如下情况下，Android会报出ANR错误：

- 主线程 ("事件处理线程" / "UI线程") 在5秒内没有响应输入事件

- BroadcastReceiver 没有在10秒内完成返回

通常情况下，下面这些做法会导致ANR

1、在主线程内进行网络操作

2、在主线程内进行一些缓慢的磁盘操作（例如执行没有优化过的SQL查询）

应用应该在5秒或者10秒内响应，否则用户会觉得"这个应用很垃圾""烂""慢"...等等

## 一些数据(Nexus One为例)
- ~0.04 ms - 通过管道进程从 A->B 再从 B->A 写一个字节；或者（从dalvik）读一个简单的/proc文件
- ~0.12 ms - 由 A->B 再由 B->A 进行一次Binder的RPC调用
- ~5-25 ms - 从未缓冲的flash
- ~5-200+(!) ms - 向为缓冲的flash中写点东西（下面是具体数据）
-    16 ms - 60fps 的视频中的一帧
-    41 ms - 24fps 的视频中的一帧
- 100-200 ms - human perception of slow action
- 108/350/500/800 ms - 3G网络上ping（可变）
- ~1-6+ seconds - 通过HTTP在3G网络上获取6k的数据

## android.os.AsyncTask
AsyncTask 可以与UI线程很方便的配合，这个类可以在后台执行一些操作，并在执行结束的时候将结果发布到UI线程中去，并且无需使用线程或handler来控制。

例子:
```
private class DownloadFilesTask extends AsyncTask {
	protected Long doInBackground(URL... urls) {  // on some background thread
		int count = urls.length;
		long totalSize = 0;
		for (int i = 0; i < count; i++) {
			totalSize += Downloader.downloadFile(urls[i]);
			publishProgress((int) ((i / (float) count) * 100));
		}

		return totalSize;
 	} 

	protected void onProgressUpdate(Integer... progress) {  // on UI thread!
		setProgressPercent(progress[0]);
	} 

	protected void onPostExecute(Long result) {  // on UI thread!
		showDialog("Downloaded " + result + " bytes");
	}
} 

new DownloadFilesTask().execute(url1, url2, url3);  // call from UI thread!

private boolean handleWebSearchRequest(final ContentResolver cr) {
    ...
	new AsyncTask() {
	    protected Void doInBackground(Void... unused) {
	    	Browser.updateVisitedHistory(cr, newUrl, false);
	    	Browser.addSearchUrl(cr, newUrl);
	    	return null;
	    } 
	}.execute()
    ...
    return true; 

}
```

## AsyncTask要点
1、必须从主线程调用，或者线程中有Handler或Looper。
2、不要在一个可能会被另外一个AsyncTask调用的库里面使用AsyncTask（AsyncTask是不可重入的）
3、如果从一个activity中调用，activity进程可能会在AsyncTask结束前退出，例如：

- 用户退出了activity
- 系统内存不足
- 系统暂存了activity的状态留待后用
- 系统干掉了你的线程

如果AsyncTask中的工作很重要，应该使用......

## android.app.IntentService
Eclair(2.0, 2.1)文档中说：

"An abstract Service that serializes the handling of the Intents passed upon service start and handles them on a handler  thread.  To use this class extend it and implement onHandleIntent(Intent). The Service will automatically be  stopped when the last enqueued Intent is handled."
有点令人困惑，因此...几乎没人用

Froyo (2.2) 的文档, 又澄清了一下....

android.app.IntentService

"IntentService is a base class for Services that handle asynchronous requests (expressed as Intents) on demand. Clients send requests  through startService(Intent) calls; the service is started as needed, handles each Intent in turn using a worker thread, and stops itself  when it runs out of work.

This 'work queue processor' pattern is commonly used to offload tasks from an application's main thread. The IntentService class exists to  simplify this pattern and take care of the mechanics. To use it, extend IntentService and implement onHandleIntent(Intent). IntentService  will receive the Intents, launch a worker thread, and stop the service as appropriate.

All requests are handled on a single worker thread -- they may take as long as necessary (and will not block the application's main loop), but  only one request will be processed at a time."

## IntentService 的好处

- Acitivity的进程，当处理Intent的时候，会产生一个对应的Service
- Android的进程处理器现在会尽可能的不kill掉你
- 非常容易使用

日历中IntentService的应用
```
public class DismissAllAlarmsService extends IntentService {
	@Override public void onHandleIntent(Intent unusedIntent) {
		ContentResolver resolver = getContentResolver();
		...
		resolver.update(uri, values, selection, null);
	}
}
in AlertReceiver extends BroadcastReceiver, onReceive()：  (main thread)
    Intent intent = new Intent(context, DismissAllAlarmsService.class);
    context.startService(intent);
```

## 其它技巧

1、当启动AsyncTask的时候，立刻disable UI元素（按钮等等）。
2、显示一些动画，表示在处理中
3、使用进度条对话框
4、使用一个定时器作为耗时警告，在AsyncTask开始时启动定时器，在AsyncTask的onPostExecute方法中取消定时器。
5、当不确定要耗时多久的时候，组合使用上述所有方法

## 总结

- 离开主线程！
- 磁盘和网络操作不是马上就能完的
- 了解sqlite在干嘛
- 进度展示很好

PS，在视频讲座中，作者还提到，Chrome团队为了避免Jank（响应超时而死掉），几乎所有的功能和任务都会在子线程里面去做。这一点也值得在Android中借鉴。

刘金雨译:  <a href="https://log4think.com/avoid_anr_in_android">避免Android开发中的ANR</a>
全文via:  <a href="https://code.google.com/events/io/2010/sessions/writing-zippy-android-apps.html" target="_blank">Writing Zippy Android Apps</a>

