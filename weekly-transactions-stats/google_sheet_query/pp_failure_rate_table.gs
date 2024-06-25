function updatePPFailureRate(date) {

  var raw_data_sheet = SpreadsheetApp.getActive().getSheetByName('PP Failure Rate Table');
  var lastRow = getLastRow();
  raw_data_sheet.insertRowBefore(lastRow);

  var issuerList = getIssuers();

  var startCell = raw_data_sheet.getRange(lastRow, 2);
  startCell.offset(0,-1).setValue(date);
  startCell.offset(0, 15).setValue(0);

  setRawData(startCell, lastRow, issuerList);
  calculateData(startCell, lastRow);

}


function setRawData(startCell, lastRow, issuerList) {
  var sourceSheetName = issuerList.join("/");
  var formulaPrefix = `='${sourceSheetName}'!`;
  var offsetsAndFunctions = {
    1: "V", 2: "Z", 3: "AU", 4: "AP", 5: "CB", 6: "CD",
    8: "BT", 9: "CE", 10: "BD",
    12: "AO", 13: "AS", 14: "AT"
  }

  for (var offsetIndex in offsetsAndFunctions) {
    var targetCell = startCell.offset(0, offsetIndex);
    var formula = formulaPrefix + offsetsAndFunctions[offsetIndex] + lastRow.toString();
    Logger.log(formula);
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
