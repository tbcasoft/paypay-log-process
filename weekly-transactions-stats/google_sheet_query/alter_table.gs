function addIssuer() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();

  var newIssuerCell = ss.getRange("MetaData!_META_DATA_newIssuer");
  var newIssuerName = newIssuerCell.getValue();

  var newIssuerColor = ss.getRange("MetaData!_META_DATA_newIssuerColor").getBackgrounds();

  var numIssuerCell = ss.getRange("MetaData!_META_DATA_numIssuers");
  var numIssuers = numIssuerCell.getValue();

  alterTable(numIssuers, newIssuerName, newIssuerColor);

  numIssuerCell.setValue(numIssuers + 1);
  
  var issuerTitleCell = ss.getRange("MetaData!_META_DATA_issuerTitle");
  var targetUpdateCell = issuerTitleCell.offset(0, numIssuers + 1);
  targetUpdateCell.setValue(newIssuerName);
  targetUpdateCell.setHorizontalAlignment('center');

}

function alterTable(numIssuers, newIssuerName, newIssuerColor) {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var namedRanges = ss.getNamedRanges()
  .map(namedRange => namedRange.getName())
  .filter(name => !name.startsWith("_META_DATA_") && !name.startsWith("_QR_"));
  var issuerList = getIssuers();
  
  var oldSheetName = issuerList.join("/");
  var raw_data_sheet = SpreadsheetApp.getActive().getSheetByName(oldSheetName);
  
  var sumRow = getSumRow(ss, raw_data_sheet);
  var lastIssuerName = getLastIssuerName(raw_data_sheet, numIssuers);

  for(var i = 0; i < namedRanges.length; i++) {
    var dataTotalCell = raw_data_sheet.getRange(`${namedRanges[i]}`);
    var lastIssuerCell = dataTotalCell.offset(0, numIssuers);
    var lastTitle = "~" + lastIssuerCell.getValue();

    var dataName = lastTitle.split(lastIssuerName)[1];
    var lastIssuerCol = lastIssuerCell.getColumn();
    
    raw_data_sheet.insertColumnAfter(lastIssuerCol);

    var newIssuerCol = lastIssuerCol + 1;
    var titleRange = raw_data_sheet.getRange(1, newIssuerCol, 3, 1);
    titleRange.merge();

    var titleName = `${newIssuerName} ${dataName}`;

    titleRange.setValue(titleName);
    titleRange.setBackground(newIssuerColor);

    var totalCell = raw_data_sheet.getRange(titleRange.getRow(), newIssuerCol).offset(sumRow - 1, 0);
    // var row4Cell = raw_data_sheet.getRange(4, newIssuerCol).getA1Notation();
    // var beforeTotalCell = raw_data_sheet.getRange(sumRow - 1, newIssuerCol).getA1Notation();
    // totalCell.setFormula(`=SUM(${row4Cell}:${beforeTotalCell})`);
    var lastIssuerTotalCell = totalCell.offset(0, -1);
    lastIssuerTotalCell.copyTo(totalCell);
  }

  var newSheetName = `${oldSheetName}/${newIssuerName}`;
  raw_data_sheet.setName(newSheetName);
}


function getLastIssuerName(raw_data_sheet, numIssuers) {
  var lastIssuerTitleCell = raw_data_sheet.getRange("totalTransactionAmountJPYMinusRefund").offset(0, numIssuers);
  var lastIssuerName = lastIssuerTitleCell.getValue().split("Total")[0];
  return lastIssuerName.trim();
}

function getSumRow(ss, raw_data_sheet) {
  var rowNumber = ss.getRange("MetaData!_META_DATA_numRows").getValue();

  for (var row = rowNumber; row <= rowNumber + 30; row++) {
    var candidateCell = raw_data_sheet.getRange(row, 1).getValue();
    if (String(candidateCell).includes("Total")) {
      return row;
    }
  }
}