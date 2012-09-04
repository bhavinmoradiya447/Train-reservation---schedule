#!/usr/bin/perl -w
use strict;
use warnings;
BEGIN {push @INC, '/home/bhavin/project/cgi-bin/cgi';}
use  Database;
use CGI; 
use CGI::Cookie;
use HTML::Template;
use Encrypt_decrypt;
my $decryption=Encrypt_decrypt->new();

my $db=new Database();
my $cgi=new CGI();
my $return_value;
my $reservation_no=$cgi->param("reservation_no");
my $user_id=$cgi->param("user_id");

my $template=new HTML::Template(filename=>'../../../html/reservation/status/cancel_status.tmpl'); 


sub date_retrive{
           
 my $count=$db->select_query("select count(*) from cancelation where reservation_no=$reservation_no")->[0][0];
if($count+0 >0)
 {
     my $result=$db->select_query("select * from cancelation where reservation_no=$reservation_no");
     if($result->[0][1] eq $user_id)
     {
         my $data=[];
            foreach my $value(@$result)
           {  
                      
                      my $source=$db->select_query("select station_name from station where station_code='".$value->[9]."'")->[0][0];
                      my $dest=$db->select_query("select station_name from station where station_code='".$value->[10]."'")->[0][0];
                      push @$data,{RESERVATION_NO=>$value->[0],TRAIN_NO=>$value->[2],DATE=>$value->[6],SOURCE=>$source,DEST=>$dest,CLASS=>$value->[3],QUOTA=>$value->[4],SEAT_CANCEL=>$value->[5],AMOUNT=>$value->[8]};
           }
       return $data;    
}
else
{
         print "Content-Type: text/html\n\n";
         print "invalid user";
}
}

else
{
         print "Content-Type: text/html\n\n";
         print "invalid reservation number or you have not canceled any seat";
   
}

}

my %cookies = CGI::Cookie->fetch;
if(defined($cookies{'user_name'}))
{
if($cookies{'user_name'}->value eq "")
{
print "Content-Type: text/html\n\n";
print<<end
   <html>
   <head>
<script type="text/javascript">
   window.location="/cgi-bin/reservation/reservation.cgi";
</script>
</head>
<body></body>
   </html>

end
}
else{
%cookies = CGI::Cookie->fetch;


$template->param(USER_NAME=>$db->fatch_username( $decryption->decrypt($cookies{'user_name'}->value)));
$template->param(USER_ID=> $decryption->decrypt($cookies{'user_name'}->value));

$template->param(CANCEL_1=>&date_retrive);
print "Content-type:text/html\n\r\n\r";
print $template->output;
}
}
else
{
 print "Content-Type: text/html\n\n";
print<<end
   <html>
   <head>
<script type="text/javascript">
   window.location="/cgi-bin/reservation/reservation.cgi";
</script>
</head>
<body></body>
   </html>

end
  
 } 
