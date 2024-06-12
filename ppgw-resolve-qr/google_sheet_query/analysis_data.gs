function getQrAnalysisResult() {
  var startTime = new Date();

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

  var stmt_unique = conn.prepareStatement(`
      SELECT mhqr.time as Time, mhqr.SUCCESS_unique as SUCCESS, mhqr.MERCHANT_SUSPENDED_unique as MERCHANT_SUSPENDED,
      mhqr.HIVEX_UNAVAILABLE_MERCHANT_unique as HIVEX_UNAVAILABLE_MERCHANT, mhqr.Dynamic_QR_unique as Dynamic_QR, 
      mhqr.P2P_unique as P2P, mhqr.Others_unique as Others, mhqr.Total_unique as Total  
      FROM hour_qr.mainnet_hour_qr_result mhqr  
      WHERE time >= ? AND time < ?
      ORDER BY time 
    `);

  var stmt_not_unique = conn.prepareStatement(`
      SELECT mhqr.time as Time, mhqr.SUCCESS as SUCCESS, mhqr.MERCHANT_SUSPENDED as MERCHANT_SUSPENDED,
      mhqr.HIVEX_UNAVAILABLE_MERCHANT as HIVEX_UNAVAILABLE_MERCHANT, mhqr.Dynamic_QR as Dynamic_QR, 
      mhqr.P2P as P2P, mhqr.Others as Others, mhqr.Total as Total 
      FROM hour_qr.mainnet_hour_qr_result mhqr   
      WHERE time >= ? AND time < ?
      ORDER BY time 
    `);
  
  var analysis_data_sheet = SpreadsheetApp.getActiveSheet();
  var startDate = analysis_data_sheet.getRange("B2").getValue();
  var endDate = analysis_data_sheet.getRange("C2").getValue();
  var startTime = analysis_data_sheet.getRange("D2").getValue();
  var endTime = analysis_data_sheet.getRange("E2").getValue();
  var isUniqueQr = analysis_data_sheet.getRange("G2").getValue();

  var stmt = isUniqueQr ? stmt_unique : stmt_not_unique

  Logger.log(startDate)
  Logger.log(startTime)
  start = getDateString(startDate, startTime);
  Logger.log(start);

  Logger.log(endDate)
  Logger.log(endTime)
  end = getDateString(endDate, endTime)
  Logger.log(end);
  Logger.log(typeof isUniqueQr)
  Logger.log(isUniqueQr);

  stmt.setString(1, start);
  stmt.setString(2, end);

  var stmt_prep_time = new Date();

  var results = stmt.executeQuery();
  var columnCount = results.getMetaData().getColumnCount();

  var query_db_time = new Date();

  data = [];
  while (results.next()) {
    var row = [];
    for(var col = 1; col <= columnCount; col ++) {
      row.push(results.getString(col));
    }
    data.push(row);
  }
  Logger.log(data.length)
  
  var parse_data_time = new Date();

  if (data.length == 0) return;
  clearRange(analysis_data_sheet);
  var analysis_data_range = analysis_data_sheet.getRange(6, 2, data.length, columnCount);
  analysis_data_range.setValues(data);
  var rowCountCell = analysis_data_sheet.getRange("A7");
  rowCountCell.setValue(data.length);

  results.close();
  stmt.close();

  var total_time = new Date();
}

function clearRange(sheet){
    var rowCount = sheet.getRange("A7").getValue();
    var range = sheet.getRange(6, 2, rowCount, 8);
    range.clear();
}

function getDateString(date, time){
  var tzoffset = (new Date()).getTimezoneOffset() * 60000;
  dateString = new Date(date - tzoffset).toISOString().split('T')[0];
  timeString = new Date(time - tzoffset).toISOString().split(/[T|:]/)[1];
  return dateString.concat(" ", timeString);
}
