  
$("document").ready(function(){
    var url=window.location.search.substring(1);
    if(url.match(/ *button=Get*/))
    {
        $(".invisible").css("display","block");
        $(".visible").css("display","none");
    }
    else if (url.match(/ *button=Submit*/))
    {
        $(".visible").css("display","block");
        $(".invisible").css("display","none");
    }
    else
    {
        $(".schedule_div").css("display","none");
        $(".visible").css("display","block");
        $(".invisible").css("display","none");
    }


});


function schedule_submit(){
    if(document.getElementById("tr_source_drop_down").selectedIndex==0 || document.getElementById("tr_dest_drop_down").selectedIndex==0)
    {
        alert("Please select both Option.");
        return false;
    }
    else
    {
        if(document.getElementById("tr_source_drop_down").selectedIndex==document.getElementById("tr_dest_drop_down").selectedIndex)
        {
            alert("You have selected same source and destination.");
            return false;
        }
        else{
            if(check_train())
            {
                return true;
            }
            else
            {
                alert("There is no train between this source and destination .");
                return false;
            }
        }
    }
}

function check_train()
{
    var source=document.getElementById("tr_source_drop_down").value;
    var dest=document.getElementById("tr_dest_drop_down").value;
    var bool=false;
    if (window.XMLHttpRequest)
    {// code for IE7+, Firefox, Chrome, Opera, Safari
        xmlhttp=new XMLHttpRequest();
    }
    else
    {// code for IE6, IE5
        xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
    }    
   
    xmlhttp.onreadystatechange=function() 
    {
        if (xmlhttp.readyState==4 && xmlhttp.status==200)
        {
            if(xmlhttp.responseText==true)
            {
                bool= true;
            }
            else
            {
                bool= false;
            }
        }
    }
    
    xmlhttp.open("POST","/cgi-bin/get_train.cgi",false)
    xmlhttp.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xmlhttp.send("source="+source+"&dest="+dest); 
    return bool;
}



function train_no_submit(){
    // alert(document.train_schedule["tr_no"].checked);
    
    var oRadio = document.forms['train_schedule'].elements['tr_no'];
 
   for(var i = 0; i < oRadio.length; i++)
   {
      if(oRadio[i].checked)
      {
        // return oRadio[i].value;
         return true;
      }
   }
  alert("First select option."); 
  return false; 
}
