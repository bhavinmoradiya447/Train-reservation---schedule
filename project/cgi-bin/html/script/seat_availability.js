  
$("document").ready(function(){
 
    });



 
function train_class_validation()
{
    if(document.getElementById("tr_class_drop_down").selectedIndex!=0&&document.getElementById("tr_no_drop_down").selectedIndex==0&&document.getElementById("tr_no_drop_down").selectedIndex==0)
    {
        alert("First select Train number.");
        document.getElementById("tr_class_drop_down").selectedIndex=0;
    }
}

function train_quota_validation()
{
    if(document.getElementById("tr_quota_drop_down").selectedIndex!=0&&document.getElementById("tr_no_drop_down").selectedIndex==0&&document.getElementById("tr_no_drop_down").selectedIndex==0)
    {
        alert("First select Train number.");
        document.getElementById("tr_quota_drop_down").selectedIndex=0;
    }
}




function check_train_root()
{
    var source=document.getElementById("tr_source_drop_down").value;
    var dest=document.getElementById("tr_dest_drop_down").value;
    var tr_no=document.getElementById("tr_no_drop_down").value;
    var xmlhttp;
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
    
    xmlhttp.open("POST","/cgi-bin/get_distance.cgi",false)
    xmlhttp.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xmlhttp.send("source="+source+"&dest="+dest+"&tr_no="+tr_no); 
    return bool;
}

function waiting_submit(){
    if(document.getElementById("tr_no_drop_down").selectedIndex==0 || document.getElementById("tr_source_drop_down").selectedIndex==0 || document.getElementById("tr_dest_drop_down").selectedIndex==0)
    {
        alert("you must have to select train number,source,destination and date Option.");
        return false;
    }
    else
    {   
        if(document.getElementById("lccp_day").value=="" || document.getElementById("lccp_month").value=="" || document.getElementById("lccp_year").value=="")
        {
            alert("Date not selected.");
            return false;
        }
        else if(document.getElementById("tr_source_drop_down").selectedIndex==document.getElementById("tr_dest_drop_down").selectedIndex)
        {
            alert("You have selected same source and destination.");
            return false;
        }
        else
        {   
            if(check_train_root())
            {
                if(get_day())
                {
                    return true;
                }
                else
                {
                    alert("This train is not arrive on selected date.");
                    return false;
                }
            }
            else
            {
                alert("Invalid Source and destination");
                return false;
            }
        }
    }
}

function get_day(){

    var d = new Date(document.getElementById("lccp_month").value+" "+document.getElementById("lccp_day").value+","+document.getElementById("lccp_year").value);
    var weekday=new Array(7);
    weekday[0]="Sun";
    weekday[1]="Mon";
    weekday[2]="Tue";
    weekday[3]="Wed";
    weekday[4]="Thu";
    weekday[5]="Fri";
    weekday[6]="Sat";

    var x = weekday[d.getDay()];
    
   
    var tr_no=document.getElementById("tr_no_drop_down").value;
    var source=document.getElementById("tr_source_drop_down").value;
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
            var result=xmlhttp.responseText.split(";");
            if(result[0].match(/Daily/))
            {
              
                bool=true;
            }
            else
            {
                for(i=0;i<result.length;i++)
                {
                    if(result[i].match(x))
                    {
                               
                        bool=true;
                    }
                }
                   
            }
        }
    }
    
    xmlhttp.open("POST","/cgi-bin/get_day.cgi",false)
    xmlhttp.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xmlhttp.send("tr_source="+source+"&tr_no="+tr_no); 
     if(bool==false)
    {
        alert("This train departed only on \""+day+"\"");
        return bool;
    }
      return bool;
    
}