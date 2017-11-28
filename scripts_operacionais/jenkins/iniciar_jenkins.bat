
REM ESSE BAT DEVE SER EXECUTADO COMO ADMINISTRADOR


set JAVA_HOME=E:\jdk1.7.0_79
SET PATH=%JAVA_HOME%/bin;%PATH%


SET PATH_JENKINS=e:\jenkins-jobs\jenkins.war


java -Xrs -Xms1024m -Xmx3072m -XX:PermSize=1024m -XX:MaxPermSize=3072m -Dhudson.lifecycle=hudson.lifecycle.WindowsServiceLifecycle -jar %PATH_JENKINS%