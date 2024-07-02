function getDailyOverwatchQuery() {

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

  var stmt = conn.prepareStatement(`
      SELECT dod.date as Date, 
      dod.acquier as Acquier,
      dod.issuer as Issuer, 
      dod.rejected_job_models_invoice_count as Invoice, 
      dod.rejected_jobmodels_RFP_count as RFP,
      dod.api_gen_target_count as GenTarget,
      dod.payments_CPM_count as CPMCount,
      dod.payments_CPM_dest_amount as CPMAmount,
      dod.payments_MPM_count as MPMCount,
      dod.payments_MPM_dest_amount as MPMAmount,
      dod.refunds_count as RefundsCount,
      dod.refunds_sum_of_amount as RefundsAmount,
      dod.termination_OPT_OUT as OptOut, 
      dod.termination_EXPIRED_CODE as ExpiredCode, 
      dod.termination_ACQUIRER_VALIDATION as AcquirerValidation
      FROM hour_qr.daily_overwatch_dashboard dod  
      WHERE date = ? AND acquier = ?
      ORDER BY date
    `);
  
  var issuerList = getIssuers();
  var acquier = getAcquier();
  var raw_data_sheet = SpreadsheetApp.getActive().getSheetByName(issuerList.join("/"));
  
  var lastRow = getLastRow(); 
  
  var lastDateStr = raw_data_sheet.getRange("A" + lastRow.toString()).getValue();
  var lastDate = stringToDate(lastDateStr);

  var curDate = new Date(lastDate);
  curDate.setDate(lastDate.getDate() + 1);
  var db_format_curDate = formatDbDate(curDate);

  stmt.setString(1, db_format_curDate);
  stmt.setString(2, acquier);

  var results = stmt.executeQuery();
  var dbColumnCount = results.getMetaData().getColumnCount();

  var unsortedData = [];

  while (results.next()) {
    var row = [];
    for(var col = 3; col <= dbColumnCount; col ++) {
      row.push(results.getString(col));
    }
    unsortedData.push(row);
  }

  var data = sortDataByIssuer(issuerList, unsortedData);

  var columnCount = data[0].length;

  var numIssuers = data.length;

  var anchorRanges = getRawDataNamedRangeOffsets();

  for(var col = 0; col < columnCount - 3; col++) {
    var dataTotalCell = offsetNamedRange(anchorRanges[col], raw_data_sheet, lastRow);

    for(var issuer = 0; issuer < numIssuers; issuer++) {
      var val = Number(data[issuer][col]);
      var targetRange = dataTotalCell.offset(0, issuer + 1)
      targetRange.setValue(val);
    }
    var firstIssuerCell = dataTotalCell.offset(0, 1).getA1Notation();
    var lastIssuerCell = dataTotalCell.offset(0, numIssuers).getA1Notation();

    dataTotalCell.setFormula(`=SUM(${firstIssuerCell}:${lastIssuerCell})`)
  }


  var cpmTerminationNamedRanges = {
    9: '_QR_CPMOptOut',
    10: '_QR_CPMExpiredCode',
    11: '_QR_CPMAcquirerValidation'
  }
  for(var rejectCode = 3; rejectCode > 0; rejectCode-=1) {
    for(var issuer = 0; issuer < numIssuers; issuer++) {
      var index = columnCount - rejectCode;
      var val = Number(data[issuer][index]);
    
      var targetRange = offsetNamedRange(cpmTerminationNamedRanges[index], raw_data_sheet, lastRow);
      targetRange.setValue(targetRange.getValue() + val);
    }
  }

  var qrData = getDailyQrAnalysisResult(conn, curDate);
  calculateAnalysis(numIssuers, qrData, lastRow, raw_data_sheet);

  var display_date = sheetDate(db_format_curDate);

  var curRow = lastRow + 1;
  raw_data_sheet.insertRowAfter(curRow);
  var headDateCell = raw_data_sheet.getRange("A" + curRow.toString());
  headDateCell.setValue(display_date);


  updateRowCount();

  results.close();
  stmt.close();

  setUU(raw_data_sheet, numIssuers, lastRow);
  updatePPFailureRate(display_date);
}

function setUU(raw_data_sheet, numIssuers, lastRow) {
  var uuTitleCell = offsetNamedRange('TotalUU', raw_data_sheet, lastRow);
  for (var issuer = 0; issuer <= numIssuers; issuer++) {
    uuTitleCell.offset(0, issuer).setValue(0);
  }
}
function offsetNamedRange(rangeName, raw_data_sheet, lastRow) {
  var namedRange = raw_data_sheet.getRange(rangeName);
  var col = namedRange.getColumn();
  var targetRange = raw_data_sheet.getRange(lastRow + 1, col);
  return targetRange;
}


function stringToDate(dateStr) {
  return new Date(dateStr);
}

function formatDbDate(date) {
  var tzoffset = (new Date()).getTimezoneOffset() * 60000;
  var dateStr = new Date(date - tzoffset).toISOString()
  return dateStr.substring(0,10);
}

function sheetDate(date) {
  return date.substring(5, 7) + "/" + date.substring(8) + "/" + date.substring(0, 4) 
}


function getRawDataNamedRangeOffsets() {
  var dataToNamedRanges = {
    0: 'totalIncompleteMPMPaymentFailedOnIssuer',
    1: 'totalRequestForPaymentRejectionIssuer',
    2: 'totalGenerateQRRequest',
    3: 'totalCPMPaymentSuccess',
    4: 'totalCPMTransactionAmountJPY',
    5: 'totalMPMPaymentSuccess',
    6: 'totalMPMTransactionAmountJPY',
    7: 'totalRefundSuccess',
    8: 'totalRefundAmountJPY'
  }
  return dataToNamedRanges;
}

function getIssuers() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var numIssuers = ss.getRange('MetaData!_META_DATA_numIssuers').getValue();
  var issuerCell = ss.getRange('MetaData!_META_DATA_issuerTitle');
  // Logger.log(`num issuer is: ${numIssuers}`);
  var issuerList = [];
  for(var i = 1; i <= numIssuers; i++) {
    var issuer = issuerCell.offset(0, i).getValue();
    issuerList.push(issuer);
  }
  console.log(`issuer list is ${issuerList}`);
  return issuerList;
}

function getAcquier() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var acquierCell = ss.getRange("MetaData!_META_DATA_acquierOne");
  return acquierCell.getValue();
}

function sortDataByIssuer(issuerList, unsortedData) {
  var issuersInData = unsortedData.map(x => x[0]);
  var presentIssuers = issuerList.filter(issuer => issuersInData.includes(issuer));
  presentIssuers = presentIssuers.filter(issuer => issuerList.includes(issuer));

  var sortedData = new Array(presentIssuers.length);
  for (var i = 0; i < presentIssuers.length; i++) {
    var targetIssuer = presentIssuers[i];
    for (var issuer = 0; issuer < unsortedData.length; issuer++) {
      if (unsortedData[issuer][0] == targetIssuer) {
        sortedData[i] = unsortedData[issuer];
      }
    }
  }
  return sortedData.map(x => x.slice(1));
}

function getLastRow() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var rowNumber = ss.getRange("MetaData!_META_DATA_numRows").getValue();
  return rowNumber;
}

function updateRowCount() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var rowCountCell = ss.getRange("MetaData!_META_DATA_numRows");
  var newRowCount = rowCountCell.getValue() + 1;
  rowCountCell.setValue(newRowCount);
}