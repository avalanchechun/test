<%@ page contentType="text/html; charset=UTF-8" %>
<%@ include file="./maintain/ext/dbinclude.jsp" %>
<%!
	public static String WS_ID_FIX( String wsid, String product ) {
        String ret=wsid;
        wsid = wsid.toUpperCase().trim();
        product = product.toUpperCase().trim();
        if ( wsid.compareTo("F2")==0 )  return "QC";
        if ( wsid.compareTo("F3")==0 )  {
            if ( product.compareTo("PCIE")==0 || product.compareTo("SATA")==0 ) {
                return "CSB";
            }
            return "BN";
        }
        if ( wsid.compareTo("F4")==0 )  {
            if ( product.compareTo("PATA")==0||product.compareTo("PCIE")==0|| product.compareTo("SATA")==0 ) {
                return "ICT";
            }
            if ( product.compareTo("USB")==0 ) {
                return "LT";
            }
            return "UP";
        }
        if ( wsid.compareTo("F5")==0 )  {
            if ( product.compareTo("PATA")==0||product.compareTo("PCIE")==0|| product.compareTo("SATA")==0 ) {
                return "PF1";
            }
        }
        if ( wsid.compareTo("F6")==0 )  {
            return "FQC";
        }
        if ( wsid.compareTo("F7")==0 )  {
            return "F1";
        }
        if ( wsid.compareTo("F8")==0 )  {
            return "QC";
        }
        if ( wsid.compareTo("F9")==0 )  {
            return "BN";
        }
        if ( wsid.compareTo("F10")==0 )  {
            return "ORT";
        }

        return ret;
	}
%>
<%
	String WO = toString(request.getParameter("WO"));
    String SkipDouble = toString(request.getParameter("SkipDouble"));
    if (SkipDouble.length()==0 ) {
        SkipDouble = "1";
    }
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
    		<!--  
    		<script language="JavaScript">
		alert("伺服器即將移轉至 http://192.168.16.111:8080/，請先郵件給  許智翔 <darren_hsu@phison.com>  申請網頁使用帳號，謝謝");
		</script>-->
					Home > Log Summary( Search MP log by WO )
            </ol>

            <!-- Content-->
            <div id="body">
<form method="post" name="mdata" action="LogSummary.jsp">
WO:&nbsp;<input type=text name="WO" value="<%=WO%>">
移除重複CTL_ID:&nbsp;<select name="SkipDouble">
  <option value="1" <%=SkipDouble.compareTo("1")==0 ? "selected":""%>>Y</option>
  <option value="0" <%=SkipDouble.compareTo("1")!=0 ? "selected":""%>>N</option>
