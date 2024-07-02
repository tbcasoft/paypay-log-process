function updatePPFailureRate(date) {
  var raw_data_sheet = SpreadsheetApp.getActive().getSheetByName('PP Failure Rate Table');
  var lastRow = getLastRow();
  raw_data_sheet.insertRowBefore(lastRow);

  var issuerList = getIssuers();

  var startCell = raw_data_sheet.getRange(lastRow, 2);
  startCell.offset(0,-1).setValue(date);
  startCell.offset(0, 15).setValue(0);

  setRawData(startCell, issuerList);
  calculateData(startCell, lastRow);

}


function setRawData(startCell, issuerList) {
  // console.log(`issuer list is: ${issuerList}`);
  var sourceSheetName = issuerList.join("/");
  var formulaPrefix = `='${sourceSheetName}'!`;
  var offsetsAndFunctions = {
    1: "totalMPMPaymentSuccess", 
    2: "totalCPMPaymentSuccess", 
    3: "_QR_MPMHivexUnavailableMerchants", 
    4: "_QR_MPMDynamicQR", 
    5: "_QR_CPMOptOut", 
    6: "_QR_CPMAcquirerValidation",
    8: "totalRequestForPaymentRejectionIssuer", 
    9: "_QR_CPMExpiredCode", 
    10: "totalIncompleteMPMPaymentFailedOnIssuer",
    12: "_QR_MPMMerchantSuspended", 
    13: "_QR_MPMP2P",
    14: "_QR_othersError"
  }

  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sourceSheet = ss.getSheetByName(sourceSheetName);
  var sourceRow = ss.getRange("MetaData!_META_DATA_numRows").getValue();

  for (var offsetIndex in offsetsAndFunctions) {
    var dataName = offsetsAndFunctions[offsetIndex];
    var dataTitleCell = sourceSheet.getRange(dataName);
    var sourceCol = dataTitleCell.getColumn();

    var dataSourceCell = sourceSheet.getRange(sourceRow, sourceCol).getA1Notation();

    var targetCell = startCell.offset(0, offsetIndex);
    var formula = formulaPrefix + dataSourceCell;
    targetCell.setFormula(formula);
  }
}

function calculateData(startCell, lastRow) {
  var offsetsAndFunctions = {
    0: "=sum(C#row#:D#row#)", 
    7: "=sum(E#row#:H#row#)", 
    11: "=sum(J#row#:L#row#)", 
    16: "=sum(N#row#:Q#row#)", 
    17: "=sum(B#row#,I#row#,M#row#,R#row#)", 
    18: "=(I#row#-E#row#)/S#row#",
    19: "=F#row#/S#row#"
  }

  for (var offsetIndex in offsetsAndFunctions) {
    var targetCell = startCell.offset(0, offsetIndex);
    var formula = offsetsAndFunctions[offsetIndex].replace(new RegExp("#row#", 'g'), lastRow.toString());
    targetCell.setFormula(formula);
  }
}