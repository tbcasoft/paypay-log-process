function checkMonthlyUpdate() {
  var isNewMonth = checkIsNewMonth();
  if (isNewMonth) {
    createNewMonthSpreadSheet();
    deactivateTriggers();
  }
}

function checkIsNewMonth() {
  var today = new Date();
  today.setHours(0);
  today.setMinutes(0);
  today.setSeconds(0);
  today.setMilliseconds(0);
  // console.log(`today is ${today}`);

  var monday = new Date(today);
  monday.setDate(today.getDate() - 7);
  // console.log(`monday is ${monday}`);
  
  
  var sunday = new Date(monday);
  sunday.setDate(monday.getDate() + 6);
  // console.log(`sunday is ${sunday}`);

  return (monday.getMonth() != sunday.getMonth()) || monday.getDate() == 1;
}

function createNewMonthSpreadSheet() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var oldSheetName = ss.getName();
  var oldSheetDateStr = oldSheetName.split(" - ")[1];
  console.log(oldSheetDateStr);

  var oldSheetDate = new Date(oldSheetDateStr.substring(0, 4), oldSheetDateStr.substring(4));
  var newSheetDate = new Date();
  newSheetDate.setMonth(oldSheetDate.getMonth() + 1);

  var newYear = String(newSheetDate.getFullYear());
  var newMonth = String(newSheetDate.getMonth()).padStart(2, "0");

  var ssID = ss.getId();
  var ssFile = DriveApp.getFileById(ssID);
  var systemFolder = ssFile.getParents().next();

  ssFile.makeCopy(`${oldSheetName.split(" - ")[0]} - ${newYear}${newMonth}`, systemFolder);

  ss.getSheetByName("SetUp").hideSheet();
  ss.getSheetByName("reportTemplate").hideSheet();
}

function deactivateTriggers() {
  var triggers = ScriptApp.getProjectTriggers();
  for (var i = 0; i < triggers.length; i++) {
    ScriptApp.deleteTrigger(triggers[i]);
  }
}


function initializeSheetDateTitle(lastWeekNumMerchant) {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var ssName = ss.getName();
  var spreadsheetDate = ssName.split("- ")[1];
  var spreadsheetYear = spreadsheetDate.substring(0, 4);
  var spreadsheetMonth = spreadsheetDate.substring(4);

  var monthNum = parseInt(spreadsheetMonth) - 1;

  var templateDate = new Date(2000, monthNum);

  var monthName = templateDate.toLocaleString("default", {month: "short"});

  var dateCell = ss.getRange("reportTemplate!date");
  dateCell.setValue(dateCell.getValue().split("-")[0] + "- " + spreadsheetYear + " " + monthName + " WK0");

  var numMerchantServiceCell = ss.getRange("reportTemplate!numOnboardedMerchantServices");
  numMerchantServiceCell.setValue(lastWeekNumMerchant);
}

function setupSheet() {
  setUpTriggers();
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var setUpSheet = ss.getSheetByName("SetUp");
  setUpSheet.hideSheet();
  
  var template = ss.getSheetByName("reportTemplate");
  template.showSheet();

  var numSheets = getNumSheets() - 2;

  for(var sheet = 1; sheet <= numSheets; sheet++) {
    var oldSheetName = "WK" + sheet.toString();
    var oldeSheet = ss.getSheetByName(oldSheetName);
    if (sheet == numSheets) {
      var lastWeekNumMerchant = ss.getRange(oldSheetName + "!numOnboardedMerchantServices").getValue();
    }
    ss.deleteSheet(oldeSheet);
  }

  initializeSheetDateTitle(lastWeekNumMerchant);

  updateHIVEXSystemReport();
  template.hideSheet();
}

function setUpTriggers() {
  ScriptApp.newTrigger("updateHIVEXSystemReport")
      .timeBased()
      .everyWeeks(1)
      .onWeekDay(ScriptApp.WeekDay.MONDAY)
      .atHour(11)
      .create();
  ScriptApp.newTrigger("checkMonthlyUpdate")
    .timeBased()
    .everyWeeks(1)
    .onWeekDay(ScriptApp.WeekDay.MONDAY)
    .atHour(9)
    .create();
}