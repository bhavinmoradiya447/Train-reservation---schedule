  
$("document").ready(function(){
    
    //  $(".first_cancel_div").css("display","block");
    // $(".second_cancel_div").css("display","none");
    
    
    });

var xmlhttp;
var reservation_no=null;
/*var total=null;
var source=null;
var dest=null;
var tr_no=null;
var tr_class=null;
var tr_quota=null;
var date=null;
var concession;
//var day=null;
//var month=null;
//var year=null;
//var source=null;
//var dest=null;
//var tr_no=null;
var no_of_seat=null;
var no_of_seat_cancel=null;
var user_id=null;
var source_code=null;
var dest_code=null;
 */

function reservation_no_validation()
{
    var field=document.getElementById("reservation_no");
    reservation_no=field.value;
    if(field.value.match(/(^\s*)|(\s*$)/gi))
    {
        field.value = field.value.replace(/(^\s*)|(\s*$)/gi,"");
        field.value = field.value.replace(/[ ]{2,}/gi," ");
    }
        
    if(!field.value.match(/^[0-9]+$/gi))
    {
        alert("only Digit allowed.\nenter again");
        field.value="";
        return false;
    }
    else if(!field.value.match(/^[0-9]{16}$/gi))
    {
        alert("reservation number must be 16 digit \n or only Digit allowed.\nenter again");
        field.value="";
        return false;
        
    }
    else
    {
        return true;
    }
}
function popitup() {
    
    reservation_no=document.getElementById("reservation_no").value;
    var user_id=document.getElementById("user_id").value;
    
    if(reservation_no_validation())
    {
    
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
                if(!xmlhttp.responseText.match(/invalid user/gi) && !xmlhttp.responseText.match(/invalid reservation number/gi))
                {
                    var result=xmlhttp.responseText.split(";");
            
                    var newwindow=window.open('','Reservation','height=412,width=572,location=no,menubar=no,scrollbar=no,status=no,titlebar=no,toolbar=no');
	
                    newwindow.document.write('<!DOCTYPE HTML>'+
                        '<html style="width:550px;height: 400px; alignment-adjust: central;">'+
                        '<head><link rel="ICON" href="/image/favicon.ico" />'+
                        '<script type="text/javascript" src="/script/jquery-1.7.2.min.js" ></script>'+
                        '<script type="text/javascript">'+
       
                        'function printpage(){'+
                        '$(".print_div").css("display","none");window.location.reload();'+
                        'window.print();'+
                        '$(".print_div").css("display","block");'+
                        '}'+
                        '</script>'+
                        '</head>'+

                        '<body style="width: 100%;height: 100%;">'+
                        '<div style="width: 100%;height: 100%;" >'+
                        '<table style="width: 100%;height:100% ; color: brown; border-style:solid;" >'+
                        '<tr style="width: 100%;height: 12%; "><td style="width: 100%;height: 12%; " colspan="2"><image src="/image/tickit_header.jpg" /></td></tr> '+

                        '<tr style="width: 100%;height: 12%; "><td style="width:50%;height: 12%; ">Reservation Number : '+result[0]+'</td>'+
                        '<td style="width: 50%;height: 12%;">Date : '+result[1]+'</td></tr>'+

                        '<tr style="width: 100%;height: 12%; "><td style="width: 50%;height: 12%; ">Name : '+result[2]+'</td> '+
                        '<td style="width: 50%;height: 12%;">Train No : '+result[3]+'</td></tr>'+

                        '<tr style="width: 100%;height: 12%; "><td style="width: 100%;height: 12%; " colspan="2">Source : '+result[4]+'</td></tr> '+

                        '<tr style="width: 100%;height: 12%; "><td style="width: 100%;height: 12%; " colspan="2">Destination : '+result[5]+'</td></tr>'+

                        '<tr style="width: 100%;height: 12%; "><td style="width: 50%;height: 12%; ">Class : '+result[6]+'</td> '+
                        '<td style="width: 50%;height: 12%;">Quota : '+result[7]+'</td></tr>'+

                        '<tr style="width: 100%;height: 12%; "><td style="width: 100%;height: 12%; ">Seat Number : '+result[8]+'</td></tr> '+

                        '<tr style="width: 100%;height: 12%; "><td style="width: 50%;height: 12%; ">Distance : '+result[10]+'</td>'+
                        '<td style="width: 50%;height: 12%;">Amount : '+result[9]+'</td></tr> '+

       
                        '<tr style="width: 100%;height: 12%; color: brown; text-align:center;  " class="print_div" >'+
                        '<td onclick="printpage();" style="cursor: pointer;" colspan="2">Print</td></tr>'+
                        '</table>'+
                        '</div>'+

                        '</body>'+
                        '</html>');
        

                }           
            }
            if(xmlhttp.responseText.match(/invalid user/gi))
            {
                alert("you have not canceled seat for this reservation number");
            }
            if(xmlhttp.responseText.match(/invalid reservation number/gi))
            {
                alert(xmlhttp.responseText);
            }
            
        }
    
        xmlhttp.open("POST","/cgi-bin/reservation/status/reserve_status.cgi",false)
        xmlhttp.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
        xmlhttp.send("reservation_no="+reservation_no+"&user_id="+user_id); 
    
        
    }
    return true;
}

function cancel_status()
{
    
    
    reservation_no=document.getElementById("reservation_no").value;
    var user_id=document.getElementById("user_id").value;
    
    if(reservation_no_validation())
    {
    
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
                if(xmlhttp.responseText !="invalid user" && xmlhttp.responseText !="invalid reservation number or you have not canceled any seat")
                {
                    var newwindow=window.open('','_self');
	
                    newwindow.document.write(xmlhttp.responseText);
                }
                else if(xmlhttp.responseText == "invalid user")
                {
                    alert("you have not canceled seat for this reservation number");
                }
                else if(xmlhttp.responseText =="invalid reservation number or you have not canceled any seat")
                {
                    alert(xmlhttp.responseText);
                }
            }           
        }
    
    }
    
    xmlhttp.open("POST","/cgi-bin/reservation/status/cancel_status.cgi",false)
    xmlhttp.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xmlhttp.send("reservation_no="+reservation_no+"&user_id="+user_id); 
    
}