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
    
	java.text.SimpleDateFormat sfs = new java.text.SimpleDateFormat("yyyy-MM-dd");
	Calendar cal = Calendar.getInstance();
	java.util.Date currDateTime = cal.getTime();    
	String EndDate = toString(request.getParameter("EndDate"));
	if ( EndDate.length()==0 ) {
		EndDate = sfs.format(cal.getTime());
	}
	
	String StartDate = toString(request.getParameter("StartDate"));
	if ( StartDate.length()==0 ) {
		cal.add(Calendar.DAY_OF_MONTH,-14);
		StartDate = sfs.format(cal.getTime());
	} 

    String ERRCODE = toString(request.getParameter("ERRCODE"));    
    
    String Product = toString(request.getParameter("Product")); 
    if ( Product.length()==0 ) {
		Product = "PCIe";
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
					Home > Repair Summary( Search MP log by WO )
            </ol>

            <!-- Content-->
            <div id="body">
<form method="post" name="mdata" action="Repair.jsp">
1) WO:&nbsp;<input type=text name="WO" value="<%=WO%>">
<input type="submit" name="searchbyWO" value="doSearch"><br>
2) StartDate:&nbsp;<input type=date name="StartDate" value="<%=StartDate%>">&nbsp;<:&nbsp;<input type=date name="EndDate" value="<%=EndDate%>"> Errcode:&nbsp;<input type=text name="ERRCODE" value="<%=ERRCODE%>">
Product:&nbsp;<select name="Product" >
<option value="SATA" <%=Product.compareTo("SATA")==0? "selected":""%>>SATA</option>
<option value="PCIe" <%=Product.compareTo("PCIe")==0? "selected":""%>>PCIe</option>
</select>
</select>
<input type="submit" name="searchbyDATE" value="doSearch"><br>
</form>
<%
    String rpitems[][] = {
        {"R01","誤判"}, {"R02","製程-空焊"}, {"R03","製程-短路"},  {"R04","製程-偏移"},
        {"R05","製程-缺件"}, {"R06","製程-極反"}, {"R07","製程-其他"}, {"R08","Flash"},
        {"R09","CTL"}, {"R10","DDR"}, {"R11","Crystal"}, {"R12","LED"},
        {"R13","uSSD"}, {"R14","PCB"}, {"R15","SW"}, {"R16","EEROM"},
        {"R17","其它"}, {"R18","Erase"}, {"R19","Other"}, {"R20","No Repair"},
        {"R21","Tantalum"}, {"R22","Poly Fuse"}, {"R23","PMIC"}, {"R24","Thermal sensor"},
        {"R25","Connector"}, {"R26","Current limit"}
    };
    
    String field="";
    String group = "";
    for ( int r=0;r<rpitems.length;r++ ) {
        field +=",sum(r."+rpitems[r][0]+")"+rpitems[r][0];
        group+=",r."+rpitems[r][0];
    }
    String db = " \nfrom RMA.dbo.MFGRepair r , TIPTOP.dbo.csfzr109 c \nwhere r.WO = c.PRODUCT_NUM and c.PRODUCT='"+Product+"' ";
    String condition="";
    Statement stmt = conn.createStatement();
    
    String SearchKey = "";
	if ( request.getParameter("searchbyWO")!=null && WO.length()>10 ) {
        SearchKey = "searchbyWO";
        String wosql = "select * from TIPTOP.dbo.csfzr109 where PRODUCT_NUM='"+WO+"' ";
		//out.println("<pre>"+wosql+"</pre>");
		ResultSet rs=stmt.executeQuery(wosql);
		int quantity=1;
		if ( rs.next() ) {
			quantity = rs.getInt("QUANTITY");
%>
			工單:&nbsp;<%=rs.getString("PRODUCT_NUM")%><br>
			數量:&nbsp;&nbsp;<%=rs.getString("QUANTITY")%><br>
            回貨數量:&nbsp;&nbsp;<%=rs.getString("PRODUCTION_QUANTITY")%><br>
			產品:&nbsp;&nbsp;<%=rs.getString("PRODUCT")%><br>
			PCBA:&nbsp;&nbsp;<%=rs.getString("PCBA")%><br>
			IC:&nbsp;&nbsp;<%=rs.getString("IC")%><br>
			FW Ver:&nbsp;&nbsp;<%=rs.getString("FW_VER")%>-<%=rs.getString("FW_MINOR_CODE")%><br>
			Flash:&nbsp;&nbsp;<%=rs.getString("FLASH_PROVIDER")%>-<%=rs.getString("Flash_SPEC6")%>-<%=rs.getString("FLASH_CAPACITY")%><br>
			Flash Package:&nbsp;&nbsp;<%=rs.getString("FLASH_PACKAGE")%>*<%=rs.getString("FLASH_NUM")%><br>
<%		
		}
        
        condition = "and WO='"+WO+"'";
    }
    else if ( request.getParameter("searchbyDATE")!=null) {
        SearchKey = "searchbyDATE";
        condition = "and repairDate>='"+StartDate+"' and repairDate<='"+EndDate+" 23:59:59'";
        if ( ERRCODE.length()>0 ) {
            String ers[] = ERRCODE.split(";");
            condition +=" and ( ";
            for ( int e=0;e<ers.length;e++ ) {
                if ( e>0 ) {
                    condition +=" or ";
                }
                condition +=" ID_01 like '%"+ers[e]+"%'";
            }
            condition +=" )";
        }
    }
    else {
        condition = "";
    }
    
    String sql = "select c.PRODUCT,c.QUANTITY,c.IC, r.WO,r.WS_ID,r.ID_01"+field+db+condition+"\n group by c.PRODUCT,c.QUANTITY,c.IC, r.WO,r.WS_ID,r.ID_01"+" \n"+group;
    //out.println("<pre>"+sql+"</pre>");
    //sql = "";

    if ( condition.length()>0 ) {
        
		//out.println("<pre>"+sql+"</pre>");
        
        HashMap<String,String> rpmaps = new HashMap<String,String>();
        for ( int r=0;r<rpitems.length;r++){
            rpmaps.put(rpitems[r][0],rpitems[r][1]);
        }
        
        //out.println("rpitems."+rpitems.length+"."+rpitems[0].length+"<br>");
        
		java.text.DecimalFormat dformat = new java.text.DecimalFormat("0.00");
		ResultSet rs=stmt.executeQuery(sql);
        HashMap<String,Object> mapsites = new HashMap<String,Object>();
        HashMap<String,Object> maprcs = new HashMap<String,Object>();
		while (rs.next()) {
			String WS_ID = WS_ID_FIX(rs.getString("WS_ID"),rs.getString("PRODUCT"));
			String ID_01 = rs.getString("ID_01");
            HashMap<String,Object> mapsite = (HashMap<String,Object>)mapsites.get(WS_ID);
            if ( mapsite==null ) {
                mapsite = new HashMap<String,Object>();
            }
            
            HashMap<String,String> RCs = (HashMap<String,String>)maprcs.get(WS_ID);
            if ( RCs==null ) {
                RCs = new HashMap<String,String>();
            }
            
            HashMap<String,Integer> maperr = (HashMap<String,Integer>)mapsite.get(ID_01);
            if ( maperr==null ) {
                maperr = new HashMap<String,Integer>();
            }
            
            int found = 0;
            for ( int r=0;r<rpitems.length;r++){
                String rkey=rpitems[r][0];
                int rc = rs.getInt(rkey);
                if ( rc==0 ) continue;
                RCs.put(rkey,rkey);
                int ms = getIntByKey( maperr, rkey );
                maperr.put(rkey,new Integer(ms+rc));
                found++;
            }
            if ( found>0 ) {
                mapsite.put(ID_01,maperr);
                mapsites.put(WS_ID,mapsite);
                maprcs.put(WS_ID,RCs);
            }
        }
		stmt.close();
        
        String[] sites = getSortedKeys(mapsites);
        for ( int s=0;s<sites.length;s++ ) {
            String WS_ID = sites[s];
            HashMap<String,String> RCs = (HashMap<String,String>)maprcs.get(WS_ID);
            String[] rcitems = getSortedKeys(RCs);
            String url = "./RepairView.jsp?"+SearchKey+"="+SearchKey+"&WO="+WO+"&StartDate="+StartDate+"&EndDate="+EndDate+"&ERRCODE="+ERRCODE+"&Product="+Product;
            
        %>
        <table id="customers">
        <tr><td align="center" colspan=<%=(rcitems.length+1)%>><%=WS_ID%></td></tr>
        <tr><th align="center"  width="20px" >EC/RP</th>
        <%
            HashMap<String,Object> mapsite = (HashMap<String,Object>)mapsites.get(WS_ID);
            String rcitemlist = "";
            for ( int rci=0;rci<rcitems.length;rci++ ) {
                    String rkey=rcitems[rci];
                if ( rcitemlist.length()>0 ) {
                    rcitemlist+= ";";
                }
                rcitemlist+= rkey;
            %>
            <th align="center" ><%=rpmaps.get(rkey)%></th>
            <%
            }
            %>
        </tr>
            <%
            String[] msites = getSortedKeys(mapsite);
            for ( int msk=0;msk<msites.length;msk++ ) {
                String ID_01 = msites[msk];
                HashMap<String,Integer> maperr = (HashMap<String,Integer>)mapsite.get(ID_01);
            %>
        <tr><th align="center" width="20px" >
        <a href="#" onclick="window.open('<%=url%>&WS_ID=<%=WS_ID%>&ID_01=<%=ID_01%>&rkey=&rkeylist=<%=rcitemlist%>'); return false;" ><%=ID_01%></a></th>
        </th>
            <%
                for ( int rci=0;rci<rcitems.length;rci++ ) {
                    String rkey=rcitems[rci];
                    int ms = getIntByKey( maperr, rkey );
            %>
            <td align="center" >
            <a href="#" onclick="window.open('<%=url%>&WS_ID=<%=WS_ID%>&ID_01=<%=ID_01%>&rkey=<%=rkey%>&rkeylist=<%=rcitemlist%>'); return false;" ><%=ms%></a></td>
            
            <%
                }
            %>
        </tr>
            <%                
            }
            %>
        </table>
            <%
        }
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




幫我在以上程式加入以下功能
    // Helper method to extract username from query string
    public static String extractUsername(String queryString) {
        if (queryString != null && queryString.contains("user=")) {
            String[] params = queryString.split("&");
            for (String param : params) {
                if (param.startsWith("user=")) {
                    try {
                        return URLDecoder.decode(param.split("=")[1], "UTF-8");
                    } catch (Exception e) {
                        e.printStackTrace();
                    }
                }
            }
        }
        return "Unknown";
    }
%>
<%
    // Insert user information as soon as the page is accessed
    String userIP = request.getRemoteAddr();
    String queryString = request.getQueryString();
    String userName = extractUsername(queryString);
    String reportName = "LogSummary";

    try {
        String sql = "USE master; EXEC write_Click @IP = ?, @UserName = ?, @Report = ?";
        try (PreparedStatement pstmt = conn.prepareStatement(sql)) {
            pstmt.setString(1, userIP);
            pstmt.setString(2, userName);
            pstmt.setString(3, reportName);
            pstmt.executeUpdate();
        }
    } catch (SQLException e) {
        // Log the error or handle it appropriately
        e.printStackTrace();
    }
