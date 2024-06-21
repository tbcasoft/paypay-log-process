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
      SELECT dod.time as Time, dod.issuer as Issuer, 
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
      WHERE time = ?
      ORDER BY time
    `);

  var raw_data_sheet = SpreadsheetApp.getActive().getSheetByName('JKO/ESB/PXP');
  
  var lastSheetRow = raw_data_sheet.getLastRow(); 
  var lastRow = raw_data_sheet.getRange(lastSheetRow, 1).getValue(); 
  
  var lastDateStr = raw_data_sheet.getRange("A" + lastRow.toString()).getValue();
  var lastDate = stringToDate(lastDateStr);

  var curDate = new Date();
  curDate.setDate(lastDate.getDate() + 1);
  var db_format_curDate = formatDbDate(curDate);

  stmt.setString(1, db_format_curDate);

  var results = stmt.executeQuery();
  var rawColumnCount = results.getMetaData().getColumnCount();

  var data = [];
  
  while (results.next()) {
    var row = [];
    for(var col = 3; col <= rawColumnCount; col ++) {
      row.push(results.getString(col));
    }
    data.push(row);
  }
  
  var columnCount = data[0].length;
  // Logger.log(`raw data is: ${data}`);

  var numIssuers = data.length;
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

  var cpmTerminationAnchors = [0, 2, 3].map(x => 16 * (numIssuers + 1) + 14 + x);
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

  var rowCountCell = raw_data_sheet.getRange(lastSheetRow + 1, 1);
  rowCountCell.setValue(curRow);

  results.close();
  stmt.close();
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