</select>
<input type="submit" name="search" value="doSearch">
</form>
<%
	if ( WO.length()>10 ) {
		String pWS_ID="";
		String moYM = "PELogSr_20"+WO.substring(4,8);
		//511-181017127
		//String sql = "use "+moYM+";select WS_ID,ID_01,count(*)cnt from  mfg_test_result where WO='"+WO+"' and ID_01<>'N/A' \n";
		//sql += " group by WS_ID,ID_01\n order by WS_ID, count(*) desc, ID_01";
		
		String sql = "use TIPTOP;select * from csfzr109 where PRODUCT_NUM='"+WO+"' ";
		//out.println("<pre>"+sql+"</pre>");
		
		Statement stmt = conn.createStatement();
		ResultSet rs=stmt.executeQuery(sql);
		int quantity=1;
        String product = "";
		if ( rs.next() ) {
			quantity = rs.getInt("QUANTITY");
            product = rs.getString("PRODUCT");
            String wostatus = rs.getString("CLOSE_STATUS");
            if ( wostatus.indexOf("3")!=-1 ) {
                wostatus="close";
            }
            else {
                wostatus="open";
            }
%>
			工單:&nbsp;<%=rs.getString("PRODUCT_NUM")%><br>
			數量:&nbsp;&nbsp;<%=rs.getString("QUANTITY")%><br>
            回貨數量:&nbsp;&nbsp;<%=rs.getString("PRODUCTION_QUANTITY")%><br>
            Status:&nbsp;&nbsp;<%=wostatus%><br>
			產品:&nbsp;&nbsp;<%=rs.getString("PRODUCT")%><br>
			PCBA:&nbsp;&nbsp;<%=rs.getString("PCBA")%><br>
			IC:&nbsp;&nbsp;<%=rs.getString("IC")%><br>
			FW Ver:&nbsp;&nbsp;<%=rs.getString("FW_VER")%>-<%=rs.getString("FW_MINOR_CODE")%><br>
			Flash:&nbsp;&nbsp;<%=rs.getString("FLASH_PROVIDER")%>-<%=rs.getString("Flash_SPEC6")%>-<%=rs.getString("FLASH_CAPACITY")%><br>
			Flash Package:&nbsp;&nbsp;<%=rs.getString("FLASH_PACKAGE")%>*<%=rs.getString("FLASH_NUM")%><br>
<%		
		}
		
		// sql = 
            // "use "+moYM+"; \n"+
            // "select ctl_lot,ws_id,id_01,count(*) cnt into #tmp from mfg_test_result  \n"+
            // "where WO='"+WO+"'  \n"+
            // "group by ctl_lot,ws_id,id_01  \n"+
            // "; \n"+
            // "select ws_id,id_01,count(*) cnt from #tmp  \n"+
            // "group by ws_id,id_01  \n"+
            // "order by ws_id,count(*) desc,id_01 \n";

        //if ( SkipDouble.compareTo("1")!=0 ) {
            sql = "select * from LogSystem.dbo.mfg_test_summary where WO='"+WO+"' and SkipDouble="+SkipDouble+" order by ws_id,cnt desc,id_01";
        //}
		
		//out.println("<pre>"+sql+"</pre>");
		
		java.text.DecimalFormat dformat = new java.text.DecimalFormat("0.00");
		rs=stmt.executeQuery(sql);
		while (rs.next()) {
			String WS_ID = rs.getString("WS_ID");
			String ID_01 = rs.getString("ID_01");
			int cnt = rs.getInt("cnt");
			if ( pWS_ID.compareTo(WS_ID)!=0 ) {
				if ( pWS_ID.length()!=0 ) {
%>
		</table></div>
<%				
				}
%>

<%		
				pWS_ID = WS_ID;
%>
		<div style="width: 200px; display: inline-block;vertical-align:top;">
		<table id="customers" >
			<tr><th align="center" colspan=3 ><%=WS_ID_FIX( WS_ID, product )%></th></tr>
<%		   }
%>			
			<tr>
			<td align="center" ><a href=".\ErrDetail.jsp?WO=<%=WO%>&WS_ID=<%=WS_ID%>&ID_01=<%=ID_01%>&SkipDouble=<%=SkipDouble%>"><%=ID_01%></td>
			<td align="center" ><%=cnt%></td>
			<td align="center" ><%=dformat.format((100.0*cnt)/quantity)%>%</td>
			</tr>
<%
        }
%>
		</table>
		<br>&nbsp;
		</div>
<%		
        // if ( SkipDouble.compareTo("1")==0 ) {
            // stmt.execute("drop table #tmp");
        // }
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






上面是我的原始程式碼，
我想增加功能如以下，能夠取得連入此網站的使用者資訊並傳到資料庫
    // 記錄使用者資訊
    String userIP = request.getRemoteAddr();
    String userName = request.getRemoteUser();
    if (userName == null) {
        userName = "Unknown";
    }
    String reportName = "LogSummary";
    Timestamp clickTime = new Timestamp(System.currentTimeMillis());


    String insertSQL = "insert into [192.168.8.44].[WebPlatForm].[dbo].[WebPlatForm_Counter] (IP,[USER],REPORT,CLICK_TIME) values  (?, ?, ?, ?)";


資料庫位置在insertSQL這個變項，請幫我改好程式碼並給我完整程式碼。
