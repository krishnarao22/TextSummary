
$(function(){

    $('#submitbtn').on("click", function(){

        console.log("submit button clicked");

        var tab_id;
        
        chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
            var currTab = tabs[0];
            if (currTab) { // Sanity check
              /* do stuff */
              console.log("we on the curr tab");
              tab_id = currTab.id;
            }
          });

        

        var doc_text;

        var getText = function() {
            return document.body.innerText;
        }
        
        setTimeout(() => {
            console.log("tab_id: " + tab_id);
            chrome.scripting.executeScript(
                {
                    target: {tabId: tab_id},
                    func: getText
                }).then((result) => {
                    console.log(result[0].result);
                    doc_text = result[0].result;
                });
            
            setTimeout(() => {
                console.log("doc_text: " + doc_text)
                
                chrome.runtime.sendMessage(
                    {text: doc_text},
                    function(response) {
                        result = response.farewell;
                        alert(result.summary);
                        
                        var notifOptions = {
                            type: "basic",
                            iconUrl: "icon48.png",
                            title: "Summary For Your Result",
                            message: result.summary
                        };
                        
                        chrome.notifications.create('WikiNotif', notifOptions);
                        
                    });
            }, 1000);
        }, 1000);

    });

 })   

