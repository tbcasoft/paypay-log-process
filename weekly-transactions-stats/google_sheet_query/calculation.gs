function calculateAnalysis(dataArray, numIssuers, qrData) {

  var groupAnchors = {
    1: {
      "targets": [2, 3, 4],
      "function": vals => vals[0] + vals[1] - vals[2]
    },
    5: {
      "targets": [6, 7, 8],
      "function": vals => vals[0] + vals[1] + vals[2]
    },
    10: {
      "targets": [6, 11],
      "function": vals => vals[0] + vals[1]
    },
    12: {
      "targets": [10, 11],
      "function": vals => vals[1]/vals[0]
    },
    14: {
      "targets": [7, 13, 15],
      "function": vals => (vals[0] + vals[2]) / vals[1]
      //  (0 + 2) / 1
    }, 
    16: {
      "targets": [7, 15],
      "function": vals => 1 - (vals[1] / (vals[0] + vals[1]))
      // 1 - (1 / (0 + 1))
    }
  };

  for(var anchorKey in groupAnchors) {
    var targets = groupAnchors[anchorKey]["targets"];
    var normalizedTargets = targets.map(x => normalizeAnchor(x, numIssuers) - 1);
    var func = groupAnchors[anchorKey]["function"];

    startAnchor = normalizeAnchor(anchorKey, numIssuers) - 1;
    applyFuntion(dataArray, startAnchor, normalizedTargets, func, numIssuers + 1);

  }
  setQrData(dataArray, numIssuers, qrData);

  setCPMTerminationData(dataArray, numIssuers);
}


function setCPMTerminationData(outputData, numIssuers) {
  var offset = outputData.length - 6;

  var total = outputData[offset] + outputData[offset + 2] + outputData[offset + 3];
  outputData[offset + 4] = total;

  var totalCPMAmount = outputData[normalizeAnchor(7, numIssuers) - 1];
  var totalRFP = outputData[normalizeAnchor(15, numIssuers) - 1];
  
  outputData[offset + 1] = outputData[offset + 0] / (total + totalCPMAmount + totalRFP);
  outputData[offset + 5] = total / (total + totalCPMAmount + totalRFP);
}


function setDefaultTotal(data, startAnchor, numIssuers) {
  var targetAnchors = [4, 8, 12].map(x => startAnchor + x);
  var largeTotal = setTargetTotal(data, startAnchor, targetAnchors, numIssuers);
  return largeTotal;
}

function setTargetTotal(data, outputAnchor, targetAnchors, numIssuers) {
  var largeTotal = 0
  for(var issuer = 0; issuer < numIssuers; issuer ++) { 
    var subTotal = 0;
    for(var numTarget = 0; numTarget < targetAnchors.length; numTarget++) {
      var targetIndex = targetAnchors[numTarget] + issuer;
      subTotal += data[targetIndex];
    }
    data[outputAnchor + issuer] = subTotal;
    largeTotal += subTotal;
  }
  return largeTotal;
}

function applyFuntion(data, startAnchor, targetAnchors, func, numIssuers) {
  for(var issuer = 0; issuer < numIssuers; issuer++) {
    var offsetTargetAnchors = targetAnchors.map(x => x + issuer);
    var targetValues = retrieveTargetValues(data, offsetTargetAnchors);
    
    var result = func(targetValues);
    data[startAnchor + issuer] = result;
  }
}

function retrieveTargetValues(data, targetAnchors) {
  var targetValues = []
  for(var target = 0; target < targetAnchors.length; target++) {
    var targetIndex = targetAnchors[target]
    targetValues.push(data[targetIndex]);
  }
  return targetValues;
}

function normalizeAnchor(anchor, numIssuers) {
  return (anchor - 1) * (numIssuers + 1) + Math.floor(anchor / 10) * 14 + 1;
}

function setQrData(outputData, numIssuers, qrData) {
    var offset = 9 * (numIssuers + 1);

    var MERCHANT_SUSPENDED = qrData[2];
    var Dynamic_QR = qrData[4];
    var P2P = qrData[5];
    var Others = qrData[6];
    var HIVEX_UNAVAILABLE_MERCHANT = qrData[3];

    outputData[offset + 3] = MERCHANT_SUSPENDED;
    outputData[offset + 4] = Dynamic_QR;
    outputData[offset + 7] = P2P;
    outputData[offset + 8] = Others;
    outputData[offset + 9] = HIVEX_UNAVAILABLE_MERCHANT;

    var qrScanFailure = MERCHANT_SUSPENDED + Dynamic_QR + P2P + Others + HIVEX_UNAVAILABLE_MERCHANT;
    outputData[offset + 12] = qrScanFailure;
    var sacnFailureRate = qrScanFailure / (qrScanFailure + outputData[offset + 14]);
    outputData[offset + 13] = sacnFailureRate;

    outputData[offset + 5] = Dynamic_QR / qrScanFailure;
    outputData[offset + 6] = outputData[offset + 5] * sacnFailureRate;
    outputData[offset + 10] = HIVEX_UNAVAILABLE_MERCHANT / qrScanFailure;
    outputData[offset + 11] = outputData[offset + 10] * sacnFailureRate;
}