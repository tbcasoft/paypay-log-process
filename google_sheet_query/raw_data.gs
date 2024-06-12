function getRawQrResult() {
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

  var stmt = conn.prepareStatement(`
      SELECT mhqr.time as Time, mhqr.id as Id, mhqr.qr as QR, mhqr.result_code as ResultCode 
      FROM hour_qr.mainnet_hour_qr_raw mhqr  
      WHERE time >= ? AND time < ?
      ORDER BY time 
    `);

  var raw_data_sheet = SpreadsheetApp.getActiveSheet();
  var startDate = raw_data_sheet.getRange("B2").getValue();
  var endDate = raw_data_sheet.getRange("C2").getValue();
  var startTime = raw_data_sheet.getRange("D2").getValue();
  var endTime = raw_data_sheet.getRange("E2").getValue();


  start = getDateString(startDate, startTime);
  Logger.log(start);


  end = getDateString(endDate, endTime)
  Logger.log(end);


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
  // Logger.log(data.length)
  
  var parse_data_time = new Date();

  if (data.length == 0) return;
  clearRange(raw_data_sheet);
  var raw_data_range = raw_data_sheet.getRange(6, 2, data.length, columnCount);
  raw_data_range.setValues(data);
  var rowCountCell = raw_data_sheet.getRange("A7");
  rowCountCell.setValue(data.length);

  // Logger.log(typeof results)
  // Logger.log(results)

  results.close();
  stmt.close();

  var total_time = new Date();
}

function clearRange(sheet){
    var rowCount = sheet.getRange("A7").getValue();
    var range = sheet.getRange(6, 2, rowCount, 4);
    range.clear();
}

function getDateString(date, time){
  var tzoffset = (new Date()).getTimezoneOffset() * 60000;
  dateString = new Date(date - tzoffset).toISOString().split('T')[0];
  timeString = new Date(time - tzoffset).toISOString().split(/[T|:]/)[1];
  return dateString.concat(" ", timeString);
}