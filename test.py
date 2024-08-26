出現以下異常

type Exception report

message

description The server encountered an internal error () that prevented it from fulfilling this request.

exception

org.apache.jasper.JasperException: Unable to compile class for JSP

An error occurred at line: 65 in the jsp file: /LogSummary.jsp
Generated servlet error:
D:\Tomcat 5.0\work\Catalina\localhost\rdmplog\org\apache\jsp\LogSummary_jsp.java:403: error: variable out is already defined in method _jspService(HttpServletRequest,HttpServletResponse)
        try (PrintWriter out = new PrintWriter(new FileWriter("user_log.txt", true))) {
                         ^


An error occurred at line: 65 in the jsp file: /LogSummary.jsp
Generated servlet error:
Note: D:\Tomcat 5.0\work\Catalina\localhost\rdmplog\org\apache\jsp\LogSummary_jsp.java uses unchecked or unsafe operations.


An error occurred at line: 65 in the jsp file: /LogSummary.jsp
Generated servlet error:
Note: Recompile with -Xlint:unchecked for details.
1 error



	org.apache.jasper.compiler.DefaultErrorHandler.javacError(DefaultErrorHandler.java:84)
	org.apache.jasper.compiler.ErrorDispatcher.javacError(ErrorDispatcher.java:332)
	org.apache.jasper.compiler.Compiler.generateClass(Compiler.java:412)
	org.apache.jasper.compiler.Compiler.compile(Compiler.java:472)
	org.apache.jasper.compiler.Compiler.compile(Compiler.java:451)
	org.apache.jasper.compiler.Compiler.compile(Compiler.java:439)
	org.apache.jasper.JspCompilationContext.compile(JspCompilationContext.java:511)
	org.apache.jasper.servlet.JspServletWrapper.service(JspServletWrapper.java:295)
	org.apache.jasper.servlet.JspServlet.serviceJspFile(JspServlet.java:292)
	org.apache.jasper.servlet.JspServlet.service(JspServlet.java:236)
	javax.servlet.http.HttpServlet.service(HttpServlet.java:802)
