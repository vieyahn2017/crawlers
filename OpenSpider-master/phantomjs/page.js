var page = require('webpage').create()
page.open('http://www.lagou.com/',function(status){
    console.log("Status: " + status);
    if(status == "success"){
        page.render('./lagou.png');
    }
    phantom.exit();
});