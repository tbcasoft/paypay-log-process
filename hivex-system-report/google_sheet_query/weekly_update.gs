function updateHIVEXSystemReport() {

  var curWeekPage = createWeekPage();
  setWeeklyReportData(curWeekPage);
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  ss.getSheetByName("SetUp").hideSheet();
  ss.getSheetByName("reportTemplate").hideSheet();

}


function createWeekPage() {
  var oldWeekNum = getNumSheets() - 2;
  var curWeekNum = oldWeekNum + 1;

  var ss = SpreadsheetApp.getActiveSpreadsheet();

  var template = ss.getSheetByName("reportTemplate");
  var curWeekName = 'WK' + curWeekNum.toString();

  template.copyTo(ss).setName(curWeekName);
  var curWeekPage = ss.getSheetByName(curWeekName);
  curWeekPage.showSheet();

  return curWeekPage;
}

function setWeeklyReportData(curWeekPage) {
  setReportMetaData(curWeekPage);

  var connectionName = 'visa-fx-05006aa44b45542b.elb.ap-southeast-1.amazonaws.com:1234';
  var user = 'aws_lambda';
  var userPwd = '&o17r%FK$Ft8';
  var db = 'hour_qr';
  var dbUrl = 'jdbc:mysql://' + connectionName + '/' + db + '?useSSL=false';  
  try {
    var conn = Jdbc.getConnection(dbUrl, user, userPwd);
  } catch (e) {
    Logger.log("Connection error: " + e);
  } 

  setReportIssuerData(conn, curWeekPage);
  setReportWeeklyStats(conn, curWeekPage);

}

function setReportMetaData(curWeekPage) {
  var pageName = curWeekPage.getName();

  var dateCell = curWeekPage.getRange(`${pageName}!date`);
  dateCell.setValue(dateCell.getValue().split("WK")[0] + curWeekPage.getName());

  var today = new Date();
  today.setHours(0);
  today.setMinutes(0);
  today.setSeconds(0);
  today.setMilliseconds(0);
  // console.log(`today is ${today}`);

  var monday = new Date(today);
  monday.setDate(today.getDate() - 7);
  
  var sunday = new Date(monday);
  sunday.setDate(monday.getDate() + 6);
  // console.log(`sunday is ${sunday}`);

  var startDateCell = curWeekPage.getRange(`${pageName}!startDate`);
  var endDateCell = curWeekPage.getRange(`${pageName}!endDate`);
  var durationCell = curWeekPage.getRange(`${pageName}!duration`);

  startDateCell.setValue(monday);
  endDateCell.setValue(sunday);
  durationCell.setFormula("=(G1-E1+1)*24*60");
}

function setReportIssuerData(conn, curWeekPage) {
  var pageName = curWeekPage.getName();

  var issuer_stmt = conn.prepareStatement(`
      SELECT hsri.issuer as Issuer, 
      hsri.get_invoice_latency_median as InvoiceMedian, 
      hsri.get_invoice_latency_p99 as InvoiceP99, 
      hsri.pay_latency_median as PayMedian, 
      hsri.pay_latency_p99 as PayP99, 
      hsri.conf_page_latency_median as ConfPageMedian, 
      hsri.conf_page_latency_p99 as ConfPageP99 
      FROM hour_qr.hivex_system_report_issuers hsri
      WHERE week_date = ? AND acquier = ?
    `);

  var acquier = "PPY";

  var startDate = curWeekPage.getRange(`${pageName}!startDate`).getValue();
  var startDateStr = getDateFormat(startDate);
  // console.log(`the formmatted startDateStr is: ${startDateStr}`);

  issuer_stmt.setString(1, startDateStr);
  issuer_stmt.setString(2, acquier);

  var issuer_results = issuer_stmt.executeQuery();
  var columnCount = issuer_results.getMetaData().getColumnCount();

  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var issuerList = ss.getRange("setUp!issuers").getValue().split("/");
  var data = {};

  for(var i = 0; i < issuerList.length; i++) {
    data[issuerList[i]] = [];
  }

  while(issuer_results.next()) {
    var row = [];
    for (var col = 1; col <= columnCount; col++) {
      row.push(issuer_results.getString(col));
    }
    if (row[0] == "ESB") {
      data["ESUN"] = row.slice(1);
    } 
    else {
      data[row[0]] = row.slice(1);
    }
  }

  var dataNames = ["Invoice", "Pay", "ConfPage"];
  var percentage = ["P50", "P99"];
  for(var i = 0; i < issuerList.length; i++) {
    var issuerName = issuerList[i];
    var issuerData = data[issuerName];

    var prefix = pageName + "!" + issuerName;
    for (var j = 0; j < dataNames.length; j++) {
      var dataName = dataNames[j];
      curWeekPage.getRange(`${prefix}${dataName}${percentage[0]}`).setValue(issuerData[j*2]);
      curWeekPage.getRange(`${prefix}${dataName}${percentage[1]}`).setValue(issuerData[j*2 + 1])
    }
  }

  issuer_results.close();
  issuer_stmt.close();
}

function setReportWeeklyStats(conn, curWeekPage) {
  var pageName = curWeekPage.getName();

  var weekly_stat_stmt = conn.prepareStatement(`
      SELECT hsrws.data_name as DataName, 
      hsrws.data_value as DataValue 
      FROM hour_qr.hivex_system_report_weekly_stat hsrws
      WHERE week_date = ?
    `);

  var startDate = curWeekPage.getRange(`${pageName}!startDate`).getValue();
  var startDateStr = getDateFormat(startDate);
  // console.log(`the formmatted startDateStr is: ${startDateStr}`);
  
  weekly_stat_stmt.setString(1, startDateStr);

  var weekly_stat_result = weekly_stat_stmt.executeQuery();

  while (weekly_stat_result.next()) {
    var dataName = weekly_stat_result.getString(1);
    var dataValue = weekly_stat_result.getString(2);
    switch (dataName) {
      case "hivex_network_peak_request":
        curWeekPage.getRange(`${pageName}!hixevPeakRequest`).setValue(dataValue);
        break;
      case "num_onboarded_merchant_services":
        handleNumOnboardedMerchantServices(pageName, dataValue);
        break;
    }
  }
}

function handleNumOnboardedMerchantServices(pageName, thisWeekVal) {
  var ss = SpreadsheetApp.getActiveSpreadsheet();

  var numMerchantCell = ss.getRange(`${pageName}!numOnboardedMerchantServices`);
  var lastWeekNum = numMerchantCell.getValue();
  var increaseValCell = ss.getRange(`${pageName}!increaseFromLastWeek`);

  numMerchantCell.setValue(thisWeekVal);
  increaseValCell.setFormula(`=SUM('${pageName}'!numOnboardedMerchantServices)-${lastWeekNum.toString()}`);

  numMerchantCell.setNumberFormat("#,##0");
  increaseValCell.setNumberFormat("#,##0");

  var templateMerchantCell = ss.getRange("reportTemplate!numOnboardedMerchantServices");
  templateMerchantCell.setValue(thisWeekVal);
  templateMerchantCell.setNumberFormat("#,##0");
}

function getNumSheets() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sheets = ss.getSheets();
  var numberOfSheets = sheets.length;
  
  return numberOfSheets;
}

function getDateFormat(date){
  var tzoffset = (new Date()).getTimezoneOffset() * 60000;
  var dateStr = new Date(date - tzoffset).toISOString().split('T')[0];
  return dateStr;
}

