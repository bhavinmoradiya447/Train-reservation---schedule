#!/usr/bin/perl -w
use strict;
use warnings;
use registration;
use CGI;
use CGI::Cookie;

BEGIN {push @INC, '/home/bhavin/project/cgi-bin/cgi';}
use  Database;
use Encrypt_decrypt;



my $encryption=new Encrypt_decrypt();

my $obj=new registration();
my $cgi=new CGI();

my ($firstname,$lastname,$houseno,$area,$other,$city,$state,$pincode,$phoneno,$email,$username,$password)=($cgi->param('first_name'),$cgi->param('last_name'),$cgi->param('house_no'),$cgi->param('area'),$cgi->param('other'),$cgi->param('city'),$cgi->param('state'),$cgi->param('pin_code'),$cgi->param('phone_no'),$cgi->param('email'),$cgi->param('username'),$cgi->param('password'));

my $db=new Database();
my $temp=$db->user_validation($username);
if($temp eq "true")
{
    $obj->Error_page($cgi->param('first_name')?$cgi->param('first_name'):"",$cgi->param('last_name')?$cgi->param('last_name'):"",$cgi->param('house_no')?$cgi->param('house_no'):"",$cgi->param('area')?$cgi->param('area'):"",$cgi->param('other')?$cgi->param('other'):"",$cgi->param('city')?$cgi->param('city'):"",$cgi->param('state')?$cgi->param('state'):"",$cgi->param('pin_code')?$cgi->param('pin_code'):"",$cgi->param('phone_no')?$cgi->param('phone_no'):"",$cgi->param('email')?$cgi->param('email'):"","User Name alredy exist.");
} 
elsif($temp eq "false")
{
  # my $time=$db->select_query("SELECT CURRENT_TIME")->[0][0];
  #  my $current_date=$db->select_query("SELECT CURRENT_DATE")->[0][0];
    $temp=$db->insert_query("user",$username,$password,$firstname." ".$lastname,$houseno."   ".$area."   ".$other."   ".$city."   ".$state."   ".$pincode,$phoneno,$email,$cgi->param('year')."-".$cgi->param('month')."-".$cgi->param('date'),"true");    
    if($temp eq "date_error")
    {
        $obj->Error_page($cgi->param('first_name')?$cgi->param('first_name'):"",$cgi->param('last_name')?$cgi->param('last_name'):"",$cgi->param('house_no')?$cgi->param('house_no'):"",$cgi->param('area')?$cgi->param('area'):"",$cgi->param('other')?$cgi->param('other'):"",$cgi->param('city')?$cgi->param('city'):"",$cgi->param('state')?$cgi->param('state'):"",$cgi->param('pin_code')?$cgi->param('pin_code'):"",$cgi->param('phone_no')?$cgi->param('phone_no'):"",$cgi->param('email')?$cgi->param('email'):"","Invalid date.");
    }
    elsif($temp eq "error occor")
    {
        $obj->Error_page($cgi->param('first_name')?$cgi->param('first_name'):"",$cgi->param('last_name')?$cgi->param('last_name'):"",$cgi->param('house_no')?$cgi->param('house_no'):"",$cgi->param('area')?$cgi->param('area'):"",$cgi->param('other')?$cgi->param('other'):"",$cgi->param('city')?$cgi->param('city'):"",$cgi->param('state')?$cgi->param('state'):"",$cgi->param('pin_code')?$cgi->param('pin_code'):"",$cgi->param('phone_no')?$cgi->param('phone_no'):"",$cgi->param('email')?$cgi->param('email'):"","Error occure ,try again.");
    }    
    elsif($temp eq "true")
    {
#call reserve page;
# my $session=CGI::Session->new("driver:File",undef,{Directory=>'/tmp'});
# my $id=$session->id();  

        my $c = CGI::Cookie->new(-name => 'user_name',
        -value =>$encryption->encrypt($username),
        -expires => '+1d');
    
        print "Set-Cookie: $c\n";
        print "Content-Type: text/html\n\n";
print<<end
   <html>
   <head>
<script type="text/javascript">
   window.location="/cgi-bin/reservation/reserve/reserve.cgi";
</script>
</head>
<body><p>Loading, please wait ...</p></body>
   </html>

end

   
}   
}
