#!/usr/bin/perl -w
use strict;
use warnings;
use HTML::Template;
use CGI::Cookie;

my $template=new HTML::Template(filename=>'../../html/reservation/reservation.tmpl'); 
# sub tr_source{
# my $data=[{TR_SOURCE=>12345},{TR_SOURCE=>12345},{TR_SOURCE=>12345},{TR_SOURCE=>12345},{TR_SOURCE=>12345}];
# }
# sub tr_dest{
# my $data=[{TR_DEST=>12345},{TR_DEST=>12345},{TR_DEST=>12345},{TR_DEST=>12345},{TR_DEST=>12345}];
# }
# sub tr_no{
# my $data=[{TR_NO=>12345},{TR_NO=>12345},{TR_NO=>12345},{TR_NO=>12345},{TR_NO=>12345}];
# }
# sub age{
# my $data=[{VAR_AGE=>12345},{VAR_AGE=>12345},{VAR_AGE=>12345},{VAR_AGE=>12345}];
# }
# sub tr_cons{
# my $data=[{TR_CONS=>12345},{TR_CONS=>12345},{TR_CONS=>12345},{TR_CONS=>12345}];
# }

# # 

# # $template->param(TRAIN_NO=>&tr_no); # to set  train  number
# $template->param(TRAIN_SOURCE=>&tr_source); # to set  train  source
# $template->param(TRAIN_DEST=>&tr_dest); # to set  train  destination
# $template->param(AGE=>&age); # to set  age
# $template->param(TRAIN_CONS=>&tr_cons); # to set  train  concession

# 

my %cookies = CGI::Cookie->fetch;

if(defined($cookies{'user_name'}))
{
    if($cookies{'user_name'}->value ne "")
    {
        my $c = CGI::Cookie->new(-name => 'user_name',
        -value => '',
        );
        print "Set-Cookie: $c\n";    
    }
}
else
{
     my $c = CGI::Cookie->new(-name => 'user_name',
     -value => '',
    );
    
 print "Set-Cookie: $c\n";    
}

print "Content-type:text/html\n\r\n\r";
print $template->output;
