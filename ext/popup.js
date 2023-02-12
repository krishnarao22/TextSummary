
$(function(){

    
    $('#submitbtn').click(function(){
		
        var doc_text = document.body.innerText;
		
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
		
    });
});