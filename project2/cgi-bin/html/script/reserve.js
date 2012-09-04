  
$("document").ready(function(){

    window.onbeforeunload=function(){
        //do some clean up
        return "refress not allowed"
    }
    $(".first_reserve_div").css("display","block");
    $(".second_reserve_div").css("display","none");
    $(".third_reserve_div").css("display","none");
    $(".forth_reserve_div").css("display","none");
    
    
});

var xmlhttp;
var total=null;
var source=null;
var dest=null;
var tr_no=null;
var tr_class=null;
var tr_quota=null;
var day=null;
var month=null;
var year=null;
var no_of_seat=null;
var user_id=null;

function seat_no_validation()
{
    var field=document.getElementById("no_of_seat");
    if(field.value.match(/(^\s*)|(\s*$)/gi))
    {
        field.value = field.value.replace(/(^\s*)|(\s*$)/gi,"");
        field.value = field.value.replace(/[ ]{2,}/gi," ");
    }
        
    if(!field.value.match(/^[0-9]+$/gi))
    {
        alert("only Digit allowed.\nenter again");
        field.value="";
    }
    else
    {
        if(field.value>10)
        {
                    
            alert("You can reserve maximum 10 seat at a time.");
            field.value="";
        }
    }
}
    
    
function check_train_root()
{
    source=document.getElementById("tr_source_drop_down").value;
    dest=document.getElementById("tr_dest_drop_down").value;
    tr_no=document.getElementById("tr_no_drop_down").value;
    user_id=document.getElementById("user_id").value;
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

function reservation()
{
    
    user_id=document.getElementById("user_id").value;
    source=document.getElementById("tr_source_drop_down").value;
    dest=document.getElementById("tr_dest_drop_down").value;
    tr_no=document.getElementById("tr_no_drop_down").value;
    tr_class=document.getElementById("tr_class_drop_down").value;
    tr_quota=document.getElementById("tr_quota_drop_down").value;
    day=document.getElementById("lccp_day").value;
    month=document.getElementById("lccp_month").value;
    year=document.getElementById("lccp_year").value;
    no_of_seat=document.getElementById("no_of_seat").value;
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
            if(xmlhttp.responseText.match(/time over/))
            {
                $("#progress").css("display","none");
                alert("You can not reserve seat after train Departed.");
                bool=false;
            }
            else{
                var result=xmlhttp.responseText.split(";");

                var temp=result[0].split("=");
                document.getElementById("TR_NO").innerHTML=temp[1];
                temp=result[1].split("=");
                document.getElementById("TR_NAME").innerHTML=temp[1];
                temp=result[2].split("=");
                document.getElementById("DATE").innerHTML=temp[1];
                temp=result[3].split("=");
                document.getElementById("TR_SOURCE").innerHTML=temp[1];
                temp=result[4].split("=");
                document.getElementById("TR_DEST").innerHTML=temp[1];
                temp=result[5].split("=");
                document.getElementById("TR_TYPE").innerHTML=temp[1];
                temp=result[6].split("=");
                document.getElementById("DIST").innerHTML=temp[1];
                temp=result[7].split("=");
                document.getElementById("CLASS").innerHTML=temp[1];
                temp=result[8].split("=");
                var fare=temp[1]*no_of_seat;
                total=fare;
                document.getElementById("FARE").innerHTML=fare;
                total+=20;
                temp=result[9].split("=");
                var super_charge=temp[1]*no_of_seat;
                total+=temp[1]*no_of_seat;
                document.getElementById("SUPER_CHARGE").innerHTML=super_charge;
                var cons=(fare*document.getElementById("tr_cons_drop_down").value)/100;
                total-=cons;
                document.getElementById("CONC").innerHTML=cons;
                document.getElementById("TOTAL").innerHTML=total;
                temp=result[10].split("=");
                document.getElementById("wait").innerHTML=temp[0];
                document.getElementById("seat_available").innerHTML=temp[1];
                bool=true;    
            }                   
        }
    }
    
    xmlhttp.open("POST","/cgi-bin/reservation/reserve/reserve_2.cgi",false)
    xmlhttp.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xmlhttp.send("tr_source="+source+"&tr_dest="+dest+"&tr_no="+tr_no+"&tr_class="+tr_class+"&tr_quota="+tr_quota+"&lccp_day="+day+"&lccp_month="+month+"&lccp_year="+year); 
    return bool;
}


function reserve_submit(){
    //   document.getElementById("TR_NO").innerHTML="bhavin";
    user_id=document.getElementById("user_id").value;
    
    if(document.getElementById("tr_no_drop_down").selectedIndex==0 || document.getElementById("tr_source_drop_down").selectedIndex==0 || document.getElementById("tr_class_drop_down").selectedIndex==0 || document.getElementById("tr_dest_drop_down").selectedIndex==0)
    {
        alert("select all Option.");
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
                    if(reservation())
                    {
                        $(".first_reserve_div").css("display","none");
                        $(".second_reserve_div").css("display","block");
                        $(".third_reserve_div").css("display","none");
                        $(".forth_reserve_div").css("display","none");
                    }
                }
                else
                {
                    
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

function confirm_submit(){
    document.getElementById("total_amount").value=total;
    $(".first_reserve_div").css("display","none");
    $(".second_reserve_div").css("display","none");
    $(".third_reserve_div").css("display","block");
    $(".forth_reserve_div").css("display","none");
}

function pay_now_submit(){
    
   
    source=document.getElementById("tr_source_drop_down").value;
    dest=document.getElementById("tr_dest_drop_down").value;
    tr_no=document.getElementById("tr_no_drop_down").value;
    tr_class=document.getElementById("tr_class_drop_down").value;
    tr_quota=document.getElementById("tr_quota_drop_down").value;
    day=document.getElementById("lccp_day").value;
    month=document.getElementById("lccp_month").value;
    year=document.getElementById("lccp_year").value;
    no_of_seat=document.getElementById("no_of_seat").value; 
    user_id=document.getElementById("user_id").value;

    $("#progress").css("display","block");

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
             
            $(".first_reserve_div").css("display","none");
            $(".second_reserve_div").css("display","none");
            $(".third_reserve_div").css("display","none");
            $(".forth_reserve_div").css("display","block");
            
            document.getElementById("reservation_no").innerHTML=result[0];
            document.getElementById("seat_assign").innerHTML=result[1];
            document.getElementById("seat_remain").innerHTML=result[2];
            
        }
    }
    
    xmlhttp.open("POST","/cgi-bin/reservation/reserve/reserve_3.cgi",false)
    xmlhttp.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xmlhttp.send("tr_source="+source+"&tr_dest="+dest+"&tr_no="+tr_no+"&tr_class="+tr_class+"&tr_quota="+tr_quota+"&lccp_day="+day+"&lccp_month="+month+"&lccp_year="+year+"&no_of_seat="+no_of_seat+"&concession="+document.getElementById("tr_cons_drop_down").value+"&total="+total+"&user_id="+user_id); 

    $("#progress").css("display","none");
    
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
    var day;
   
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
            day=xmlhttp.responseText.replace(";",",");
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