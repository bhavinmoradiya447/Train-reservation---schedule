  
$("document").ready(function(){
    $(".setting_hide_div").hide();
    $("#setting").click(function(){
        get_user_details('','','','','');
        $('input[name=checkbox]').attr('checked', false);
        $(".setting_hide_div").toggle(1000);
    })
});

var userid;
var name;
var phone_no;
var email;
var paswod;

function get_user_details(na,ph,em,pa,oldpa){
    userid=document.getElementById("user_id").value;
    var xmlhttp;
    //var bool=false;
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
            name=result[0];
            phone_no=result[1];
            email=result[2];
            paswod=result[3];
            document.getElementById("change_user_name").value=name;
            document.getElementById("change_phone_number").value=phone_no;
            document.getElementById("change_email").value=email;
        }
    }
    
    xmlhttp.open("POST","/cgi-bin/get_user_details.cgi",false)
    xmlhttp.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xmlhttp.send("userid="+userid+"&name="+na+"&ph_no="+ph+"&email="+em+"&password="+pa+"&oldpassword="+oldpa); 
}

function change_name(){
    var old_name=document.getElementById("change_user_name").value;
    if(old_name !=null && old_name!="")
    {
        var old_paswod=document.getElementById("change_old_password").value;
        if(old_paswod==null || old_paswod=="")
        {
            alert("First enter Old password.");
        }
        else
        {
            get_user_details(old_name,"","","",old_paswod);
              
            if(!paswod.match("true"))
            {
                alert("wrong password.");
            }
        }
    }
    else{
        alert("Enter name.");
    }  
}

function change_phone_no(){
    var old_phone=document.getElementById("change_phone_number").value;
    if(old_phone !=null && old_phone!="")
    {
        var old_paswod=document.getElementById("change_old_password").value;
        if(old_paswod==null || old_paswod=="")
        {
            alert("First enter Old password.");
        }
        else
        {
          
            get_user_details("",old_phone,"","",old_paswod);
           
            if(!paswod.match("true"))
            {
                alert("wrong password.");
            }
        }
    }
    else{
        alert("Enter phone number.");
    }   
}

function change_email(){
    var old_email=document.getElementById("change_email").value;
    if(old_email !=null && old_email!="")
    {
        var old_paswod=document.getElementById("change_old_password").value;
        if(old_paswod==null || old_paswod=="")
        {
            alert("First enter Old password.");
        }
        else
        {
            
            get_user_details("","",old_email,"",old_paswod);
           
            if(!paswod.match("true"))
            {
                alert("wrong password.");
            }
        }
    }
    else{
        alert("Enter email address.");
    }
}

function change_password(){
    var new_password=document.getElementById("change_new_passowrd").value;
    var confirm_password=document.getElementById("change_confirm_password").value;
    if(new_password !=null && new_password!="" && confirm_password!=null && confirm_password!="")
    {
        var old_paswod=document.getElementById("change_old_password").value;
        if(old_paswod==null || old_paswod=="")
        {
            alert("First enter Old password.");
        }
        else
        {  
            get_user_details("","","",new_password,old_paswod);
           
            if(!paswod.match("true"))
            {
                alert("wrong password.");
            }
        }
    }
    else{
        alert("Enter Password.");
    }
}

function enable_change(id1,id2)
{
    
    if(document.getElementById(id1).checked)
    {
        document.getElementById(id2).removeAttribute("readonly",0);
    }    
    else
    {
        document.getElementById(id2).setAttribute("readonly","");
    }
}

function name_validation(field)
{
    // var value=field.value;
    if(field.value.match(/(^\s*)|(\s*$)/gi))
    {
        field.value = field.value.replace(/(^\s*)|(\s*$)/gi,"");
        field.value = field.value.replace(/[ ]{2,}/gi," ");
    }
        
    if(!field.value.match(/^[A-Z\. ]+$/gi))
    {
        alert("Only alphabetic character allowed.\nenter again");
        field.value="";
    }
}

