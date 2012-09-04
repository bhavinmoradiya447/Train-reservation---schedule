#!/usr/bin/perl -w
use strict;
use warnings;
use HTML::Template;
use CGI::Cookie;
use CGI;
BEGIN {push @INC, '/home/bhavin/project/cgi-bin/cgi';}
use  Database;

use Encrypt_decrypt;

my $encryption=Encrypt_decrypt->new();

        my $template;
my $cgi=new CGI();

my $username=$cgi->param('username');
my $password=$cgi->param('password');

if(!defined($username) ||!defined($password))
{
 
    $template=new HTML::Template(filename=>'../../html/reservation/reservation.tmpl'); 
    #$template->param(LOGIN_ERROR=>"Invalid Username or Password.");
    print "Content-type:text/html\n\r\n\r";
    print $template->output;
    
}
else{
    my $db=new Database();
    my $temp=$db->login_validation($username,$password);
    if($temp eq "true")
    {
        my $c = CGI::Cookie->new(-name => 'user_name',
        -value => $encryption->encrypt($username),
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
<body></body>
 </html>
end
}
else
{
    $template=new HTML::Template(filename=>'../../html/reservation/reservation.tmpl'); 
    $template->param(LOGIN_ERROR=>"Invalid Username or Password.");
    print "Content-type:text/html\n\r\n\r";
    print $template->output;
}
}
