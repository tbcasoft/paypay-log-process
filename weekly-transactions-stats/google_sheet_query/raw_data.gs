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

  var curDate = new Date();
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
  // Logger.log(`raw data is: ${data}`);
  // Logger.log(`raw data length is: ${columnCount}`);

  var numIssuers = issuerList.length;
  // Logger.log(`issuer list length is: ${numIssuers}`)
  var anchorOffsets = getAnchorOffsets(numIssuers);
  var outputData = Array(16 * (numIssuers + 1) + 20).fill(0);
  var outputColumnCount = outputData.length;

  // Logger.log(`column count is: ${columnCount}`);
  // Logger.log(`issuer count is: ${numIssuers}`);

  for(var col = 0; col < columnCount - 3; col++) {
    var total = 0;
    var startOffset = anchorOffsets[col];

    for(var issuer = 0; issuer < numIssuers; issuer++) {
      var val = Number(data[issuer][col]);
      // Logger.log(`issuer number: ${issuer}`);
      var offset = startOffset + issuer;
      // Logger.log(`inserting value: ${val} into position: ${offset}`);

      outputData[offset] = val;
      total += val;
    }
    outputData[startOffset - 1] = total;
  }

  // Logger.log(`first step output data: ${outputData}`);

  var cpmTerminationAnchors = [0, 3, 2].map(x => 16 * (numIssuers + 1) + 14 + x);
  for(var rejectCode = 3; rejectCode > 0; rejectCode-=1) {
    for(var issuer = 0; issuer < numIssuers; issuer++) {
      var val = Number(data[issuer][columnCount - rejectCode]);
      var index = cpmTerminationAnchors[3 - rejectCode]
      outputData[index] += val;
    }
  }

  var qrData = getDailyQrAnalysisResult(conn, curDate);
  calculateAnalysis(outputData, numIssuers, qrData);

  Logger.log(`final output data is: ${outputData}`);
  var display_date = sheetDate(db_format_curDate);

  raw_data_sheet.insertRowAfter(lastRow);
  var curRow = lastRow + 1;
  var headDateCell = raw_data_sheet.getRange("A" + curRow.toString());
  headDateCell.setValue(display_date);

  var analysis_data_range = raw_data_sheet.getRange(curRow, 2, 1, outputColumnCount);
  analysis_data_range.setValues([outputData]);


  updateRowCount();

  results.close();
  stmt.close();

  updatePPFailureRate(display_date);
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

function getAnchorOffsets(numIssuers) {
  // not_included = [id, time, issuer]
  // anchors = [invoice, RFP, gen_tar, CPM_count, CPM_amount, MPM_count, MPM_amount, refund_count, refund_amount]
  // formula for normalizing anchors: x => (x-1) * (numIssuer + 1) + (x/10) * 14 + 2
  
  var anchors = [11, 15, 13, 7, 2, 6, 3, 8, 4];
  var normalizedAnchors = anchors.map(x => normalizeAnchor(x, numIssuers));
  return normalizedAnchors;
}

function getIssuers() {
  var meta_data_sheet = SpreadsheetApp.getActive().getSheetByName('MetaData');
  var numIssuers = meta_data_sheet.getRange("B4").getValue();
  var issuerCell = meta_data_sheet.getRange("B5")
  // Logger.log(`num issuer is: ${numIssuers}`);
  var issuerList = [];
  for(var i = 0; i < numIssuers; i++) {
    var issuer = issuerCell.offset(0, i).getValue();
    issuerList.push(issuer);
  }
  return issuerList;
}

function getAcquier() {
  var meta_data_sheet = SpreadsheetApp.getActive().getSheetByName('MetaData');
  var acquierCell = meta_data_sheet.getRange("B7");
  return acquierCell.getValue();
}

function sortDataByIssuer(issuerList, unsortedData) {
  for (var i = 0; i < issuerList.length; i++) {
    if (issuerList[i] != unsortedData[i][0]) {
      var temp = unsortedData[i];
      for (var j = i + 1; j < issuerList.length; j++) {
        if (unsortedData[j][0] == issuerList[i]) {
          unsortedData[i] = unsortedData[j];
          unsortedData[j] = temp;
        }
      }
    }
  }
  return unsortedData.map(x => x.slice(1));
}

function getLastRow() {
  var meta_data_sheet = SpreadsheetApp.getActive().getSheetByName('MetaData');
  var rowCountCell = meta_data_sheet.getRange("B3");
  return rowCountCell.getValue();
}

function updateRowCount() {
  var meta_data_sheet = SpreadsheetApp.getActive().getSheetByName('MetaData');
  var rowCountCell = meta_data_sheet.getRange("B3");
  var newRowCount = rowCountCell.getValue() + 1;
  rowCountCell.setValue(newRowCount);
}