function  number_validation(field)
{
    if(field.value.match(/(^\s*)|(\s*$)/gi))
    {
        field.value = field.value.replace(/(^\s*)|(\s*$)/gi,"");
        field.value = field.value.replace(/[ ]{2,}/gi," ");
    }
        
    if(!field.value.match(/^[A-Z0-9\.\-\/\\, ]*$/gi))
    {
        alert("invalid entry.\nenter again");
        field.value="";
    }
}

function  address_validation(field)
{
    if(field.value.match(/(^\s*)|(\s*$)/gi))
    {
        field.value = field.value.replace(/(^\s*)|(\s*$)/gi,"");
        field.value = field.value.replace(/[ ]{2,}/gi," ");
    }
        
    if(!field.value.match(/^[A-Z\.\-\/\\,_\"\' ]*$/gi))
    {
        alert("invalid entry.\nenter again");
        field.value="";
    }
}

function  pin_code_validation(field)
{
    if(field.value.match(/(^\s*)|(\s*$)/gi))
    {
        field.value = field.value.replace(/(^\s*)|(\s*$)/gi,"");
        field.value = field.value.replace(/[ ]{2,}/gi," ");
    }
        
    if(!field.value.match(/^[0-9]{6}$/gi))
    {
        alert("Pin must be Six digit \n or only Digit allowed .\nenter again");
        field.value="";
    }
}

function  phone_no_validation(field)
{
    if(field.value.match(/(^\s*)|(\s*$)/gi))
    {
        field.value = field.value.replace(/(^\s*)|(\s*$)/gi,"");
        field.value = field.value.replace(/[ ]{2,}/gi," ");
    }
        
    if(!field.value.match(/^[0-9]{10}$/gi))
    {
        alert("Phone number must be 10 digit \n or only Digit allowed.\nenter again");
        field.value="";
    }
}
function  no_validation(field)
{
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
}

/*function  reservation_no_validation(field)
{
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
}*/

function  email_validation(field)
{
    if(field.value.match(/(^\s*)|(\s*$)/gi))
    {
        field.value = field.value.replace(/(^\s*)|(\s*$)/gi,"");
        field.value = field.value.replace(/[ ]{2,}/gi," ");
    }
        
    if(!field.value.match(/^([a-z0-9])(([-.]|[_]+)?([a-z0-9]+))*(@)([a-z0-9])((([-]+)?([a-z0-9]+))?)*(\.)(([a-z]{2,3})?((\.)?[a-z]{2,6}))$/i))
    {
        alert("invalid Email address.\nenter again");
        field.value="";
    }
}


function  username_validation(field)
{    
    if(field.value.match(/(^\s*)|(\s*$)/gi))
    {
        field.value = field.value.replace(/(^\s*)|(\s*$)/gi,"");
        field.value = field.value.replace(/[ ]{2,}/gi," ");
    }
        
    if(!field.value.match(/^[A-Z0-9\.\-_@#$]*$/gi))
    {
        alert("bad username.\nenter again");
        field.value="";
    }
}

function password_confirmation(field1,field2){
    if(field1.value!=field2.value)
    {  
        var span = document.getElementById("confirm_password");
        span.innerHTML="Password not match";
        field2.value="";
    }   
}

function password_validation(field){
    var span = document.getElementById("password_strength");
    span.innerHTML=CheckPassword(field.value);

}

function CheckPassword(password)
{
    var strength = new Array();
    strength[0] = "Blank";
    strength[1] = "Very Weak";
    strength[2] = "Weak";
    strength[3] = "Medium";
    strength[4] = "Strong";
    strength[5] = "Very Strong";
	 
    var score = 1;
	 
    if (password.length < 1)
        return strength[0];
	 
    if (password.length < 4)
        return strength[1];
	 
    if (password.length >= 8)
        score++;
    if (password.length >= 10)
        score++;
    if (password.match(/\d+/))
        score++;
    if (password.match(/[a-z]/) &&
        password.match(/[A-Z]/))
        score++;
    if (password.match(/.[!,@,#,$,%,^,&,*,?,_,~,-,£,(,)]/))
        score++;	 
    return strength[score];
}
        
function train_no_name_validation()
{
    if(document.getElementById("tr_no_drop_down").selectedIndex!=0 && document.getElementById("tr_name_drop_down").selectedIndex!=0 && (document.getElementById("tr_no_drop_down").selectedIndex!=document.getElementById("tr_name_drop_down").selectedIndex))
    {
        document.getElementById("tr_no_drop_down").selectedIndex=0;
        document.getElementById("tr_name_drop_down").selectedIndex=0;
        alert ("Train number And Train Name does not match.");
    }
}
 
function train_class_validation()
{
    if(document.getElementById("tr_class_drop_down").selectedIndex!=0&&document.getElementById("tr_no_drop_down").selectedIndex==0&&document.getElementById("tr_no_drop_down").selectedIndex==0)
    {
        alert("First select either Train number or Train name.");
        document.getElementById("tr_class_drop_down").selectedIndex=0;
    }
}

function train_quota_validation()
{
    if(document.getElementById("tr_quota_drop_down").selectedIndex!=0&&document.getElementById("tr_no_drop_down").selectedIndex==0&&document.getElementById("tr_no_drop_down").selectedIndex==0)
    {
        alert("First select either Train number or Train name.");
        document.getElementById("tr_quota_drop_down").selectedIndex=0;
    }
}

function search_validation(){
    if(document.getElementById("tr_no_drop_down").selectedIndex==0&&document.getElementById("tr_name_drop_down").selectedIndex==0&&document.getElementById("tr_class_drop_down").selectedIndex==0&&document.getElementById("tr_quota_drop_down").selectedIndex==0)
    {
        alert("Please select an Option.");
        return false;
    }
    else
    {
        return true;
    }
}




function remove_cookie()
{
    window.location = "/cgi-bin/reservation/reservation.cgi"; // TO Redirect THE PAGE
}


function get_fare_submit(){
    if(document.getElementById("tr_no_drop_down").selectedIndex==0 || document.getElementById("tr_source_drop_down").selectedIndex==0 || document.getElementById("tr_class_drop_down").selectedIndex==0 || document.getElementById("tr_dest_drop_down").selectedIndex==0)
    {
        alert("select all Option.");
        return false;
    }
    else
    {   
        if(document.fare_enq.lccp_day.value=="" || document.fare_enq.lccp_month.value=="" || document.fare_enq.lccp_year.value=="")
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
                   
                    return false;
                }
            }
            else
            {
                alert("Train number and Source or destination does not match.");
                return false;
            }
            
        }
    }
}

function get_day(){

    var d = new Date(document.fare_enq.lccp_month.value+" "+document.fare_enq.lccp_day.value+","+document.fare_enq.lccp_year.value);
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
    var day;
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
            day=xmlhttp.responseText.replace(";",",");
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

function reserve_submit(){
    if(document.getElementById("tr_no_drop_down").selectedIndex==0 || document.getElementById("tr_source_drop_down").selectedIndex==0 || document.getElementById("tr_class_drop_down").selectedIndex==0 || document.getElementById("tr_dest_drop_down").selectedIndex==0)
    {
        alert("select all Option.");
        return false;
    }
    else
    {   
        if(document.reserve.lccp_day.value=="" || document.reserve.lccp_month.value=="" || document.reserve.lccp_year.value=="")
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
                return true;
            }
            else
            {
                alert("Invalid Source and destination");
                return false;
            }
        }
    }
}

function send_password()
{
    var userid=document.getElementById("username").value;
    if(userid==null || userid=="")
    {
        alert("enter User Name.");
    }
    else
    {
        $("#progress").css("display","block");
        var xmlhttp;
        //var bool=false;
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
                if(xmlhttp.responseText==1)
                {
                    alert("password has been sent to your Phone and Email.");
                }
                else if(xmlhttp.responseText==0)
                {
                    alert("user does not exist.");
                }    
            }
            
        }
    
        xmlhttp.open("POST","/cgi-bin/send_password.cgi",false)
        xmlhttp.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
        xmlhttp.send("userid="+userid); 
        $("#progress").css("display","none");
    }
}


/*function printpage()
{
  
    var f=document.getElementById("first_status_div");
    $(".head").css("display","none");
    $(".body").css("display","none");
    $(".display_tr").css("display","none");
    
    $(".first").css("display","block");
    
  window.print()
}*/