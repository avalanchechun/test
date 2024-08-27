<%@ page contentType="text/html; charset=UTF-8" %>
<%@ include file="./maintain/ext/dbinclude.jsp" %>

<%

	String WO = toString(request.getParameter("WO"));
%>

<html>
<head>
    <meta charset="utf-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <title><%=_title%></title>
    <link rel="stylesheet" type="text/css" href="./Content/bootstrap/css/bootstrap.min.css" />
    <link rel="stylesheet" type="text/css" href="./Content/sb-admin/sb-admin.min.css">
    <link rel="stylesheet" type="text/css" href="./Content/font-awesome/css/all.css">
    <link rel="stylesheet" href="./css/Phison.css">
</head>
<style>
#customers {
  font-family: "Trebuchet MS", Arial, Helvetica, sans-serif;
  border-collapse: collapse;
  width: 100%;
}

#customers td, #customers th {
  border: 1px solid #ddd;
  padding: 8px;
}

#customers tr:nth-child(even){background-color: #f2f2f2;}

#customers tr:hover {background-color: #ddd;}

#customers th {
  padding-top: 12px;
  padding-bottom: 12px;
  text-align: center;
  background-color: #4CAF50;
  color: white;
}
</style>
  <body class="fixed-nav sticky-footer bg-dark" id="page-top">
    <!-- Navigation-->	
<%@ include file="Navigation.jsp" %>
    <div class="content-wrapper">
        <div class="container-fluid">
            <ol class="breadcrumb">
                <!-- SiteMap-->
					Home > Log Summary*2 ( Search double test log by WO )
            </ol>

            <!-- Content-->
            <div id="body">
<form method="post" name="mdata" action="LogSummaryDouble.jsp">
WO:&nbsp;<input type=text name="WO" value="<%=WO%>">
<input type="submit" name="search" value="doSearch">
</form>
<%
	if ( WO.length()>10 ) {
		String pWS_ID="";
		String moYM = "PELogSr_20"+WO.substring(4,8);
		//511-181017127
		//String sql = "use "+moYM+";select WS_ID,ID_01,count(*)cnt from  mfg_test_result where WO='"+WO+"' and ID_01<>'N/A' \n";
		//sql += " group by WS_ID,ID_01\n order by WS_ID, count(*) desc, ID_01";
		
		String sql = 
		"use "+moYM+"; \n"+
		"select * into #tmp from mfg_test_result  \n"+
		"where WO='"+WO+"' \n"+
		"; \n"+
		"select ws_id,ctl_lot,START_DATETIME,ID_01 from #tmp t1  \n"+
		"where exists(  \n"+
		"select ctl_lot,ws_id,count(*) from #tmp \n"+
		"where ctl_lot<>'' \n"+
		"group by ctl_lot, ws_id having count(*)>1 and t1.WS_ID=WS_ID and t1.CTL_LOT=CTL_LOT \n"+
		")  \n"+
		"order by ws_id,ctl_lot,START_DATETIME,ID_01 \n";
		//out.println("<pre>"+sql+"</pre>");
		
		Statement stmt = conn.createStatement();
		ResultSet rs=stmt.executeQuery(sql);
%>
		<table id="customers" >
		<tr>
		<th align="center" >WS_ID</th>
		<th align="center" >CTL_LOT</th>
		<th align="center" >START_DATETIME</th>
		<th align="center" >ID_01</th>
		</tr>
<%		
		String pCTL_LOT="";
		while (rs.next()) {
			String WS_ID = rs.getString("WS_ID");
			String CTL_LOT = rs.getString("CTL_LOT");
			String START_DATETIME = rs.getString("START_DATETIME");
			String ID_01 = rs.getString("ID_01");
			String indent = "";
			if ( pCTL_LOT.compareTo(CTL_LOT)!=0 ) {
				pCTL_LOT = CTL_LOT;
			}
			else {
				indent = "style=\"color:red\"";
			}
			
%>			
			<tr>
			<td align="center" ><%=WS_ID%></td>
			<td align="center" <%=indent%>><%=CTL_LOT%></td>
			<td align="center" ><%=START_DATETIME%></td>
			<td align="center" ><%=ID_01%></td>
			</tr>
<%
        }
%>
		</table>
<%		
		stmt.execute("drop table #tmp");
		stmt.close();
	}
%>
            </div>
        </div>
	</div>
        <!-- /.container-fluid-->
<%@ include file="Foot.jsp" %>    
<!-- /.content-wrapper-->
    <script src="./Scripts/modernizr-2.6.2.js"></script>
    <script src="./Content/jquery/jquery.min.js"></script>
    <script src="./Content/popper/popper.min.js"></script>
    <script src="./Content/bootstrap/js/bootstrap.min.js"></script>
    <script src="./Content/sb-admin/sb-admin.min.js"></script>
    <script defer src="./Content/font-awesome/js/all.js"></script>

    <script type="text/javascript">

    </script>
  </body>
</html>

<%@ include file="./maintain/ext/dbexit.jsp" %>
