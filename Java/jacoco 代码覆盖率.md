## jacoco 代码覆盖率

---

1. 修改 gradle 文件，修改如下：


```
// 引用 jacoco
apply plugin: 'jacoco'
jacoco{
    version = '0.7.8'
}
// buildTypes 设置
testCoverageEnabled true
// 新建 jacoco 任务
    task testJacocoReport(type:JacocoReport) {
        group = "Reporting"
        description = "Generate Jacoco coverage reports on the  build."
        classDirectories = fileTree(
                dir: "$buildDir/intermediates/classes",
                excludes: ['**/R.class',
                           '**/R$*.class',
                           '**/RecyclingBitmapDrawable.class',
                           '**/ImageLruDiskBasedCache.class',
                           '**/VolleyLog.class',
                           '**/KTVApplication.class',
                           '**/ImageManager.class',
                           '**/TaskQueueLog.class',
                           '**/LiveViewerActivity.class',
                           '**/LiveRoomGiftController$6.class',
                           '**/*$ViewInjector*.*',
                           '**/BuildConfig.*',
                           '**/Manifest*.*']
        )
        def coverageSourceDirs = ["app／src/main/java"]
        additionalSourceDirs = files(coverageSourceDirs)
        sourceDirectories = files(coverageSourceDirs)
        executionData = fileTree(dir: './build/outputs', include: '**/*.ec')
        reports {
            xml.enabled = true
            html.enabled = true
        }
    }
```

2. 修改 Application 类相关代码，如下：


``` java
public void onActivityDestroyed(Activity activity) {
	// Todo jacoco
	jacoco();
	}
// Todo jacoco create file
String DEFAULT_COVERAGE_FILE_PATH = "/mnt/sdcard/coverage.ec";
File file = new File(DEFAULT_COVERAGE_FILE_PATH);
if (!file.exists()) {
	try {
		file.createNewFile();
		} catch (IOException e) {
		e.printStackTrace();
		}
		}
		
// Todo jacoco write file
private void jacoco () {
    OutputStream out = null;
    try {
        out = new FileOutputStream("/mnt/sdcard/coverage.ec", false);
        Object agent = Class.forName("org.jacoco.agent.rt.RT")
                .getMethod("getAgent")
                .invoke(null);
        out.write((byte[]) agent.getClass().getMethod("getExecutionData", boolean.class)
                .invoke(agent, false));
    } catch (Exception e) {
        e.printStackTrace();
    } finally {
        if (out != null) {
            try {
                out.close();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }
}
```



