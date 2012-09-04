#!/usr/bin/perl -w
use strict;
use warnings;
use HTML::Template;
use CGI::Cookie;
BEGIN {push @INC, '/home/bhavin/project/cgi-bin/cgi';}
use Encrypt_decrypt;
use  Database;

my $db=new Database();
my $decryption=Encrypt_decrypt->new();
# my %cookies = CGI::Cookie->fetch;
    # for (keys %cookies) {
    # print $cookies{$_};
    # }

my $template=new HTML::Template(filename=>'../../../html/reservation/cancel/cancel.tmpl'); 

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
print "Content-type:text/html\n\r\n\r";

$template->param(USER_NAME=> $db->fatch_username( $decryption->decrypt($cookies{'user_name'}->value)));
$template->param(USER_ID=>$decryption->decrypt($cookies{'user_name'}->value));

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
