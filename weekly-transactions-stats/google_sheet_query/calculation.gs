function calculateAnalysis(numIssuers, qrData, lastRow, raw_data_sheet) {

  var namedRangeAnchors = {
    'totalTransactionAmountJPYMinusRefund': {
      "targets": ['totalCPMTransactionAmountJPY', 'totalMPMTransactionAmountJPY', 'totalRefundAmountJPY'],
      "formula": '=#0 + #1 - #2'
    },
    'totalSuccessfulTransaction': {
      "targets": ['totalMPMPaymentSuccess', 'totalCPMPaymentSuccess', 'totalRefundSuccess'],
      "formula": '=#0 + #1 + #2'
    },
    'totalMPMPaymentSuccessfulAndIncomplete': {
      "targets": ['totalMPMPaymentSuccess', 'totalIncompleteMPMPaymentFailedOnIssuer'],
      "formula": '=#0 + #1'
    },
    'incompleteMPMPaymentRateAsPercentageOfTotalMPMPayment': {
      "targets": ['totalMPMPaymentSuccessfulAndIncomplete', 'totalIncompleteMPMPaymentFailedOnIssuer'],
      "formula": '=#1 / #0'
    },
    'QRUtilizationRate': {
      "targets": ['totalCPMPaymentSuccess', 'totalGenerateQRRequest', 'totalRequestForPaymentRejectionIssuer'],
      "formula": '=(#0 + #2) / #1'
      //  (0 + 2) / 1
    }, 
    'totalRequestForPaymentSuccessRate': {
      "targets": ['totalCPMPaymentSuccess', 'totalRequestForPaymentRejectionIssuer'],
      "formula": '=1 - (#1 / (#0 + #1))'
      // '1' - (1 / (0 + 1))
    }
  };

  for(var anchorKey in namedRangeAnchors) {
    var targets = namedRangeAnchors[anchorKey]["targets"];
    var offsetedRanges = targets.map(x => offsetNamedRange(x, raw_data_sheet, lastRow));
    var formula = namedRangeAnchors[anchorKey]["formula"];

    for (var issuer = 0; issuer <= numIssuers; issuer++) {
      var copyFormula = formula;
      for (var i = 0; i < offsetedRanges.length; i++) {
        var targetRange = offsetedRanges[i].offset(0, issuer);
        var targetRangeName = targetRange.getA1Notation();
        var tempFormula = copyFormula.replace(new RegExp(`#${i}`, 'g'), targetRangeName);
        copyFormula = tempFormula;
      }

      var startAnchor = offsetNamedRange(anchorKey, raw_data_sheet, lastRow);
      var resultRange = startAnchor.offset(0, issuer);
      resultRange.setFormula(copyFormula);
    }
  }
  setQrData(raw_data_sheet, qrData, lastRow);

  setCPMTerminationData(raw_data_sheet, lastRow);
}


function setCPMTerminationData(raw_data_sheet, lastRow) {
  var startCell = offsetNamedRange('_QR_CPMOptOut', raw_data_sheet, lastRow);

  var total = startCell.getValue() + startCell.offset(0,2).getValue() + startCell.offset(0,3).getValue();
  startCell.offset(0,4).setValue(total);

  var totalCPMAmount = offsetNamedRange('totalCPMPaymentSuccess', raw_data_sheet, lastRow).getValue();
  var totalRFP = offsetNamedRange('totalRequestForPaymentRejectionIssuer', raw_data_sheet, lastRow).getValue();
  
  startCell.offset(0,1).setValue(startCell.getValue() / (total + totalCPMAmount + totalRFP));
  startCell.offset(0,5).setValue(total / (total + totalCPMAmount + totalRFP));
}

function normalizeAnchor(anchor, numIssuers) {
  return (anchor - 1) * (numIssuers + 1) + Math.floor(anchor / 10) * 14 + 1;
}

function setQrData(raw_data_sheet, qrData, lastRow) {
    var offsetCell = offsetNamedRange('_QR_QRScanFailure1', raw_data_sheet, lastRow);

    var MERCHANT_SUSPENDED = qrData[2];
    var Dynamic_QR = qrData[4];
    var P2P = qrData[5];
    var Others = qrData[6];
    var HIVEX_UNAVAILABLE_MERCHANT = qrData[3];

    offsetCell.setValue(0);
    offsetCell.offset(0, 1).setValue(0);
    offsetCell.offset(0, 2).setValue(0);

    offsetCell.offset(0, 3).setValue(MERCHANT_SUSPENDED);
    offsetCell.offset(0, 3).setValue(MERCHANT_SUSPENDED);
    offsetCell.offset(0, 4).setValue(Dynamic_QR);
    offsetCell.offset(0, 7).setValue(P2P);
    offsetCell.offset(0, 8).setValue(Others);
    offsetCell.offset(0, 9).setValue(HIVEX_UNAVAILABLE_MERCHANT);

    var qrScanFailure = MERCHANT_SUSPENDED + Dynamic_QR + P2P + Others + HIVEX_UNAVAILABLE_MERCHANT;
    offsetCell.offset(0, 12).setValue(qrScanFailure);
    var sacnFailureRate = qrScanFailure / (qrScanFailure + offsetCell.offset(0, 14).getValue());
    offsetCell.offset(0, 13).setValue(sacnFailureRate);

    offsetCell.offset(0, 5).setValue(Dynamic_QR / qrScanFailure);
    offsetCell.offset(0, 6).setValue(offsetCell.offset(0, 5).getValue() * sacnFailureRate);
    offsetCell.offset(0, 10).setValue(HIVEX_UNAVAILABLE_MERCHANT / qrScanFailure);
    offsetCell.offset(0, 11).setValue(offsetCell.offset(0, 10).getValue() * sacnFailureRate);
}