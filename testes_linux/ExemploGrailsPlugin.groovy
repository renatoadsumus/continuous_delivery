class MailServiceGrailsPlugin {
    // the plugin version
    def version = "1.10.1"
    def groupId = "br.com.infoglobo.classificados"
    def repository = "http://inforep01.ogmaster.local:8080/nexus/content/repositories/"
    // the version or versions of Grails the plugin is designed for
    def grailsVersion = "2.3 > *"
    // resources that are excluded from plugin packaging
    def pluginExcludes = [
        "grails-app/views/error.gsp"
    ]

}
