chrome.runtime.onInstalled.addListener(() => {
  console.log("Extension Installed");
});

chrome.action.onClicked.addListener((tab) => {
  chrome.scripting.executeScript({
      target: { tabId: tab.id },
      function: () => window.location.href,
  }, (results) => {
      chrome.runtime.sendMessage({ url: results[0].result });
  });
});

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.url) {
      console.log('Processing URL:', message.url);
  }
});
