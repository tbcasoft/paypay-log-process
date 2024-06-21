function getDailyQrAnalysisResult(conn, startDate) {

  var stmt_not_unique = conn.prepareStatement(`
      SELECT mhqr.time as Time, mhqr.SUCCESS as SUCCESS, mhqr.MERCHANT_SUSPENDED as MERCHANT_SUSPENDED,
      mhqr.HIVEX_UNAVAILABLE_MERCHANT as HIVEX_UNAVAILABLE_MERCHANT, mhqr.Dynamic_QR as Dynamic_QR, 
      mhqr.P2P as P2P, mhqr.Others as Others, mhqr.Total as Total 
      FROM hour_qr.mainnet_hour_qr_result mhqr   
      WHERE time >= ? AND time < ?
      ORDER BY time 
    `);

  var stmt = stmt_not_unique;

  var endDate = new Date();
  endDate.setDate(startDate.getDate() + 1);
  var start = formatDbDate(startDate);
  var end = formatDbDate(endDate);

  stmt.setString(1, start);
  stmt.setString(2, end);

  var results = stmt.executeQuery();
  var columnCount = results.getMetaData().getColumnCount();

  var data = getDailyData(results, columnCount);

  results.close();
  return data;
}

function getDailyData(results, columnCount) {
  var seenDate = new Set();
  var data = [];
  var counter = 0;
  results.next();
  var isDbHead = checkDbHead(results);
  results.beforeFirst();
  while (results.next()) {
    if (seenDate.has(results.getString(1))) continue;
    else {
      seenDate.add(results.getString(1));
    }
    if (counter % 24 == 0) {
      var row = [results.getString(1).substring(0, 10)];
      for(var col = 2; col <= columnCount; col ++) {
        var val = parseInt(results.getString(col));
        row.push(val);
      }
      data.push(row);
      if (isDbHead) {
        counter++;
        isDbHead = false;
      }
    } 
    else {
      var row = data[Math.floor(counter/24)];
      for(var col = 2; col <= columnCount; col ++) {
        var val = parseInt(results.getString(col));
        row[col-1] += val;
      }
    }
    counter ++;
  }
  return data[0];
}

function checkDbHead(results) {
  // db miss 1 row for 2024/06/11 00:00
  return results.getString(1).includes('2024-06-11')
}