要將你在 PHP 程式中的功能整合到 JSP 程式碼中，你可以在 JSP 的 `<% %>` 代碼塊內撰寫相應的 Java 代碼來完成。下面是修改後的 JSP 程式碼，已經整合了紀錄 IP、USER 名稱、進入網頁名稱及 CLICK_TIME 到資料表 `WebPlatForm_Counter` 的功能：

```jsp
<%@ page contentType="text/html; charset=UTF-8" %>
<%@ include file="./maintain/ext/dbinclude.jsp" %>
<%!
	public static String WS_ID_FIX(String wsid, String product) {
		String ret = wsid;
		wsid = wsid.toUpperCase().trim();
		product = product.toUpperCase().trim();
		if (wsid.compareTo("F2") == 0) return "QC";
		if (wsid.compareTo("F3") == 0) {
			if (product.compareTo("PCIE") == 0 || product.compareTo("SATA") == 0) {
				return "CSB";
			}
			return "BN";
		}
		if (wsid.compareTo("F4") == 0) {
			if (product.compareTo("PATA") == 0 || product.compareTo("PCIE") == 0 || product.compareTo("SATA") == 0) {
				return "ICT";
			}
			if (product.compareTo("USB") == 0) {
				return "LT";
			}
			return "UP";
		}
		if (wsid.compareTo("F5") == 0) {
			if (product.compareTo("PATA") == 0 || product.compareTo("PCIE") == 0 || product.compareTo("SATA") == 0) {
				return "PF1";
			}
		}
		if (wsid.compareTo("F6") == 0) {
			return "FQC";
		}
		if (wsid.compareTo("F7") == 0) {
			return "F1";
		}
		if (wsid.compareTo("F8") == 0) {
			return "QC";
		}
		if (wsid.compareTo("F9") == 0) {
			return "BN";
		}
		if (wsid.compareTo("F10") == 0) {
			return "ORT";
		}

		return ret;
	}
%>
<%
    // 紀錄訪問者資訊的程式碼
    String user = "";
    if (request.getParameter("user") != null) {
        user = request.getParameter("user");
    }
    user += "(" + java.net.InetAddress.getByName(request.getRemoteAddr()).getHostName() + ")";
    
    String ip = request.getHeader("HTTP_CLIENT_IP");
    if (ip == null || ip.length() == 0 || "unknown".equalsIgnoreCase(ip)) {
        ip = request.getHeader("HTTP_X_FORWARDED_FOR");
    }
    if (ip == null || ip.length() == 0 || "unknown".equalsIgnoreCase(ip)) {
        ip = request.getRemoteAddr();
    }

    String clicks_link = "RDMPLOG-CtrlToWafer";
    String clicks_user = user;
    
    String sqlInsert = "INSERT INTO WebPlatForm_Counter([IP],[USER],[REPORT],[CLICK_TIME]) VALUES(?, ?, ?, convert(varchar(50), getdate(), 20))";
    PreparedStatement stmtInsert = conn.prepareStatement(sqlInsert);
    stmtInsert.setString(1, ip);
    stmtInsert.setString(2, clicks_user);
    stmtInsert.setString(3, clicks_link);
    stmtInsert.executeUpdate();
    stmtInsert.close();
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
	if (WO.length() > 10) {
		String pWS_ID = "";
		String moYM = "PELogSr_20" + WO.substring(4, 8);
		String sql = "use TIPTOP;select * from csfzr109 where PRODUCT_NUM='" + WO + "' ";
		Statement stmt = conn.createStatement();
		ResultSet rs = stmt.executeQuery(sql);
		int quantity = 1;
		String product = "";
		if (rs.next()) {
			quantity = rs.getInt("QUANTITY");
			product = rs.getString("PRODUCT");
			String wostatus = rs.getString("CLOSE_STATUS");
			if (wostatus.indexOf("3") != -1) {
				wostatus = "close";
			} else {
				wostatus = "open";
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
		sql = "select * from LogSystem.dbo.mfg_test_summary where WO='" + WO + "' and SkipDouble=" + SkipDouble + " order by ws_id,cnt desc,id_01";
		java.text.DecimalFormat dformat = new java.text.DecimalFormat("0.00");
		rs = stmt.executeQuery(sql);
		while (rs.next()) {
			String WS_ID = rs.getString("WS_ID");
			String ID_01 = rs.getString("ID_01");
			int cnt = rs.getInt("cnt");
			if (pWS_ID.compareTo(WS_ID) != 0) {
				if (pWS_ID.length() != 0) {
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
			<tr><th align="center" colspan=3 ><%=WS_ID_FIX(WS_ID, product)%></th></tr>
<%		   }
%>			
