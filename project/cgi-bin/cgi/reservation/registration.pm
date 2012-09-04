#!/usr/bin/perl -w
use strict;
use warnings;
use HTML::Template;

package registration;


sub new{
    my $class=shift;
    return bless {},$class;   
}

sub date{
    my $data=[];   
    for(my $i=1;$i<=31;$i++)
    {
         push @{$data},{DATE_VALUE=>$i};
    }
    $data;
}
sub year{
 
    my $y=(localtime)[5];
    my $data=[];   
    for(my $i=$y-18;$i>=$y-110;$i--)
    {   
        push @{$data},{YEAR_VALUE=>$i+1900};
    }
    $data;
}
sub month{
    my @mon=qw(jan feb mar apr may jun jul aug sep oct nov dec);
    my $data=[];   
    foreach(@mon)
    {
        push @{$data},{MONTH_VALUE=>$_};
    }
    $data;
}

sub Error_page
{
    my $template=new HTML::Template(filename=>'../../html/reservation/registration.tmpl'); 
    $template->param(DATE=>&date); # to set  date
    $template->param(MONTH=>&month); # to set  month
    $template->param(YEAR=>&year); # to set  year

    $template->param(FIRST_NAME=>$_[1]);
    $template->param(LAST_NAME=>$_[2]);
    $template->param(HOUSE_NO=>$_[3]);
    $template->param(AREA=>$_[4]);
    $template->param(OTHER=>$_[5]);
    $template->param(CITY=>$_[6]);
    $template->param(STATE=>$_[7]);
    $template->param(PIN_NO=>$_[8]);
    $template->param(PHONE_NO=>$_[9]);
    $template->param(EMAIL=>$_[10]);

    $template->param(ERROR=>$_[11]);

    print "Content-type:text/html\n\r\n\r";
    print $template->output;
} 
1

